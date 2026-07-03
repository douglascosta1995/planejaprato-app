from app.database.database import Base
from app.database.database import engine
from app.database.database import SessionLocal

from app.scripts.initialize_db import initialize_database

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    initialize_database(db)
finally:
    db.close()

print("Banco recriado.")
