import os
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from app.dependencies import get_current_user
from app.internal.supabase import supabase
from app.internal.ipfs import upload_to_pinata
from app.internal.certification import generate_certificate, extract_certificate_info
from app.schemas.certifications import CertificateRequest
from app.internal.blockchain import contract, w3
import hashlib
from typing import Dict

# Helper function to get institution details from Supabase using the user ID
async def get_institution_by_user_id(user_id: str):
    try:
        # Query the institution table for the corresponding user_id
        response = supabase.table('institutions').select('*').eq('user_id', user_id).execute()
        if response.data:
            return response.data[0]  # Return the first matching institution
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching institution: {str(e)}")

router = APIRouter()

# Route to issue a certificate
@router.post("/issue-certificate")
async def issue_certificate(data: CertificateRequest, user: dict = Depends(get_current_user)):
    try:
        # Retrieve the institution information based on the current authenticated user
        institution = await get_institution_by_user_id(user['sub'])
        org_name = institution['name']
        institute_logo_url = institution['logo_url']

        # Generate the certificate
        output_pdf_path = f"{data.cne.lower()}_{data.candidate_name.lower()}_generated_certificate.pdf"
        generate_certificate(output_pdf_path, data.cne, data.candidate_name, data.major_name, org_name, institute_logo_url)

        # Upload the certificate to IPFS
        ipfs_hash = await upload_to_pinata(output_pdf_path)

        # Generate certificate ID based on extracted data
        certificate_id = hashlib.sha256(f"{data.cne}{data.candidate_name}{data.major_name}{org_name}".encode('utf-8')).hexdigest()
        
        # Blockchain Interaction: Call the smart contract function
        transaction = contract.functions.generateCertificate(
            certificate_id,
            data.cne,
            data.candidate_name,
            data.major_name,
            org_name,
            ipfs_hash,
        ).transact({"from": w3.eth.accounts[0]})

        # Get transaction receipt to confirm success
        transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction)
        # Serialize transaction receipt for response
        serialized_receipt = {
            "transactionHash": transaction_receipt.transactionHash.hex(),
            "blockHash": transaction_receipt.blockHash.hex(),
            "blockNumber": transaction_receipt.blockNumber,
            "gasUsed": transaction_receipt.gasUsed,
            "status": transaction_receipt.status,
        }
 
        # Clean up generated certificate file
        if os.path.exists(output_pdf_path):
            os.remove(output_pdf_path)

        return {
            "message": "Certificate issued successfully",
            "certificate_id": certificate_id,
            "ipfs_hash": ipfs_hash,
            "transaction_receipt": serialized_receipt,
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error issuing certificate: {e}")


@router.post("/verify-certificate")
async def verify_certificate(uploaded_file: UploadFile = File(...)) -> Dict:
    try:
        # Save the uploaded file temporarily
        temp_file_path = "certificate.pdf"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await uploaded_file.read())

        # Extract certificate details from the uploaded file
        try:
            cne, candidate_name, major_name, org_name = extract_certificate_info(temp_file_path)
        except Exception as extraction_error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to extract certificate details: {str(extraction_error)}"
            )

        # Remove the temporary file after extraction
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        # Calculate the certificate hash
        data_to_hash = f"{cne}{candidate_name}{major_name}{org_name}".encode("utf-8")
        certificate_id = hashlib.sha256(data_to_hash).hexdigest()

        # Call the smart contract to verify the certificate
        is_verified = contract.functions.isVerified(certificate_id).call()

        # Return the result
        if is_verified:
            return {
                "message": "Certificate is valid and verified.",
                "certificate_id": certificate_id,
                "status": "verified"
            }
        else:
            return {
                "message": "Invalid certificate! It might have been tampered with.",
                "certificate_id": certificate_id,
                "status": "unverified"
            }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verifying certificate: {str(e)}"
        )