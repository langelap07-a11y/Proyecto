# Bitácora de commits

> Este archivo se **regenera con el historial real** del repositorio ejecutando
> `python scripts/git_ayuda.py bitacora`. Hasta entonces muestra el plan de commits.

## Plan de commits

| # | Mensaje | Archivos | Responsable |
|---|---------|----------|-------------|
| 1 | `chore: estructura inicial, .gitignore y dependencias` | `.gitignore`, `requirements.txt`, `ejecutar.bat` | _[nombre]_ |
| 2 | `feat(tad): lista enlazada simple para guardar las paradas` | `tad/` | _[nombre]_ |
| 3 | `feat(modelo): clase abstracta Entidad y clases Barrio, Parada, Ruta y Reporte` | `modelo/` | _[nombre]_ |
| 4 | `feat(db): esquema MySQL con datos de ejemplo` | `database/` | _[nombre]_ |
| 5 | `feat(dao): conexión a MySQL y DAOs de barrio, ruta y reporte` | `dao/` | _[nombre]_ |
| 6 | `feat(api): servidor Flask con los endpoints /api` | `app.py` | _[nombre]_ |
| 7 | `feat(web): interfaz HTML, CSS y JavaScript con cuatro pestañas` | `web/` | _[nombre]_ |
| 8 | `docs(interfaces): capturas y descripción de las pantallas` | `interfaces/` | _[nombre]_ |
| 9 | `docs: README con objetivo, ejecución, módulos y problemas resueltos` | `README.md`, `.github/`, `docs/`, `scripts/` | _[nombre]_ |
| 10 | `test: pruebas unitarias del TAD, el modelo y la API` (**Pull Request #1**) | `tests/` | _[nombre]_ · revisó: _[compañero]_ |

## Convención de mensajes

`feat` (funcionalidad nueva) · `fix` (corrección) · `docs` (documentación) · `test` (pruebas) · `chore` (configuración).
