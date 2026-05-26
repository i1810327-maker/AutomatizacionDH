## ADDED Requirements

### Requirement: Correo automático al rechazar
El sistema SHALL enviar un correo al Docente cuando la Directora rechaza su reporte. El correo SHALL incluir los comentarios de la Directora y el título del reporte. SHALL usar Gmail API.

#### Scenario: Rechazo dispara correo
- **WHEN** la Directora rechaza un reporte con comentarios
- **THEN** el Docente recibe un correo con asunto "Reporte rechazado: [título]" y el cuerpo incluye los comentarios

#### Scenario: Error Gmail API
- **WHEN** la Gmail API falla al enviar el correo
- **THEN** el sistema guarda un log del error pero el reporte queda como rechazado igual
