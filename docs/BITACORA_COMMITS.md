# Bitácora de commits

**Repositorio:** https://github.com/langelap07-a11y/Proyecto
**Integrantes:** Eileen Sierra, Elkin Rodriguez y Angela Puentes
**Fecha de desarrollo y subida:** 18/11/2026

> El historial completo y exacto está en la pestaña **Commits** del repositorio.

## Commits principales (orden de subida)

| # | Mensaje | Contenido | Autor del commit |
|---|---------|-----------|------------------|
| 1 | `chore: estructura inicial, .gitignore y dependencias` | `.gitignore`, `requirements.txt`, `ejecutar.bat` | Angela Puentes (langelap07-a11y) |
| 2 | `feat(tad): lista enlazada simple para guardar las paradas` | carpeta `tad/` | Angela Puentes (langelap07-a11y) |
| 3 | `feat(modelo): clase abstracta Entidad y clases Barrio, Parada, Ruta y Reporte` | carpeta `modelo/` | Angela Puentes (langelap07-a11y) |
| 4 | `feat(db): esquema MySQL con datos de ejemplo` | carpeta `database/` | Angela Puentes (langelap07-a11y) |
| 5 | `feat(dao): conexión a MySQL y DAOs de barrio, ruta y reporte` | carpeta `dao/` | Angela Puentes (langelap07-a11y) |
| 6 | `feat(api): servidor Flask con los endpoints /api` | `app.py` | Angela Puentes (langelap07-a11y) |
| 7 | `feat(web): interfaz HTML, CSS y JavaScript con cuatro pestañas` | carpeta `web/` | Angela Puentes (langelap07-a11y) |
| 8 | `docs(interfaces): capturas y descripción de las pantallas` | carpeta `interfaces/` | Angela Puentes (langelap07-a11y) |
| 9 | `docs: README con objetivo, ejecución, módulos y problemas resueltos` | `README.md`, `docs/`, `scripts/` | Angela Puentes (langelap07-a11y) |
| 10 | `test: pruebas unitarias del TAD, el modelo y la API` | carpeta `tests/` | Angela Puentes (langelap07-a11y) |

## Commits de corrección

Al subir los pasos 2 a 5 por la web, los archivos quedaron sueltos en la raíz del repositorio en lugar de dentro de sus carpetas. Se borraron esos archivos y se volvieron a subir las carpetas completas (`tad/`, `modelo/`, `database/`, `dao/`). Estos commits aparecen en la pestaña **Commits**.

## Pull Requests

| PR | Rama | Contenido | Autora | Revisó | Estado |
|----|------|-----------|--------|--------|--------|
| #1 | `feature/plantilla-pull-request` | Plantilla de Pull Request (`.github/pull_request_template.md`) | Angela Puentes | Elkin Rodriguez (elkinrodriguez054-beep) | _[Merged / Open]_ |

## Convención de mensajes

`feat` (funcionalidad nueva) · `fix` (corrección) · `docs` (documentación) · `test` (pruebas) · `chore` (configuración).
