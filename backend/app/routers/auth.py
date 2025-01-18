from app.internal.supabase import supabase
from app.schemas.institution import InstitutionRegistration, InstitutionLogin
from app.dependencies import get_current_user
from fastapi import APIRouter, HTTPException, status, Depends

router = APIRouter()

# Helper function to sign up a user
async def sign_up_user(email: str, password: str):
    try:
        response = supabase.auth.sign_up({
           "email": email, "password": password
           })
        if response.user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User sign-up failed")
        return response.user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    
# Helper function to create an institution in the database
async def create_institution(user_id: str, name: str, contact_email: str, address: str, phone_number: str, website_url: str, logo_url: str):
    try:
        institution = supabase.table('institutions').insert({
            'user_id': user_id,
            'name': name,
            'contact_email': contact_email,
            'address': address,
            'phone_number': phone_number,
            'website_url': website_url,
            'logo_url': logo_url
        }).execute()
        
        print(institution)
        return institution.data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

# Route to register an institution
@router.post("/register")
async def register_institution(data: InstitutionRegistration):
    print(data)
    try:
        user = await sign_up_user(data.email, data.password)
        institution = await create_institution(user.id, data.name, data.contact_email, data.address, data.phone_number, data.website_url, data.logo_url)
        return {"message": "Institution registered successfully", "institution": institution}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
# Helper function to sign in a user
async def sign_in_user(email: str, password: str):
    try:
        # Call the Supabase sign-in method
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if response.user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return response.session
    except HTTPException:
        # Re-raise the HTTPException (e.g., invalid credentials)
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred during login")
    
@router.post("/login")
async def login_institution(data: InstitutionLogin):
    try:
        session = await sign_in_user(data.email, data.password)
        return {
            "message": "Login successful",
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "expires_in": session.expires_in
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/institution")
async def get_institution(current_user: dict = Depends(get_current_user)):
    # Extract user_id from the decoded JWT
    user_id = current_user.get("sub")  # 'sub' typically contains the user ID

    # Query the Supabase institutions table for the user's institution
    response = supabase.table("institutions").select("*").eq("user_id", user_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Institution not found")

    return {"institution": response.data[0]}