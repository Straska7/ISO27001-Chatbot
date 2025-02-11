"""
main.py - Point d'entrée de l'API FastAPI

📌 Ce fichier initialise et configure l'application FastAPI :
    - Déclare l'application avec FastAPI
    - Ajoute des middlewares de sécurité (CORS, Trusted Host)
    - Définit des routes API (inclusion du routeur `users`)
    - Gère les erreurs globales
    - Vérifie la connexion à la base de données
"""

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from app.database import get_db
from app.config import settings
from app.routes import users  # Import du fichier users.py
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

# ✅ Initialisation de l'application FastAPI
app = FastAPI(title=settings.PROJECT_NAME, version=settings.API_VERSION)

# ✅ Sécurité : Restriction des hôtes autorisés
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])  # ⚠️ À configurer en prod

# ✅ Sécurité : Middleware CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Change cela en prod : ["https://ton-site.com"]
    allow_methods=["*"],  # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les headers
)

# ✅ Gestion globale des erreurs
@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    """
    Intercepte les erreurs non gérées pour masquer les détails en production.
    
    🔹 En mode DEBUG, affiche le message d'erreur exact.
    🔹 En production, masque l'erreur pour éviter de divulguer des informations sensibles.
    """
    if settings.DEBUG:
        return JSONResponse(status_code=500, content={"detail": str(exc)})
    return JSONResponse(status_code=500, content={"detail": "Une erreur interne est survenue. Contactez l'admin."})

# ✅ Inclusion du routeur `users`
app.include_router(users.router)

# ✅ Route de test pour vérifier que l'API fonctionne
@app.get("/")
def read_root():
    """Route principale affichant un message de bienvenue."""
    return {"message": "Bienvenue sur ISO27001-Chatbot API 🚀"}

# ✅ Route pour tester la connexion à la base de données
@app.get("/db-test")
async def test_db(db: AsyncSession = Depends(get_db)):
    """
    Vérifie si la connexion à la base de données est opérationnelle.
    
    Retourne :
        - ✅ "Database connected!" si la connexion fonctionne.
        - ❌ "Database connection failed" en cas d'échec.
    """
    try:
        result = await db.execute(text("SELECT 1"))
        return {"status": "Database connected!", "result": result.scalar()}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}

# ✅ Route pour vérifier que la variable DATABASE_URL est bien chargée
@app.get("/check-db-url")
def check_db_url():
    """
    Vérifie si la variable d'environnement DATABASE_URL est bien définie.
    
    Utile pour le debug en développement.
    """
    return {"database_url": settings.DATABASE_URL}

# ✅ Route pour afficher les paramètres de configuration
@app.get("/config")
def check_env():
    """
    Affiche les paramètres de configuration actuels :
    - URL de la base de données
    - Mode DEBUG activé/désactivé
    """
    return {"database_url": settings.DATABASE_URL, "debug_mode": settings.DEBUG}