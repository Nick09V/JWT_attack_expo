# main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
from api.routes import router as api_router

app = FastAPI(title="Demo JWT Attack Modular")

# Montamos las rutas de la API bajo el prefijo /api
app.include_router(api_router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
def get_ui():
    """Lee el archivo HTML separado y lo sirve."""
    html_path = Path("templates/index.html")
    if not html_path.exists():
        return "<h1>Error: Archivo index.html no encontrado en la carpeta templates.</h1>"
    return html_path.read_text(encoding="utf-8")