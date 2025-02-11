from passlib.hash import scrypt
import jwt
from datetime import datetime, timedelta
from app.config import settings
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer
from jwt import DecodeError
from app.database import get_db
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import User
from cryptography.fernet import Fernet
import base64
from app.config import settings

security = HTTPBearer()

def hash_password(password: str) -> str:
    return scrypt.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return scrypt.verify(plain_password, hashed_password)

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Security(security), db: AsyncSession = Depends(get_db)):
    try:
        decoded_token = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email = decoded_token["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalide")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=401, detail="Utilisateur non trouvé")

    return user  # ✅ Retourner l'utilisateur complet

# Générer une clé de chiffrement si elle n'existe pas encore (à faire une seule fois)
def generate_encryption_key():
    return base64.urlsafe_b64encode(Fernet.generate_key()).decode()

# Charger la clé depuis le fichier .env
cipher = Fernet(settings.ENCRYPTION_KEY.encode())

def encrypt_data(data: str) -> bytes:
    """Chiffre une donnée sensible"""
    return cipher.encrypt(data.encode())

def decrypt_data(encrypted_data: bytes) -> str:
    """Déchiffre une donnée chiffrée"""
    return cipher.decrypt(encrypted_data).decode()