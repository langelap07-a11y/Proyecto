"""Ayudante de Git para el proyecto EcoRutas.

Uso (desde la carpeta raíz del proyecto):

    python scripts/git_ayuda.py historial   # crea el repositorio local con commits ordenados por módulo
    python scripts/git_ayuda.py bitacora    # escribe docs/BITACORA_COMMITS.md con el `git log` real

Los commits usan TU nombre y correo de Git (git config user.name / user.email) y la fecha real
del momento en que se ejecutan. Si el trabajo lo hizo todo el equipo, cada integrante debería
hacer sus propios commits con su cuenta; este script es solo un punto de partida ordenado.
"""
import subprocess
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# (mensaje del commit, archivos/carpetas que incluye) - se ejecutan en este orden en `main`.
COMMITS_MAIN = [
    ("chore: estructura inicial, .gitignore y dependencias", [".gitignore", "requirements.txt", "ejecutar.bat"]),
    ("feat(tad): lista enlazada simple para guardar las paradas", ["tad"]),
    ("feat(modelo): clase abstracta Entidad y clases Barrio, Parada, Ruta y Reporte", ["modelo"]),
    ("feat(db): esquema MySQL con datos de ejemplo", ["database"]),
    ("feat(dao): conexión a MySQL y DAOs de barrio, ruta y reporte", ["dao"]),
    ("feat(api): servidor Flask con los endpoints /api", ["app.py"]),
    ("feat(web): interfaz HTML, CSS y JavaScript con cuatro pestañas", ["web"]),
    ("docs(interfaces): capturas y descripción de las pantallas", ["interfaces"]),
    ("docs: README con objetivo, ejecución, módulos y problemas resueltos",
     ["README.md", ".github", "docs/GUIA_GITHUB_Y_PULL_REQUEST.md", "scripts"]),
]

# Commit que va en una rama aparte para practicar el Pull Request.
RAMA_PR = "feature/pruebas-unitarias"
COMMIT_PR = ("test: pruebas unitarias del TAD, el modelo y la API", ["tests"])


def git(*args, capturar=False):
    resultado = subprocess.run(["git", *args], cwd=RAIZ, text=True, capture_output=capturar)
    if resultado.returncode != 0:
        sys.exit(f"Error ejecutando: git {' '.join(args)}\n{resultado.stderr or ''}")
    return resultado.stdout if capturar else None


def commit(mensaje, rutas):
    existentes = [r for r in rutas if (RAIZ / r).exists()]
    git("add", *existentes)
    git("commit", "-m", mensaje)
    print("  ✔", mensaje)


def historial():
    if (RAIZ / ".git").exists():
        sys.exit("Ya existe un repositorio Git aquí. Si quieres rehacerlo, borra la carpeta .git primero.")
    git("init", "-b", "main")
    print("Creando commits en la rama main...")
    for mensaje, rutas in COMMITS_MAIN:
        commit(mensaje, rutas)
    print(f"Creando la rama {RAMA_PR} (para el Pull Request)...")
    git("checkout", "-b", RAMA_PR)
    commit(*COMMIT_PR)
    git("checkout", "main")
    print("\nListo. Siguientes pasos:")
    print("  1) Crea un repositorio VACÍO en github.com y copia su URL.")
    print("  2) git remote add origin <URL>")
    print(f"  3) git push -u origin main {RAMA_PR}")
    print("  4) En GitHub: Compare & pull request -> pide revisión a un compañero (ver docs/GUIA_GITHUB_Y_PULL_REQUEST.md)")
    print("  5) Cuando se apruebe y se haga merge: git pull y  python scripts/git_ayuda.py bitacora")


def bitacora():
    salida = git("log", "--all", "--reverse", "--date=short",
                 "--pretty=format:%h|%ad|%an|%s", capturar=True)
    if not salida.strip():
        sys.exit("Todavía no hay commits.")
    filas = ["| # | Commit | Fecha | Autor | Mensaje |", "|---|--------|-------|-------|---------|"]
    for n, linea in enumerate(salida.splitlines(), 1):
        h, fecha, autor, msg = linea.split("|", 3)
        filas.append(f"| {n} | `{h}` | {fecha} | {autor} | {msg.replace('|', '/')} |")
    destino = RAIZ / "docs" / "BITACORA_COMMITS.md"
    destino.write_text(
        "# Bitácora de commits\n\n"
        f"_Generada automáticamente con `git log` el {date.today().isoformat()}. "
        "Para actualizarla: `python scripts/git_ayuda.py bitacora`._\n\n"
        + "\n".join(filas) + "\n\n"
        "## Pull Requests\n\n"
        "| PR | Rama | Autor | Revisó | Estado |\n|----|------|-------|--------|--------|\n"
        "| #1 | `feature/pruebas-unitarias` | _[nombre]_ | _[compañero]_ | _[Merged / Open]_ |\n",
        encoding="utf-8")
    print("Bitácora escrita en", destino.relative_to(RAIZ))


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("historial", "bitacora"):
        sys.exit(__doc__)
    historial() if sys.argv[1] == "historial" else bitacora()
