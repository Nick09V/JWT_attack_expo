# core/security.py
import jwt
import datetime
from fastapi import HTTPException
from core.config import SECRET_KEY

def create_jwt_token(username: str, name: str, role: str) -> str:
    """Genera un token firmado correctamente."""
    payload = {
        "sub": username,
        "name": name,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_jwt_token(token: str, secure_mode: bool) -> dict:
    """
    Decodifica el token. 
    Aquí es donde radica la vulnerabilidad si secure_mode es False.
    """
    try:
        if secure_mode:
            # MODO SEGURO: El servidor valida que la firma criptográfica coincida.
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        else:
            # MODO VULNERABLE: El servidor solo lee el JSON en Base64 y confía en él.
            # Ignora la firma (verify_signature: False).
            return jwt.decode(token, options={"verify_signature": False})
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ha expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Firma inválida o token manipulado")