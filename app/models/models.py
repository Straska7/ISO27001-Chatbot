from sqlalchemy import Column, Integer, String, LargeBinary
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    encrypted_email = Column(LargeBinary, nullable=False)  # ✅ Stockage de l'email chiffré
    email_salt = Column(LargeBinary, nullable=False)  # ✅ Stockage du sel
    email_iv = Column(LargeBinary, nullable=False)  # ✅ Stockage de l'IV
    hashed_password = Column(String(255), nullable=False)