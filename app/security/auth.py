from passlib.hash import scrypt
import jwt
from datetime import datetime, timedelta
from app.config import settings
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.models import User

security = HTTPBearer()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def hash_password(password: str) -> str:
    """Hachage du mot de passe avec Scrypt (salé automatiquement)."""
    return scrypt.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie la correspondance entre un mot de passe en clair et un haché."""
    return scrypt.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """Crée un token JWT valide pour `ACCESS_TOKEN_EXPIRE_MINUTES` minutes."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Security(security), db: AsyncSession = Depends(get_db)):
    """Extrait et valide l'utilisateur à partir du token JWT."""
    payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("id")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    return user