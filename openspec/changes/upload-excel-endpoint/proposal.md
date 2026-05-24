## Why

Sistema donde la Directora escolar gestiona reportes académicos. El flujo inicia con la Directora creando solicitudes de reporte con fechas límite, el sistema notifica internamente a los Docentes, ellos suben sus reportes (PDF/Word), y la Directora los revisa: si cumplen los archiva, si no, envía correo de rechazo con comentarios al Docente.

## What Changes

- Cargar usuarios desde un Excel (correo, clave, rol) a MySQL — seed inicial
- Login con correo y contraseña, redirección por rol
- Directora: crear solicitudes de reporte con fecha límite
- Directora: notificar internamente a todos los docentes sobre una solicitud
- Docente: ver solicitudes pendientes y enviar reporte vinculado a una solicitud
- Directora: ver reportes, descargar archivo, archivar (si cumple) o rechazar con comentarios
- Al rechazar: correo automático al Docente vía Gmail API

## Capabilities

### New Capabilities
- `excel-seed`: Carga de usuarios desde Excel a MySQL
- `auth-login`: Autenticación por correo y contraseña
- `solicitudes`: Directora crea solicitudes de reporte con fechas
- `notificaciones`: Sistema notifica internamente a docentes
- `report-submission`: Docente envía reporte vinculado a una solicitud
- `report-review`: Directora archiva o rechaza reportes
- `email-notification`: Correo automático al rechazar

### Modified Capabilities

*None*

## Impact

- `app/database.py`: Nuevas tablas `solicitudes` y `notificaciones`, campo `solicitud_id` en reportes
- `app/routers/directora.py`: Endpoints de solicitudes + notificar + archivar
- `app/routers/docente.py`: Ver solicitudes + ver notificaciones + enviar reporte vinculado
