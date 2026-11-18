# ♻ EcoRutas – Rutas de recolección de basura

>  **Integrantes:** _Elkin Rodriguez, Angela Puentes, Eileen Sierra_ · **Asignatura:** _Programación II_

## 1. Objetivo del proyecto

Que la comunidad pueda **consultar cuándo pasa el camión de la basura por su barrio o vereda** y
**reportar fallas** del servicio (no pasó el camión, basura acumulada, escombros), mientras la empresa de
aseo administra las rutas y atiende los reportes desde un panel.

Objetivos específicos:
- Publicar las rutas con día, hora, vehículo y paradas ordenadas, filtradas por barrio.
- Permitir a los ciudadanos enviar reportes y a la empresa cambiar su estado (*Pendiente → En atención → Resuelto*).
- Aplicar los contenidos de la asignatura: **TAD (lista enlazada)**, **POO** y **persistencia en MySQL** con patrón DAO.

## 2. Tecnologías

| Capa | Tecnología |
|------|-----------|
| Interfaz | HTML + CSS + JavaScript (sin frameworks) |
| Servidor / API | Python 3 + Flask |
| Base de datos | MySQL (XAMPP) con PyMySQL |
| Pruebas | `unittest` (incluido en Python) |

## 3. Instrucciones de ejecución

**Requisitos:** Python 3.10+, XAMPP (MySQL) y Git.

```bash
# 1. Clonar el repositorio
git clone https://github.com/<usuario>/<repositorio>.git
cd <repositorio>

# 2. (Recomendado) crear y activar un entorno virtual
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux / macOS

# 3. Instalar dependencias
pip install -r requirements.txt
```

4. **Base de datos:** abre XAMPP → inicia **MySQL** → entra a `http://localhost/phpmyadmin` → pestaña
   **Importar** → elige `database/schema.sql` → *Continuar*. Esto crea la base `rutas_basura` con datos de ejemplo.
   (También sirve: `mysql -u root < database/schema.sql`).
5. **Ejecutar:** `python app.py` (en Windows también basta con doble clic a `ejecutar.bat`).
6. **Abrir** <http://localhost:5000>.

Si tu MySQL no usa `root` sin contraseña, define las variables de entorno `DB_HOST`, `DB_PORT`, `DB_USER`,
`DB_PASSWORD` y `DB_NAME` antes de ejecutar (ver `dao/conexion.py`).

### Pruebas automáticas (no necesitan MySQL)

```bash
python -m unittest discover -s tests -t . -v
```

## 4. Estructura y descripción de módulos

```
ecorutas/
├── app.py                 # Servidor Flask y rutas de la API
├── tad/lista_enlazada.py  # TAD ListaEnlazada
├── modelo/                # Clases del dominio (POO)
├── dao/                   # Acceso a datos (MySQL)
├── database/schema.sql    # Tablas y datos de ejemplo
├── web/                   # Interfaz: index.html, css/, js/
├── interfaces/            # Capturas y descripción de las pantallas
├── tests/                 # Pruebas unitarias
├── docs/                  # Bitácora de commits y guía de GitHub / Pull Request
└── scripts/git_ayuda.py   # Crea el historial de commits y genera la bitácora
```

| Módulo | Descripción |
|--------|-------------|
| `app.py` | Crea la app Flask, expone los endpoints REST, valida datos, convierte errores a JSON y sirve la carpeta `web/`. No contiene SQL. |
| `tad/lista_enlazada.py` | **TAD** lista enlazada simple: `agregar_al_final`, `agregar_al_inicio`, `obtener`, `eliminar`, `esta_vacia`, `len()` e iteración. Guarda las paradas de cada ruta y los resultados de los DAO. |
| `modelo/entidad.py` | Clase **abstracta** base con `id`, `to_dict()` y `describir()` (herencia + abstracción). |
| `modelo/barrio.py`, `parada.py`, `reporte.py`, `ruta.py` | Clases hijas de `Entidad`. Atributos encapsulados con `@property`; cada una implementa su propio `to_dict()` (**polimorfismo**). `Ruta` contiene sus `Parada` en una `ListaEnlazada` (**composición**). |
| `dao/conexion.py` | Configuración y fábrica de conexiones PyMySQL. |
| `dao/barrio_dao.py`, `ruta_dao.py`, `reporte_dao.py` | Patrón **DAO**: único lugar con SQL. Usan consultas parametrizadas y cierran la conexión siempre. |
| `database/schema.sql` | Tablas `barrio`, `ruta`, `parada`, `reporte` con llaves foráneas y `ON DELETE CASCADE`. |
| `web/index.html`, `css/estilos.css`, `js/app.js` | Interfaz de 4 pestañas (Rutas, Reportar, Aprende, Administrar) que consume la API con `fetch`. |

