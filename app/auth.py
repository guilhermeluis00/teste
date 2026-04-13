import jwt
import bcrypt
import os
import base64
import hashlib
import hmac
from datetime import datetime, timedelta

# busca no .env a chave segura
SECRET_KEY = os.getenv("SECRET_KEY", "changeme")

# Função para decodificar uma string base64 URL-safe
def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode((data + padding).encode("utf-8"))


# Função para verificar a senha usando PBKDF2-SHA256
def _verify_pbkdf2_sha256(password: str, hashed: str) -> bool:
    try:
        scheme, iter_s, salt_b64, hash_b64 = hashed.split("$", 3)
        if scheme != "pbkdf2_sha256":
            return False
        iterations = int(iter_s)
        salt = _b64url_decode(salt_b64)
        expected = _b64url_decode(hash_b64)
        candidate = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, iterations
        )
        return hmac.compare_digest(candidate, expected)
    except Exception:
        return False

# Função para hash uma senha usando PBKDF2-SHA256
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Função para verificar a senha usando PBKDF2-SHA256
def verify_password(password: str, hashed: str) -> bool:
    if not hashed:
        return False
    if hashed.startswith("pbkdf2_sha256$"):
        return _verify_pbkdf2_sha256(password, hashed)
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except ValueError:
        return False

# Função para criar um token JWT
def create_token(user_id: int, email: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(days=365)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")