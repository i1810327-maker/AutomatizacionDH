## 1. Setup y Dependencias

- [x] 1.1 Agregar dependencias a `pyproject.toml`: `openpyxl`, `mysql-connector-python` (o `aiomysql`), `python-jose[cryptography]`, `passlib[bcrypt]`, `python-multipart`, `google-api-python-client`, `google-auth-httplib2`, `google-auth-oauthlib`
- [x] 1.2 Ejecutar `uv lock` para instalar dependencias
- [x] 1.3 Crear directorio `uploads/` para archivos subidos

## 2. Base de Datos MySQL

- [x] 2.1 Crear base de datos y tablas (usuarios, reportes) en MySQL vía script SQL
- [x] 2.2 Configurar conexión desde FastAPI a MySQL

## 3. Seed de Usuarios desde Excel

- [x] 3.1 Crear endpoint `POST /seed/` que recibe Excel y parsea con openpyxl
- [x] 3.2 Validar columnas requeridas (Correo, Clave, Rol)
- [x] 3.3 Hashear contraseñas con passlib/bcrypt e insertar en MySQL

## 4. Autenticación JWT

- [x] 4.1 Crear endpoint `POST /login/` que valida credenciales contra MySQL
- [x] 4.2 Generar token JWT con correo y rol
- [x] 4.3 Crear dependencia de FastAPI para proteger rutas según rol

## 5. Panel Docente — Envío de Reportes

- [x] 5.1 Crear endpoint `POST /reportes/` que recibe título, descripción y archivo
- [x] 5.2 Validar tipo de archivo (PDF o Word)
- [x] 5.3 Guardar archivo en `uploads/` con nombre único
- [x] 5.4 Insertar reporte en MySQL con estado "pendiente"
- [x] 5.5 Crear endpoint `GET /reportes/mis-reportes` para listar propios

## 6. Panel Directora — Revisión

- [x] 6.1 Crear endpoint `GET /directora/reportes/` para listar pendientes
- [x] 6.2 Crear endpoint `PUT /directora/reportes/{id}/aprobar`
- [x] 6.3 Crear endpoint `PUT /directora/reportes/{id}/rechazar` con comentarios requeridos

## 7. Notificaciones por Correo (Gmail API)

- [x] 7.1 Configurar autenticación Gmail API con credentials.json
- [x] 7.2 Implementar función de envío de correo al rechazar reporte
- [x] 7.3 Integrar en el flujo de rechazo (paso 6.3)

## 8. Verificación del Flujo Completo

- [x] 8.1 Iniciar servidor y verificar que arranca sin errores
- [x] 8.2 Seed de usuarios desde Excel
- [x] 8.3 Login como Docente y envío de reporte
- [x] 8.4 Login como Directora, ver reportes, aprobar uno
- [x] 8.5 Rechazar otro reporte con comentarios — correo pendiente de autorizar Gmail API
