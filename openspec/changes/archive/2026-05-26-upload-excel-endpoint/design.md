## Context

Proyecto FastAPI minimalista con una sola ruta (`GET /`). Sin base de datos, sin autenticación, sin manejo de archivos. El sistema actual no puede sostener el flujo de reportes escolares.

## Goals / Non-Goals

**Goals:**
- Seed de usuarios desde Excel a MySQL con contraseñas hasheadas
- Login con JWT, panel según rol
- Directora: crear solicitudes de reporte con fecha límite
- Directora: notificar internamente a todos los docentes
- Docente: ver solicitudes y enviar reporte vinculado a una solicitud
- Directora: archivar reportes que cumplen, rechazar con comentarios + correo
- Probar el flujo completo exitosamente

**Non-Goals:**
- Interfaz gráfica elaborada (API sola)
- Recuperación de contraseña
- Edición de usuarios

## Decisions

1. **MySQL + phpMyAdmin** — Ya está corriendo y es conocido. Mejor que aprender SQLite para este proyecto.

2. **JWT para autenticación** — Stateless, fácil de implementar en FastAPI. El token contiene correo y rol.

3. **passlib + bcrypt para hash de contraseñas** — Estándar, seguro, compatible con FastAPI.

4. **python-multipart** — Necesario para recibir archivos vía `UploadFile` en FastAPI.

5. **Archivos en disco local** — Los PDFs/Word se guardan en `uploads/` con UUID. La DB guarda la ruta.

6. **Gmail API para correos** — Ya configurada, con credenciales OAuth2. Enviar correo al rechazar.

7. **Estructura de routers** — Separar por funcionalidad: `routers/auth.py`, `routers/docente.py`, `routers/directora.py`.

## Risks / Trade-offs

- **Archivos grandes** → Límite de tamaño en FastAPI. Para sistema escolar con PDFs ligeros es suficiente.
- **Gmail API requiere autenticación OAuth2** → Puede vencer el token. Mitigación: guardar token refrescado.
- **Sin HTTPS en desarrollo** → Contraseñas viajan en texto plano. Aceptable para pruebas locales.
