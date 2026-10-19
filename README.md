# PedidoFácil

Aplicación web para gestionar **productos** y **pedidos**, desarrollada con Django y Python.
Base de datos PostgreSQL en Neon y despliegue en Render.

## Funcionalidades

- Inicio y cierre de sesión con el sistema de autenticación de Django.
- Páginas protegidas: sin sesión se redirige al formulario de login.
- CRUD de productos (nombre, descripción, precio, cantidad disponible, fecha de registro).
- CRUD de pedidos (número único, cliente, descripción, valor total, estado y usuario que lo registró) y cambio de estado.
- Búsqueda por nombre de producto, y por cliente o número de pedido.
- Validaciones con JavaScript (cliente) y con Django (servidor), respaldadas por restricciones en la base de datos.
- Interfaz con Bootstrap, adaptable a computador y móvil, con confirmación antes de eliminar.

## Estructura

```
config/      configuración del proyecto (settings, urls, wsgi)
cuentas/     inicio y cierre de sesión
productos/   modelo, formularios, vistas y urls de productos
pedidos/     modelo, formularios, vistas y urls de pedidos
templates/   plantillas HTML (Bootstrap)
static/      CSS y JavaScript (validaciones.js)
```

## Instalación local

```bash
git clone <URL-DE-TU-REPOSITORIO>
cd pedidofacil
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # Windows: copy .env.example .env
```

Edita `.env` y completa `SECRET_KEY` y `DATABASE_URL` (cadena de conexión de Neon).

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py cargar_demo      # opcional: datos de ejemplo
python manage.py runserver
```

Abre http://127.0.0.1:8000/ e inicia sesión con el usuario creado.

## Variables de entorno

| Variable | Descripción |
|---|---|
| `SECRET_KEY` | Clave secreta de Django |
| `DEBUG` | `True` en local, `False` en producción |
| `DATABASE_URL` | Cadena de conexión PostgreSQL de Neon |
| `ALLOWED_HOSTS` | Hosts permitidos separados por coma (en Render se agrega solo) |

Las credenciales nunca se suben a GitHub: `.env` está en `.gitignore`.

## Pruebas

```bash
python manage.py test
```

## Despliegue en Render

1. Sube el proyecto a GitHub.
2. En Render: **New > Web Service**, conecta el repositorio.
3. Configura:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn config.wsgi:application`
4. En **Environment** agrega: `SECRET_KEY`, `DEBUG=False`, `DATABASE_URL` (la de Neon) y `PYTHON_VERSION=3.12.8`.
5. Despliega y abre la URL pública. Crea el usuario administrador desde la consola (Shell) de Render con `python manage.py createsuperuser`.

## Validaciones

- **JavaScript** (`static/js/validaciones.js`): mensajes por campo, marcado visual, bloqueo del envío con errores y revalidación al corregir.
- **Django** (`forms.py` y modelos): se repiten las reglas en el servidor, incluida la unicidad del número de pedido y las opciones de estado.
- **Base de datos**: `UNIQUE` en `numero_pedido` y `CHECK` en precio, valor total y estado.
