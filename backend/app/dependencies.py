from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from app.internal.supabase import supabase, SUPABASE_JWT_SECRET


# HTTPBearer will extract the Authorization header with "Bearer <token>"
auth_scheme = HTTPBearer()

# Function to decode and validate the JWT
def decode_jwt(token: str):
    try:
        # Decode the JWT using the secret and validate it
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"], options={"verify_aud": False})
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Dependency to extract and validate the token
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    token = credentials.credentials
    if token.startswith("Bearer "):
        token = token.split("Bearer ")[1]
    return decode_jwt(token)
        
    