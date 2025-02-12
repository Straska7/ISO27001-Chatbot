"""
database.py - Configuration de la base de données SQLAlchemy (asynchrone)

📌 Ce fichier configure :
    - Le chargement des variables d'environnement (DATABASE_URL)
    - L'initialisation du moteur de base de données asynchrone
    - La création de sessions de base de données pour les requêtes
    - L'intégration avec SQLAlchemy pour la gestion des modèles
"""
import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# ✅ Chargement des variables d’environnement
load_dotenv()

# ✅ Vérification et récupération de l'URL de la base de données
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL est introuvable dans .env ! Vérifie ta configuration.")
# ✅ Création du moteur de base de données asynchrone
engine = create_async_engine(DATABASE_URL, echo=False)

# ✅ Configuration des sessions de base de données
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# ✅ Définition de la base pour SQLAlchemy (corrige l'erreur ImportError dans Alembic)
Base = declarative_base()

# ✅ Dépendance pour récupérer une session de base de données
async def get_db():
    """
    Fournit une session de base de données asynchrone pour exécuter des requêtes.

    Utilisation :
        - `db: AsyncSession = Depends(get_db)`

    Cette fonction est utilisée dans les routes FastAPI pour injecter une session de base de données.
    """
    async with SessionLocal() as session:
        yield session