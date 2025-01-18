from pydantic import BaseModel, EmailStr, Field


# Pydantic model for the input data
class InstitutionRegistration(BaseModel):
    email: str
    password: str
    name: str
    contact_email: str
    address: str = None
    phone_number: str = None
    website_url: str = None
    logo_url: str = None
    
class InstitutionLogin(BaseModel):
    email: EmailStr  
    password: str = Field(..., min_length=8) 