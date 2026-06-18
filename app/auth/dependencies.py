from fastapi import Request
from fastapi import HTTPException

from jose import jwt
from jose import JWTError

from app.config import (SECRET_KEY, ALGORITHM)

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User

def get_current_user_id(request: Request):

    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Não autenticado"
        )

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

        return int(user_id)

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )


def get_current_user(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )

    return user
