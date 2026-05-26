## Why

El `.gitignore` actual no excluye `__pycache__/`, `token.json` ni `.venv/`, lo que puede llevar a subir archivos temporales, tokens de Gmail API y el entorno virtual al repositorio.

## What Changes

- Agregar `__pycache__/` para excluir cachés de Python
- Agregar `token.json` para no subir el token de Gmail API
- Agregar `.venv/` para no subir el entorno virtual

## Capabilities

### New Capabilities

*None — es un cambio de configuración, no una nueva capacidad del sistema.*

### Modified Capabilities

*None*

## Impact

- `.gitignore`: Se agregan 3 entradas
