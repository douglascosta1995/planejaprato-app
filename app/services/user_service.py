from sqlalchemy.orm import Session

from app.models.user import User
from app.auth.password import hash_password
from app.auth.password import verify_password


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, name: str, email: str, password: str):
    user = User(name=name, email=email, password_hash=hash_password(password))

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(db, email, password):
    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user
