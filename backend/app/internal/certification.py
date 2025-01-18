from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import pdfplumber

def generate_certificate(output_path, cne, candidate_name, major_name, org_name, institute_logo_path):
    # Create a PDF document
    doc = SimpleDocTemplate(output_path, pagesize=letter)

    # Create a list to hold the elements of the PDF
    elements = []

    # Add institute logo and institute name
    # if institute_logo_path:
        # logo = Image(institute_logo_path, width=150, height=150)
        # elements.append(logo)

    # Add institute name
    institute_style = ParagraphStyle(
        "InstituteStyle",
        parent=getSampleStyleSheet()["Title"],
        fontName="Helvetica-Bold",
        fontSize=15,
        spaceAfter=40,
    )
    institute = Paragraph(org_name, institute_style)
    elements.extend([institute, Spacer(1, 12)])

    # Add title
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=getSampleStyleSheet()["Title"],
        fontName="Helvetica-Bold",
        fontSize=25,
        spaceAfter=20,
    )
    title1 = Paragraph("Certificate of Completion", title_style)
    elements.extend([title1, Spacer(1, 6)])

    # Add recipient name, CNE, and major with increased line space
    recipient_style = ParagraphStyle(
        "RecipientStyle",
        parent=getSampleStyleSheet()["BodyText"],
        fontSize=14,
        spaceAfter=6,
        leading=18,
        alignment=1
    )

    recipient_text = f"""This is to certify that<br/><br/>
                     <font color='red'> {candidate_name} </font><br/>
                     with CNE <br/> 
                    <font color='red'> {cne} </font> <br/><br/>
                     has successfully completed the major:<br/>
                     <font color='blue'> {major_name} </font>"""

    recipient = Paragraph(recipient_text, recipient_style)
    elements.extend([recipient, Spacer(1, 12)])

    # Build the PDF document
    doc.build(elements)

    print(f"Certificate generated and saved at: {output_path}")
    
def extract_certificate_info(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Extract text from the first page (assuming certificates are a single page)
            page = pdf.pages[0]
            text = page.extract_text()

            # Split the text into lines for further processing
            lines = text.splitlines()

            # Assuming the following text structure in the certificate:
            # Line 1: Organization Name
            # Line 3: Candidate Name
            # Line 5: CNE (Student's Code)
            # Last line: Major Name

            org_name = lines[0].strip()
            candidate_name = lines[3].strip()
            cne = lines[5].strip()
            major_name = lines[-1].strip()

            return cne, candidate_name, major_name, org_name
    except Exception as e:
        raise ValueError(f"Error extracting information from certificate: {e}")
    