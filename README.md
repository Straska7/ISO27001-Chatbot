# 📜 ISO27001-Chatbot API 🚀
Une API FastAPI sécurisée permettant aux utilisateurs de poser des questions sur la norme **ISO 27001** grâce à un chatbot intelligent.

---

## 📌 Fonctionnalités
- 🔐 **Authentification sécurisée** avec hachage des mots de passe (`Scrypt`) et JWT.
- 🔒 **Stockage sécurisé des emails** avec chiffrement AES-GCM.
- 🗄️ **Base de données asynchrone** avec `SQLAlchemy` et `Alembic`.
- 🌐 **API REST bien structurée** avec `FastAPI` et documentation intégrée (`Swagger`).
- 🚀 **Connexion et vérification de la base de données** pour assurer le bon fonctionnement.

---

## 🔧 Installation & Exécution

### 1️⃣ **Pré-requis**
- Python **3.10+**
- PostgreSQL (ou Supabase)
- `pip` et `venv` pour la gestion des dépendances
- Un compte OpenAI (si utilisation d’un modèle GPT)

### 2️⃣ **Installation du projet**
```sh
git clone https://github.com/Straska7/ISO27001-Chatbot.git
cd ISO27001-Chatbot/backend

ISO27001-Chatbot/
│── backend/                 # Backend FastAPI
│   ├── app/                 # Code principal de l’API
│   │   ├── models/          # Modèles de base de données (SQLAlchemy)
│   │   ├── routes/          # Routes API (utilisateurs, chatbot)
│   │   ├── security/        # Gestion de l’authentification et chiffrement
│   │   ├── security_utils.py # Fonctions utilitaires pour la sécurité
│   │   ├── database.py      # Configuration de la base de données
│   │   ├── main.py          # Point d’entrée de l’API
│   │   ├── config.py        # Variables d’environnement et paramètres globaux
│   ├── migrations/          # Scripts de migration de la base de données
│   ├── requirements.txt     # Liste des dépendances Python
│   ├── README.md            # Documentation principale
│   ├── docs/                # Documentation API détaillée
│
│── mobile-app/              # Application Flutter (à venir)


# Aller dans le dossier backend
cd backend

# Créer un environnement virtuel et l'activer
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### 3️⃣ **Configuration**

💡 Créez un fichier `.env` dans `backend/` avec les variables suivantes :
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
SECRET_KEY=supersecretkey
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
```

### 4️⃣ **Lancer l’API**
```sh
uvicorn app.main:app --reload
```
L’API sera accessible sur (http://127.0.0.1:8000/docs)

