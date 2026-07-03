from sqlalchemy.orm import Session

from app.services.user_service import create_user
from app.services.user_service import get_user_by_email


SYSTEM_USER_EMAIL = "system@planejaprato.local"


def populate_system_user(db: Session):

    existing_user = get_user_by_email(db, SYSTEM_USER_EMAIL)

    if existing_user:
        print("Usuário do sistema já existe.")
        return existing_user

    user = create_user(
        db=db,
        name="PlanejaPrato",
        email=SYSTEM_USER_EMAIL,
        password="system"
    )

    print("Usuário do sistema criado.")

    return user
