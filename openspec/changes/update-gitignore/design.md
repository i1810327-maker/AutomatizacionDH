## Context

El `.gitignore` actual excluye lo básico de Python pero falta `__pycache__/`, `token.json` y `.venv/`. Estos archivos no deben subirse al repositorio por razones de seguridad y limpieza.

## Goals / Non-Goals

**Goals:**
- Excluir `__pycache__/` del control de versiones
- Excluir `token.json` (contiene token de Gmail API)
- Excluir `.venv/` (entorno virtual local)

**Non-Goals:**
- No se modifican otras reglas de `.gitignore`
- No se eliminan archivos ya trackeados

## Decisions

- Agregar las entradas en orden alfabético dentro de la sección de Python del `.gitignore` existente.
- Usar `/` al final de directorios (`__pycache__/`, `.venv/`) para excluir solo directorios, no archivos con ese nombre.

## Risks / Trade-offs

- Si `token.json` ya está siendo trackeado por git, agregarlo a `.gitignore` no lo va a dejar de trackear. Habrá que usar `git rm --cached token.json`.
