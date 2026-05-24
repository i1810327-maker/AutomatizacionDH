import os
import uuid

from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException

from app.config import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from app.database import get_connection
from app.auth import get_current_user, require_rol

router = APIRouter(dependencies=[Depends(require_rol("docente"))])

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/reportes/")
def crear_reporte(
    titulo: str = Form(...),
    descripcion: str = Form(...),
    archivo: UploadFile = File(...),
    user: dict = Depends(get_current_user),
):
    ext = os.path.splitext(archivo.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            400, "Tipo de archivo no permitido. Solo PDF o Word (.pdf, .doc, .docx)"
        )

    contenido = archivo.file.read()
    if len(contenido) > MAX_FILE_SIZE:
        raise HTTPException(400, "El archivo excede el tamaño máximo de 10MB")

    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(contenido)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM usuarios WHERE correo = %s",
        (user["correo"],),
    )
    docente = cursor.fetchone()

    cursor.execute(
        "INSERT INTO reportes (docente_id, titulo, descripcion, archivo_ruta, estado) "
        "VALUES (%s, %s, %s, %s, 'pendiente')",
        (docente[0], titulo, descripcion, filepath),
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {"mensaje": "Reporte enviado correctamente", "id": cursor.lastrowid}


@router.get("/reportes/mis-reportes/")
def mis_reportes(user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, titulo, descripcion, estado, comentarios, created_at "
        "FROM reportes WHERE docente_id = (SELECT id FROM usuarios WHERE correo = %s) "
        "ORDER BY created_at DESC",
        (user["correo"],),
    )
    reportes = cursor.fetchall()
    cursor.close()
    conn.close()
    return reportes
