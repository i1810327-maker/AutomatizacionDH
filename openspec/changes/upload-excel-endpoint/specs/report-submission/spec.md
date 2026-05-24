## ADDED Requirements

### Requirement: Docente envía reporte
El sistema SHALL permitir al Docente autenticado enviar un reporte mediante `POST /reportes/` con título, descripción y archivo (PDF o Word).

#### Scenario: Envío exitoso
- **WHEN** un Docente autenticado envía título, descripción y un archivo .pdf
- **THEN** el sistema guarda el archivo en `uploads/`, crea el registro en MySQL con estado "pendiente", y retorna 201

#### Scenario: Envío sin archivo
- **WHEN** un Docente envía título y descripción sin archivo
- **THEN** el sistema retorna 422

#### Scenario: Tipo de archivo inválido
- **WHEN** un Docente envía un archivo .png
- **THEN** el sistema retorna 400 indicando que solo se aceptan PDF o Word

### Requirement: Listar mis reportes
El sistema SHALL permitir al Docente ver sus reportes enviados mediante `GET /reportes/mis-reportes`.

#### Scenario: Docente ve sus reportes
- **WHEN** un Docente autenticado solicita sus reportes
- **THEN** retorna una lista con todos sus reportes y sus estados
