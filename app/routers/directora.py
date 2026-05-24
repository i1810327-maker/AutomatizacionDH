import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.database import get_connection
from app.auth import get_current_user, require_rol
from app.email_service import send_rejection_email

router = APIRouter(dependencies=[Depends(require_rol("directora"))])


class RevisionRequest(BaseModel):
    comentarios: str = ""


@router.get("/directora/reportes/")
def listar_pendientes(user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.id, r.titulo, r.descripcion, r.archivo_ruta, r.estado,
               r.created_at, u.nombre AS autor, u.correo AS autor_correo
        FROM reportes r
        JOIN usuarios u ON r.docente_id = u.id
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


@router.put("/directora/reportes/{reporte_id}/aprobar")
def aprobar_reporte(reporte_id: int, user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE reportes SET estado = 'aprobado' WHERE id = %s AND estado = 'pendiente'",
        (reporte_id,),
    )
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(404, "Reporte no encontrado o ya fue revisado")
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": "Reporte aprobado correctamente"}


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
