# api/routes.py
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from core.config import MOCK_DB
from core.security import create_jwt_token, decode_jwt_token

router = APIRouter()

class LoginData(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginData):
    user = MOCK_DB.get(data.username)
    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    # Delegamos la creación del token
    token = create_jwt_token(data.username, user["name"], user["role"])
    return {"token": token}

@router.get("/profile")
def get_profile(secure_mode: bool = False, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token no proporcionado")
    
    token = authorization.split(" ")[1]
    
    # Delegamos la validación del token
    payload = decode_jwt_token(token, secure_mode)
    
    # Si la validación no falló, confiamos en el payload
    username = payload.get("sub")
    role = payload.get("role")
    
    if role == "profesor":
        return {"name": payload.get("name"), "role": role, "message": "Acceso a edición concedido"}
    else:
        user_db = MOCK_DB.get(username, {})
        return {"name": payload.get("name"), "role": role, "grades": user_db.get("grades", {})}

# api/routes.py (Añade esto al final del archivo)

class GradeUpdate(BaseModel):
    student_username: str
    subject: str
    new_grade: float

@router.post("/update_grade")
def update_grade(data: GradeUpdate, secure_mode: bool = False, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token no proporcionado")
    
    token = authorization.split(" ")[1]
    payload = decode_jwt_token(token, secure_mode)
    
    # Verificamos si el rol en el token le permite hacer esto
    if payload.get("role") != "profesor":
        raise HTTPException(status_code=403, detail="Acceso denegado: No tienes privilegios de profesor")
    
    # Modificamos la base de datos en memoria (persistencia temporal durante la ejecución)
    student = MOCK_DB.get(data.student_username)
    if not student or "grades" not in student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    student["grades"][data.subject] = data.new_grade
    return {"message": f"Nota de {data.student_username} en {data.subject} actualizada a {data.new_grade}"}