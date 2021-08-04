from fastapi import APIRouter, status, HTTPException, Depends
from ..schemas.auth_schema import Token, Login
from ..services.auth_service import create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Auth']
)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
def login(request: OAuth2PasswordRequestForm = Depends()):
    if request.username == "admin" and request.password == "admin":
        return {"access_token": create_access_token({"sub": request.username})}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid username or password")
