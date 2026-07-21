from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.modules.auth.repository import AuthRepository
from src.modules.auth.schemas import TokenResponse
from src.modules.auth.service import (
    AuthService,
    InactiveUserError,
    InvalidCredentialsError,
)
from src.shared.database.connection import get_db

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=TokenResponse)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:
    service = AuthService(AuthRepository(db))
    try:
        _, access_token = service.authenticate(form.username, form.password)
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except InactiveUserError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sua conta está desativada.",
        ) from exc

    return TokenResponse(access_token=access_token)
