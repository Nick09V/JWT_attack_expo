# core/config.py

# En producción, esto vendría de un archivo .env
SECRET_KEY = "clave_super_secreta_epn"

# Base de datos simulada
MOCK_DB = {
    "nvalverde": {
        "password": "123", 
        "name": "Piero Hincapie", 
        "role": "estudiante",
        "grades": {"Física": 8.5, "Matemáticas": 9.2, "Ingeniería de Software": 9.8}
    },
    "admin": {
        "password": "admin", 
        "name": "Dr. Pérez", 
        "role": "profesor"
    }
}