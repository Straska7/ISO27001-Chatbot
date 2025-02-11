from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.models import User
from app.security.auth import hash_password, verify_password, create_access_token, get_current_user
from app.security.encryption import encrypt_data, decrypt_data, generate_salt_iv

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
async def register_user(name: str, email: str, password: str, db: AsyncSession = Depends(get_db)):
    """
    Inscription d'un nouvel utilisateur.

    - Chiffre l'email avant de le stocker.
    - Hache le mot de passe avec Scrypt.
    - Vérifie si l'utilisateur existe déjà avant d'ajouter un nouvel enregistrement.

    **Paramètres :**
    - `name` : Nom de l'utilisateur.
    - `email` : Email de l'utilisateur.
    - `password` : Mot de passe en clair.

    **Retour :**
    - Message de succès et ID utilisateur.
    """
    salt, iv = generate_salt_iv()
    encrypted_email = encrypt_data(email, salt, iv)

    result = await db.execute(select(User).where(User.encrypted_email == encrypted_email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="L'utilisateur existe déjà")

    hashed_password = hash_password(password)

    new_user = User(
        name=name,
        encrypted_email=encrypted_email,
        email_salt=salt,
        email_iv=iv,
        hashed_password=hashed_password
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "Utilisateur créé avec succès", "id": new_user.id}

@router.post("/login")
async def login(email: str, password: str, db: AsyncSession = Depends(get_db)):
    """
    Authentification utilisateur.

    - Déchiffre l'email et vérifie l'existence de l'utilisateur.
    - Vérifie le mot de passe haché.
    - Génère un token JWT pour les connexions valides.

    **Paramètres :**
    - `email` : Email de connexion.
    - `password` : Mot de passe en clair.

    **Retour :**
    - Token d'accès en cas de succès.
    """
    result = await db.execute(select(User))
    users = result.scalars().all()

    for user in users:
        try:
            decrypted_email = decrypt_data(user.encrypted_email, user.email_salt, user.email_iv)

            if decrypted_email.strip() == email.strip():
                if verify_password(password, user.hashed_password):
                    token = create_access_token({"id": user.id})
                    return {"access_token": token, "token_type": "bearer"}
        except:
            continue

    raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Retourne les informations de l'utilisateur actuellement authentifié.

    **Retour :**
    - ID, nom et email (déchiffré).
    """
    email = decrypt_data(current_user.encrypted_email, current_user.email_salt, current_user.email_iv)

    return {
        "message": "Utilisateur authentifié",
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "email": email
        }
    }