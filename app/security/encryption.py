from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend
import os

def generate_salt_iv():
    """
    Génère un Salt et un IV sécurisés pour le chiffrement AES-GCM.

    📌 **Pourquoi ?**
    - **Salt (16 bytes)** : Utilisé pour la dérivation de la clé AES (renforce la sécurité).
    - **IV (12 bytes)** : Vecteur d'initialisation nécessaire pour AES-GCM (garantit l'unicité des opérations).

    📌 **Retourne :**
    - `salt` (bytes) : Une valeur aléatoire de 16 octets.
    - `iv` (bytes) : Un vecteur d'initialisation de 12 octets.

    🔐 **Sécurité :**
    - `os.urandom()` génère des valeurs **cryptographiquement sécurisées**.
    - AES-GCM exige un **IV unique** pour chaque chiffrement afin d'éviter les failles.
    """

    salt = os.urandom(16)  # Génère un Salt aléatoire (16B)
    iv = os.urandom(12)    # Génère un IV aléatoire (12B) conforme à AES-GCM

    return salt, iv

def generate_key(salt: bytes):
    """
    Génère une clé AES 256 bits à partir d'un Salt via PBKDF2-HMAC.

    📌 **Pourquoi ?**
    - **PBKDF2-HMAC** est une fonction de dérivation de clé résistante aux attaques par force brute.
    - L'utilisation d'un **Salt** empêche les attaques par pré-calcul (Rainbow Tables).

    📌 **Paramètres :**
    - `salt` (bytes) : Une valeur aléatoire (16 bytes) utilisée pour générer la clé.

    📌 **Retourne :**
    - `key` (bytes) : Une clé AES 256 bits (32 bytes) dérivée du Salt.

    🔐 **Sécurité :**
    - `hashes.SHA256` garantit une fonction de hachage robuste.
    - **100,000 itérations** de PBKDF2 ralentissent les attaques par force brute.
    - Génère une clé **uniquement basée sur le Salt**, donc toujours cohérente.
    """

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),  # Algorithme de hachage robuste
        length=32,  # Clé AES 256 bits (32B)
        salt=salt,  # Utilisation du Salt unique pour éviter les attaques Rainbow Table
        iterations=100000,  # Ralentit les attaques par brute-force
        backend=default_backend()
    )

    return kdf.derive(salt)  # Retourne la clé AES dérivée

# ✅ Fonction de chiffrement
def encrypt_data(plaintext: str, salt: bytes, iv: bytes) -> bytes:
    """
    Chiffre une donnée avec AES-GCM et retourne les données sous la forme :
    `Salt + IV + Tag + Ciphertext`.

    📌 **Paramètres :**
    - `plaintext` (str) : Texte en clair à chiffrer.
    - `salt` (bytes) : Valeur aléatoire utilisée pour générer la clé AES (16 bytes).
    - `iv` (bytes) : Vecteur d'initialisation pour AES-GCM (12 bytes).

    📌 **Retourne :**
    - `bytes` : Données chiffrées sous la forme **Salt (16B) + IV (12B) + Tag (16B) + Ciphertext**.

    🔐 **Sécurité :**
    - Utilise **AES-256-GCM** pour un chiffrement **authentifié** et sécurisé.
    - Le **Tag d'authentification (16 bytes)** assure l'intégrité des données chiffrées.
    - **Le Salt et l'IV doivent être stockés** pour permettre le déchiffrement ultérieur.
    """

    # Générer une clé AES 256 bits à partir du Salt
    key = generate_key(salt)

    # Initialiser AES-GCM avec la clé et l'IV
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Ajouter un padding sécurisé (PKCS7) avant chiffrement
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()

    # Chiffrement des données avec AES-GCM
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Construire les données chiffrées : Salt (16B) + IV (12B) + Tag (16B) + Ciphertext
    encrypted_data = salt + iv + encryptor.tag + ciphertext

    return encrypted_data

def decrypt_data(encrypted_data: bytes, salt: bytes, iv: bytes) -> str:
    """
    Déchiffre une donnée AES-GCM en utilisant le Salt, l'IV et le Tag stockés.

    📌 **Paramètres :**
    - `encrypted_data` (bytes) : Données chiffrées au format **Salt + IV + Tag + Ciphertext**.
    - `salt` (bytes) : Valeur utilisée pour générer la clé AES (16 bytes).
    - `iv` (bytes) : Vecteur d'initialisation pour AES-GCM (12 bytes).

    📌 **Retourne :**
    - `str` : Données déchiffrées sous forme de texte en clair.

    🔐 **Sécurité :**
    - Utilise **AES-256-GCM**, garantissant à la fois **confidentialité et intégrité** des données.
    - Le **Tag d'authentification (16 bytes)** est extrait et validé pour détecter toute modification des données.
    - Si le déchiffrement échoue (clé incorrecte, données altérées), une **erreur est levée**.
    """

    try:
        # Extraction du Tag (16 bytes) et du Ciphertext
        tag = encrypted_data[28:44]   # Tag d'authentification (16B)
        ciphertext = encrypted_data[44:]  # Données chiffrées

        # Générer la clé AES à partir du Salt
        key = generate_key(salt)

        # Initialiser AES-GCM avec la clé, l'IV et le Tag
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()

        # Déchiffrer les données
        decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

        # Suppression du padding sécurisé (PKCS7)
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

        return decrypted_data.decode()

    except Exception:
        # Lever une erreur en cas d'échec du déchiffrement
        raise ValueError("❌ Erreur lors du déchiffrement : données corrompues ou clé incorrecte.")
    
