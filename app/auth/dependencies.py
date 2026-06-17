from fastapi import Request
from fastapi import HTTPException

from jose import jwt
from jose import JWTError

from app.config import (SECRET_KEY, ALGORITHM)


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
