import os
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.database import get_connection
from app.auth import get_current_user, require_rol
from app.email_service import send_rejection_email

router = APIRouter(dependencies=[Depends(require_rol("directora"))])


class RevisionRequest(BaseModel):
    comentarios: str = ""


class SolicitudRequest(BaseModel):
    titulo: str
    descripcion: str
    fecha_limite: date


# ── Solicitudes ──────────────────────────────────────────


@router.post("/directora/solicitudes/")
def crear_solicitud(body: SolicitudRequest, user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM usuarios WHERE correo = %s",
        (user["correo"],),
    )
    directora = cursor.fetchone()
    cursor.execute(
        "INSERT INTO solicitudes (directora_id, titulo, descripcion, fecha_limite) "
        "VALUES (%s, %s, %s, %s)",
        (directora[0], body.titulo, body.descripcion, body.fecha_limite),
    )
    conn.commit()
    solicitud_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {"mensaje": "Solicitud creada", "id": solicitud_id}


@router.get("/directora/solicitudes/")
def listar_solicitudes(user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.id, s.titulo, s.descripcion, s.fecha_limite, s.created_at,
               (SELECT COUNT(*) FROM reportes WHERE solicitud_id = s.id) AS reportes_recibidos
        FROM solicitudes s
        ORDER BY s.created_at DESC
    """)
    solicitudes = cursor.fetchall()
    cursor.close()
    conn.close()
    return solicitudes


@router.post("/directora/solicitudes/{solicitud_id}/notificar")
def notificar_docentes(solicitud_id: int, user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, titulo FROM solicitudes WHERE id = %s",
        (solicitud_id,),
    )
    solicitud = cursor.fetchone()
    if not solicitud:
        cursor.close()
        conn.close()
        raise HTTPException(404, "Solicitud no encontrada")

    cursor.execute("SELECT id FROM usuarios WHERE rol = 'docente'")
    docentes = cursor.fetchall()
    if not docentes:
        cursor.close()
        conn.close()
        raise HTTPException(400, "No hay docentes registrados")

    mensaje = f"Nueva solicitud: {solicitud['titulo']}"
    for d in docentes:
        cursor.execute(
            "INSERT INTO notificaciones (usuario_id, solicitud_id, mensaje) VALUES (%s, %s, %s)",
            (d["id"], solicitud_id, mensaje),
        )
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": f"Notificados {len(docentes)} docente(s)"}


# ── Reportes ─────────────────────────────────────────────


@router.get("/directora/reportes/")
def listar_pendientes(user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.id, r.titulo, r.descripcion, r.archivo_ruta, r.estado,
               r.created_at, u.nombre AS autor, u.correo AS autor_correo,
               s.titulo AS solicitud_titulo
        FROM reportes r
        JOIN usuarios u ON r.docente_id = u.id
        LEFT JOIN solicitudes s ON r.solicitud_id = s.id
        WHERE r.estado = 'pendiente'
        ORDER BY r.created_at DESC
    """)
    reportes = cursor.fetchall()
    cursor.close()
    conn.close()
    return reportes


@router.get("/directora/reportes/{reporte_id}/descargar")
def descargar_reporte(reporte_id: int, user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT archivo_ruta, titulo FROM reportes WHERE id = %s",
        (reporte_id,),
    )
    reporte = cursor.fetchone()
    cursor.close()
    conn.close()

    if not reporte:
        raise HTTPException(404, "Reporte no encontrado")

    ruta = reporte["archivo_ruta"]
    if not os.path.exists(ruta):
        raise HTTPException(404, "Archivo no encontrado en el servidor")

    nombre_archivo = f"{reporte['titulo']}{os.path.splitext(ruta)[1]}"
    return FileResponse(ruta, filename=nombre_archivo)


@router.put("/directora/reportes/{reporte_id}/archivar")
def archivar_reporte(reporte_id: int, user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE reportes SET estado = 'archivado' WHERE id = %s AND estado = 'pendiente'",
        (reporte_id,),
    )
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(404, "Reporte no encontrado o ya fue revisado")
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": "Reporte archivado correctamente"}


@router.put("/directora/reportes/{reporte_id}/rechazar")
def rechazar_reporte(
    reporte_id: int,
    body: RevisionRequest,
    user: dict = Depends(get_current_user),
):
    if not body.comentarios or not body.comentarios.strip():
        raise HTTPException(400, "Debes escribir comentarios para rechazar el reporte")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.id, r.titulo, r.estado, u.correo AS autor_correo, u.nombre AS autor_nombre
        FROM reportes r
        JOIN usuarios u ON r.docente_id = u.id
        WHERE r.id = %s
    """, (reporte_id,))
    reporte = cursor.fetchone()

    if not reporte or reporte["estado"] != "pendiente":
        cursor.close()
        conn.close()
        raise HTTPException(404, "Reporte no encontrado o ya fue revisado")

    cursor.execute(
        "UPDATE reportes SET estado = 'rechazado', comentarios = %s WHERE id = %s",
        (body.comentarios.strip(), reporte_id),
    )
    conn.commit()
    cursor.close()
    conn.close()

    send_rejection_email(
        destinatario=reporte["autor_correo"],
        nombre_docente=reporte["autor_nombre"],
        titulo_reporte=reporte["titulo"],
        comentarios=body.comentarios.strip(),
    )

    return {"mensaje": "Reporte rechazado. Se notificó al docente."}
