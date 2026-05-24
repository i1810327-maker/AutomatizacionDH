## Why

Se necesita un sistema donde la Directora escolar gestione reportes académicos enviados por Docentes. El flujo completo permite: cargar usuarios desde Excel, autenticación por rol (Directora/Docente), envío de reportes (PDF/Word), revisión con aprobación o rechazo, y notificación automática por correo (Gmail API) al rechazar un reporte con comentarios.

## What Changes

- Cargar usuarios desde un Excel (correo, clave, rol) a MySQL — seed inicial
- Login con correo y contraseña, redirigiendo al panel según el rol
- Panel Docente: formulario para enviar reporte (título + descripción + archivo PDF/Word)
- Panel Directora: lista de reportes pendientes, aprobar o rechazar con comentarios
- Al rechazar: enviar correo automático al Docente con los comentarios vía Gmail API
- Gestionar archivos subidos en el sistema de archivos local

## Capabilities

### New Capabilities
- `excel-seed`: Carga de usuarios desde Excel a MySQL con contraseñas hasheadas
- `auth-login`: Autenticación por correo y contraseña, redirección por rol
- `report-submission`: Docente envía reporte con título, descripción y archivo adjunto
- `report-review`: Directora revisa, aprueba o rechaza reportes con comentarios
- `email-notification`: Envío automático de correos vía Gmail API al rechazar un reporte

### Modified Capabilities

*None*

## Impact

- `main.py`: Reestructuración completa con routers, login, paneles
- `pyproject.toml`: Nuevas dependencias: `openpyxl`, `mysql-connector` o `aiomysql`, `python-jose` (JWT), `passlib` (hash), `python-multipart`
- Base de datos MySQL con tablas: usuarios, reportes
- Archivos subidos en directorio local (`uploads/`)
- Credenciales Gmail API para envío de correos
