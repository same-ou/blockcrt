from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.certificates import router as certificates_router
from app.internal.blockchain import contract_address

app = FastAPI()

# Include the API router with the specific prefix
app.include_router(auth_router, prefix="/institutions", tags=["institutions"])
app.include_router(certificates_router, prefix="/certificates", tags=["certificates"]) 

@app.get("/")
async def info():
    return {
        'address': contract_address
    }