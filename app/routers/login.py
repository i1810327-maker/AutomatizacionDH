from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database import get_connection
from app.auth import verify_password, create_token

router = APIRouter()


class LoginRequest(BaseModel):
    correo: str
    clave: str


@router.post("/login/")
def login(body: LoginRequest):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, correo, clave_hash, nombre, rol FROM usuarios WHERE correo = %s",
        (body.correo,),
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user or not verify_password(body.clave, user["clave_hash"]):
        raise HTTPException(401, "Credenciales inválidas")

    token = create_token(user["correo"], user["rol"])
    return {
        "token": token,
        "rol": user["rol"],
        "nombre": user["nombre"],
        "panel": "/directora" if user["rol"] == "directora" else "/docente",
    }
