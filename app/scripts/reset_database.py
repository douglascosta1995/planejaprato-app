from app.database.database import Base
from app.database.database import engine

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("Banco recriado.")
