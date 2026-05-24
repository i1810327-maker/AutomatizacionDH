import os
import uuid

from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException

from app.config import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from app.database import get_connection
from app.auth import get_current_user, require_rol

router = APIRouter(dependencies=[Depends(require_rol("docente"))])

os.makedirs(UPLOAD_DIR, exist_ok=True)


# ── Solicitudes Pendientes ──────────────────────────────


@router.get("/docente/solicitudes/")
def solicitudes_pendientes(user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.id, s.titulo, s.descripcion, s.fecha_limite, s.created_at,
               (SELECT COUNT(*) FROM reportes WHERE solicitud_id = s.id
                AND docente_id = (SELECT id FROM usuarios WHERE correo = %s)) AS ya_envie
        FROM solicitudes s
        ORDER BY s.fecha_limite ASC
    """, (user["correo"],))
    solicitudes = cursor.fetchall()
    cursor.close()
    conn.close()
    return solicitudes


# ── Notificaciones ──────────────────────────────────────


@router.get("/docente/notificaciones/")
def listar_notificaciones(user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT n.id, n.mensaje, n.leida, n.solicitud_id, n.created_at
        FROM notificaciones n
        JOIN usuarios u ON n.usuario_id = u.id
        WHERE u.correo = %s
        ORDER BY n.created_at DESC
    """, (user["correo"],))
    notis = cursor.fetchall()
    cursor.close()
    conn.close()
    return notis


@router.put("/docente/notificaciones/{notificacion_id}/leer")
def marcar_leida(notificacion_id: int, user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE notificaciones SET leida = 1 WHERE id = %s AND usuario_id = "
        "(SELECT id FROM usuarios WHERE correo = %s)",
        (notificacion_id, user["correo"]),
    )
    conn.commit()
    filas = cursor.rowcount
    cursor.close()
    conn.close()
    if filas == 0:
        raise HTTPException(404, "Notificación no encontrada")
    return {"mensaje": "Notificación marcada como leída"}


# ── Envío de Reportes ────────────────────────────────────


@router.post("/reportes/")
def crear_reporte(
    solicitud_id: int = Form(...),
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
        "INSERT INTO reportes (docente_id, solicitud_id, titulo, descripcion, archivo_ruta, estado) "
        "VALUES (%s, %s, %s, %s, %s, 'pendiente')",
        (docente[0], solicitud_id, titulo, descripcion, filepath),
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {"mensaje": "Reporte enviado correctamente", "id": cursor.lastrowid}


@router.get("/reportes/mis-reportes/")
def mis_reportes(user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.id, r.titulo, r.descripcion, r.estado, r.comentarios,
               r.created_at, s.titulo AS solicitud_titulo
        FROM reportes r
        LEFT JOIN solicitudes s ON r.solicitud_id = s.id
        WHERE r.docente_id = (SELECT id FROM usuarios WHERE correo = %s)
        ORDER BY r.created_at DESC
    """, (user["correo"],))
    reportes = cursor.fetchall()
    cursor.close()
    conn.close()
    return reportes
