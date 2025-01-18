from pydantic import BaseModel

class CertificateRequest(BaseModel):
    cne: str  # Student's code (CNE)
    candidate_name: str
    major_name: str  # Major instead of course
