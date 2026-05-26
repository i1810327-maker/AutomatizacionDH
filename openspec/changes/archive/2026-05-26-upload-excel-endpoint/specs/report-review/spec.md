## ADDED Requirements

### Requirement: Directora lista reportes pendientes
El sistema SHALL permitir a la Directora ver todos los reportes pendientes mediante `GET /directora/reportes/`.

#### Scenario: Ver pendientes
- **WHEN** la Directora autenticada solicita los reportes pendientes
- **THEN** retorna lista de reportes con estado "pendiente" incluyendo autor, título y descripción

### Requirement: Directora aprueba o rechaza reporte
El sistema SHALL permitir a la Directora aprobar (`PUT /directora/reportes/{id}/aprobar`) o rechazar (`PUT /directora/reportes/{id}/rechazar`) un reporte. Al rechazar SHALL incluir comentarios.

#### Scenario: Aprobar reporte
- **WHEN** la Directora aprueba un reporte
- **THEN** el estado del reporte cambia a "aprobado"

#### Scenario: Rechazar reporte con comentarios
- **WHEN** la Directora rechaza un reporte con comentarios
- **THEN** el estado cambia a "rechazado", se guardan los comentarios, y se dispara el envío de correo al Docente

#### Scenario: Rechazar sin comentarios
- **WHEN** la Directora rechaza sin escribir comentarios
- **THEN** el sistema retorna 400 solicitando comentarios
