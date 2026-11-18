# Guía: subir el proyecto a GitHub y hacer el Pull Request revisado

Hay dos caminos. **El A es el recomendado** porque deja una bitácora de commits ordenada por módulo.
El B sirve si solo tienen acceso a la página web de GitHub.

> ⚠️ Nunca suban la carpeta `.venv/` (ya está en `.gitignore`). Si usas la web, no la arrastres.

---

## Camino A – Con Git instalado (recomendado)

1. **Crear el repositorio vacío:** github.com → **New repository** → nombre (p. ej. `ecorutas`) →
   *sin* README, *sin* .gitignore → **Create repository**. Copia la URL.
2. **Agregar a los compañeros:** Settings → **Collaborators** → *Add people* (necesario para que puedan revisar el PR).
   Si el repositorio es privado, agrega también al profesor.
3. En la carpeta del proyecto abre una terminal y configura tu identidad (una sola vez):
   ```bash
   git config --global user.name "Tu Nombre"
   git config --global user.email "tu-correo@ejemplo.com"
   ```
4. Crea el historial de commits (uno por módulo + la rama del Pull Request):
   ```bash
   python scripts/git_ayuda.py historial
   ```
5. Conecta y sube:
   ```bash
   git remote add origin https://github.com/<usuario>/<repositorio>.git
   git push -u origin main feature/pruebas-unitarias
   ```
   (La primera vez GitHub te pedirá iniciar sesión en el navegador.)
6. **Pull Request:** en la página del repositorio aparece el aviso amarillo *Compare & pull request* →
   ponle título (`test: pruebas unitarias`) → la plantilla se llena sola → **Create pull request**.
7. **Revisión por un compañero** (él/ella, desde su cuenta): pestaña **Files changed** → botón
   **Review changes** → dejar al menos un comentario → elegir **Approve** → **Submit review**.
8. **Merge:** el autor pulsa **Merge pull request** → **Confirm merge**.
9. Actualiza y genera la bitácora final:
   ```bash
   git checkout main
   git pull
   python scripts/git_ayuda.py bitacora
   git add docs/BITACORA_COMMITS.md
   git commit -m "docs: bitácora de commits"
   git push
   ```

---

## Camino B – Solo con la página web de GitHub

1. Crea el repositorio (paso 1 y 2 del camino A).
2. **Add file → Upload files** y arrastra el contenido del proyecto **excepto la carpeta `tests/`**
   (GitHub web permite hasta 100 archivos por subida; si pasas ese límite, sube por partes).
   En *Commit changes* escribe un mensaje claro, p. ej. `feat: código fuente, base de datos e interfaz`,
   y deja **Commit directly to the main branch**. Repite por partes si quieres más commits
   (`tad/`, `modelo/`, `dao/`, `web/`, `interfaces/`, `docs/`…).
3. **Para el Pull Request:** **Add file → Upload files** → arrastra la carpeta `tests/` → en *Commit changes*
   elige **Create a new branch for this commit and start a pull request** → nombre
   `feature/pruebas-unitarias` → **Propose changes** → **Create pull request**.
4. Un compañero revisa y aprueba (paso 7 del camino A) y se hace el merge (paso 8).
5. La bitácora está en la pestaña **Commits** del repositorio; copia lo esencial a `docs/BITACORA_COMMITS.md`
   (**Add file → Create new file**) o descarga el log con el camino A.

---

## Qué debe ver el profesor en el repositorio

- [ ] Código fuente comentado (`app.py`, `dao/`, `modelo/`, `tad/`, `web/`)
- [ ] Carpeta `interfaces/`
- [ ] Varios commits con mensajes claros (pestaña **Commits**) y `docs/BITACORA_COMMITS.md`
- [ ] Al menos 1 Pull Request **revisado y aprobado por un compañero** (pestaña **Pull requests → Closed/Merged**)
- [ ] `README.md` con objetivo, ejecución, módulos y problemas/soluciones (rellena equipo e integrantes arriba)
- [ ] La aplicación corre siguiendo el README
