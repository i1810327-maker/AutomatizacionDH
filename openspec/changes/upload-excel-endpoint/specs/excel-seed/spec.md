## ADDED Requirements

### Requirement: Seed usuarios desde Excel
El sistema SHALL aceptar un archivo Excel (.xlsx) con columnas Correo, Clave, Rol a través de `POST /seed/`. El sistema SHALL hashear la contraseña con bcrypt antes de insertar en MySQL.

#### Scenario: Seed exitoso
- **WHEN** se envía un Excel válido con 3 usuarios
- **THEN** los 3 usuarios se insertan en la tabla `usuarios` con contraseñas hasheadas

#### Scenario: Excel sin columnas requeridas
- **WHEN** el Excel falta la columna Clave
- **THEN** el sistema retorna 400 indicando las columnas faltantes

### Requirement: Tabla usuarios en MySQL
El sistema SHALL tener una tabla `usuarios` con campos: id, correo, clave_hash, rol, nombre.

#### Scenario: Esquema correcto
- **WHEN** se ejecuta la migración
- **THEN** la tabla `usuarios` existe con los campos definidos
