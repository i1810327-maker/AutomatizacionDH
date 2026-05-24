## 1. Setup y Dependencias

- [x] 1.1 Agregar dependencias a `pyproject.toml`
- [x] 1.2 Ejecutar `uv lock` para instalar dependencias
- [x] 1.3 Crear directorio `uploads/`

## 2. Base de Datos MySQL

- [x] 2.1 Crear base de datos y tablas
- [x] 2.2 Configurar conexión
- [x] 2.3 Agregar tablas `solicitudes`, `notificaciones` y `solicitud_id`

## 3. Seed de Usuarios

- [x] 3.1 Endpoint `POST /seed/`
- [x] 3.2 Validar columnas
- [x] 3.3 Hash + insertar

## 4. Autenticación JWT

- [x] 4.1 `POST /login/`
- [x] 4.2 Token JWT
- [x] 4.3 Dependencia por rol

## 5. Solicitudes (Directora)

- [x] 5.1 `POST /directora/solicitudes/` — crear solicitud con fecha límite
- [x] 5.2 `GET /directora/solicitudes/` — listar solicitudes
- [x] 5.3 `POST /directora/solicitudes/{id}/notificar` — notificar a docentes

## 6. Notificaciones Internas

- [x] 6.1 `GET /docente/notificaciones/` — ver notificaciones
- [x] 6.2 `PUT /docente/notificaciones/{id}/leer` — marcar leída

## 7. Panel Docente

- [x] 7.1 `POST /reportes/` con `solicitud_id`
- [x] 7.2 Validar tipo archivo
- [x] 7.3 Guardar en `uploads/`
- [x] 7.4 Insertar reporte vinculado
- [x] 7.5 `GET /docente/solicitudes/` — ver solicitudes pendientes
- [x] 7.6 `GET /reportes/mis-reportes/`

## 8. Panel Directora — Revisión

- [x] 8.1 `GET /directora/reportes/` — listar pendientes
- [x] 8.2 `GET /directora/reportes/{id}/descargar`
- [x] 8.3 `PUT .../archivar` — reporte archivado
- [x] 8.4 `PUT .../rechazar` + comentarios + correo automático

## 9. Verificación

- [x] 9.1 Directora crea solicitud y notifica
- [x] 9.2 Docente ve solicitud y envía reporte
- [x] 9.3 Directora archiva o rechaza
- [x] 9.4 Correo al rechazar
