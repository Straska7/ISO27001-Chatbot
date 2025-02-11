# 📖 Documentation de l'API ISO27001-Chatbot

## 📌 Routes Utilisateurs (`/users`)

### 🔹 **Inscription**
**POST** `/users/register`
- ✅ **Description** : Crée un nouvel utilisateur.
- 🔒 **Sécurité** : Aucune (accessible à tous).
- 📥 **Params** :
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }
  ```

### 🔹 **Connexion**
**POST** `/users/login`
- ✅ **Description** : Authentifie un utilisateur existant.
- 🔒 **Sécurité** : Aucune (accessible à tous).
- 📥 **Params** :
  ```json
  {
    "email": "john@example.com",
    "password": "password123"
  }
  ```

### 🔹 **Obtenir les informations de l'utilisateur**
**GET** `/users/me`
- ✅ **Description** : Récupère les informations de l'utilisateur authentifié.
- 🔒 **Sécurité** : Requiert un token d'authentification.
- 📥 **Headers** :
  ```json
  {
    "Authorization": "Bearer <token>"
  }
  ```

### 🔹 **Mettre à jour les informations de l'utilisateur**
**PUT** `/users/me`
- ✅ **Description** : Met à jour les informations de l'utilisateur authentifié.
- 🔒 **Sécurité** : Requiert un token d'authentification.
- 📥 **Headers** :
  ```json
  {
    "Authorization": "Bearer <token>"
  }
  ```
- 📥 **Params** :
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "newpassword123"
  }
  ```

### 🔹 **Supprimer l'utilisateur**
**DELETE** `/users/me`
- ✅ **Description** : Supprime le compte de l'utilisateur authentifié.
- 🔒 **Sécurité** : Requiert un token d'authentification.
- 📥 **Headers** :
  ```json
  {
    "Authorization": "Bearer <token>"
  }
  ```

## 📌 Routes de Chatbot (`/chatbot`)

### 🔹 **Envoyer un message**
**POST** `/chatbot/message`
- ✅ **Description** : Envoie un message au chatbot et reçoit une réponse.
- 🔒 **Sécurité** : Requiert un token d'authentification.
- 📥 **Headers** :
  ```json
  {
    "Authorization": "Bearer <token>"
  }
  ```
- 📥 **Params** :
  ```json
  {
    "message": "Bonjour, comment puis-je vous aider?"
  }
  ```

### 🔹 **Obtenir l'historique des messages**
**GET** `/chatbot/history`
- ✅ **Description** : Récupère l'historique des messages échangés avec le chatbot.
- 🔒 **Sécurité** : Requiert un token d'authentification.
- 📥 **Headers** :
  ```json
  {
    "Authorization": "Bearer <token>"
  }
  ```

## 📌 Routes de Sécurité (`/security`)

### 🔹 **Vérifier la conformité**
**GET** `/security/compliance`
- ✅ **Description** : Vérifie la conformité aux normes ISO27001.
- 🔒 **Sécurité** : Requiert un token d'authentification.
- 📥 **Headers** :
  ```json
  {
    "Authorization": "Bearer <token>"
  }
  ```

### 🔹 **Obtenir les rapports de sécurité**
**GET** `/security/reports`
- ✅ **Description** : Récupère les rapports de sécurité générés.
- 🔒 **Sécurité** : Requiert un token d'authentification.
- 📥 **Headers** :
  ```json
  {
    "Authorization": "Bearer <token>"
  }
  ```

### 🔹 **Générer un rapport de sécurité**
**POST** `/security/reports`
- ✅ **Description** : Génère un nouveau rapport de sécurité.
- 🔒 **Sécurité** : Requiert un token d'authentification.
- 📥 **Headers** :
  ```json
  {
    "Authorization": "Bearer <token>"
  }
  ```
- 📥 **Params** :
  ```json
  {
    "type": "full",
    "date": "2023-10-01"
  }
  ```