### API

| Método | Ruta | Qué hace |
|--------|------|----------|
| GET | `/api/barrios` | Lista barrios y veredas |
| GET | `/api/rutas[?barrio=ID]` | Lista rutas con paradas (filtro opcional) |
| POST | `/api/rutas` | Crea una ruta con sus paradas |
| DELETE | `/api/rutas/<id>` | Elimina una ruta y sus paradas |
| GET | `/api/reportes` | Lista reportes ciudadanos |
| POST | `/api/reportes` | Crea un reporte |
| PUT | `/api/reportes/<id>` | Cambia el estado de un reporte |

## 5. Funcionalidades de la aplicación

- Consultar rutas por barrio/vereda (días, hora, vehículo, paradas en orden).
- Enviar reportes ciudadanos con validación de campos obligatorios.
- Crear y eliminar rutas desde el panel de administración.
- Cambiar el estado de los reportes.
- Guía educativa para separar residuos.
- Diseño adaptable a celular (ver [`interfaces/`](interfaces/README.md)).

## 6. Problemas encontrados y soluciones aplicadas

| # | Problema | Solución |
|---|----------|----------|
| 1 | Flask no encontraba `web/index.html` según desde qué carpeta se ejecutaba `python app.py`. | La ruta de `web/` se calcula a partir de la ubicación de `app.py` con `os.path.abspath(__file__)`. |
| 2 | PyMySQL devuelve el campo `TIME` como `timedelta`, que Flask no puede convertir a JSON ni mostrar como `HH:MM`. | La función `_hora()` de `ruta_dao.py` lo convierte a texto `HH:MM`. |
| 3 | Una ruta y sus paradas podían quedar a medias si fallaba un `INSERT`. | `RutaDAO.crear` guarda todo en **una transacción** con `commit` y `rollback` ante error. |
| 4 | Flask no leía los datos que enviaba el navegador en los formularios. | `app.js` envía `application/x-www-form-urlencoded` (`enviarFormulario`) y Flask lo lee con `request.form`. |
| 5 | Texto escrito por el usuario podía inyectar HTML en la página (XSS). | Todo texto dinámico pasa por `esc()` antes de insertarse con `innerHTML`. |
| 6 | Si MySQL estaba apagado, la API devolvía una página de error HTML y el JavaScript fallaba sin explicación. | Un `errorhandler` devuelve `{"error": "..."}` en JSON y el frontend lo muestra; además `app.py` avisa al arrancar si no hay conexión. |
| 7 | Al comenzar a versionar, la carpeta `.venv` (cientos de archivos) estaba dentro del proyecto. | Se creó `.gitignore` y cada integrante crea su propio entorno virtual. |
| 8 | Quedaban textos de una versión anterior en Java ("API Java", pie de página). | Se corrigieron para reflejar el stack actual (Python + Flask). |

> ✏️ **Equipo:** esta tabla se redactó a partir de decisiones que ya están en el código. Agreguen o ajusten
> filas con los problemas reales que enfrentaron durante el desarrollo.

## 7. Flujo de trabajo con Git

- Rama estable: `main`. Los cambios nuevos se hacen en ramas `feature/<nombre>` y entran por **Pull Request**
  revisado por un compañero (plantilla en `.github/pull_request_template.md`).
- Mensajes de commit en español con prefijo: `feat`, `fix`, `docs`, `test`, `chore`.
- La bitácora de commits está en [`docs/BITACORA_COMMITS.md`](docs/BITACORA_COMMITS.md).
- Guía paso a paso para GitHub web y Pull Request: [`docs/GUIA_GITHUB_Y_PULL_REQUEST.md`](docs/GUIA_GITHUB_Y_PULL_REQUEST.md).
