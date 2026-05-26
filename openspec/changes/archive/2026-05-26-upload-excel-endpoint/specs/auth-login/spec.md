## ADDED Requirements

### Requirement: Login con correo y contraseña
El sistema SHALL autenticar usuarios mediante `POST /login/` con correo y contraseña. SHALL retornar un token JWT con el rol del usuario.

#### Scenario: Login exitoso Directora
- **WHEN** una Directora envía correo y contraseña correctos
- **THEN** recibe un JWT con rol="directora" y redirección al panel de Directora

#### Scenario: Login exitoso Docente
- **WHEN** un Docente envía correo y contraseña correctos
- **THEN** recibe un JWT con rol="docente" y redirección al panel de Docente

#### Scenario: Contraseña incorrecta
- **WHEN** se envía un correo existente con contraseña incorrecta
- **THEN** el sistema retorna 401 Unauthorized

#### Scenario: Usuario inexistente
- **WHEN** se envía un correo no registrado
- **THEN** el sistema retorna 401 Unauthorized
