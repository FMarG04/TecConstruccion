# N-Layer Store

Aplicacion web sencilla en Python usando arquitectura web de n-capas.

El ejemplo usa un inventario de productos, parecido a un dominio e-commerce, pero reducido para que sea facil de entender, ejecutar y explicar.

## Estructura del proyecto

```text
n_layer_store/
├── app/
│   ├── presentation/
│   ├── business/
│   ├── domain/
│   ├── data/
│   └── infrastructure/
├── tests/
├── .env.example
├── requirements.txt
├── README.md
└── run.py
```

## Capas

| Capa | Carpeta | Responsabilidad |
| --- | --- | --- |
| Presentacion | `app/presentation` | Rutas Flask, formularios HTML y respuestas al usuario. |
| Negocio | `app/business` | Reglas: validar nombre, precio y stock antes de guardar. |
| Dominio | `app/domain` | Entidad `Product`, independiente de Flask y de la base de datos. |
| Acceso a datos | `app/data` | Repositorio y modelo SQLAlchemy para consultar, crear, editar y eliminar productos. |
| Infraestructura | `app/infrastructure` | Configuracion de la conexion a la base de datos. |

## Requisitos

- Python 3.9+
- SQLite para correr localmente
- Visual Studio Code

## Ejecutar desde VS Code

Abre en VS Code la carpeta:

```text
C:\Users\Usuario\Documents\TecConstruccion\ncapas
```

Luego abre una terminal integrada y ejecuta:

```powershell
.\.venv\Scripts\activate
cd .\n_layer_store
python -m pip install -r requirements.txt
```

Si no existe el archivo `.env`, crealo dentro de `n_layer_store` con este contenido:

```env
FLASK_SECRET_KEY=dev-secret-change-me
DATABASE_URL=sqlite:///n_layer_store.db
```

Despues ejecuta:

```powershell
python run.py
```

Abre en el navegador:

```text
http://localhost:5000
```

La aplicacion crea automaticamente el archivo de base de datos SQLite y la tabla `products`.

## Probar la logica de negocio

Desde la carpeta `n_layer_store`:

```powershell
python -m unittest discover -s tests
```

## Flujo de la arquitectura

La ruta web no guarda directamente en la base de datos. Primero llama a un servicio de negocio, el servicio valida los datos, y luego usa un repositorio para persistirlos.

```text
Usuario -> Presentacion -> Negocio -> Acceso a datos -> Base de datos
```

## Usar PostgreSQL de forma opcional

Si quieres usar PostgreSQL en lugar de SQLite, cambia el valor de `DATABASE_URL` en `.env`:

```env
DATABASE_URL=postgresql+psycopg2://postgres:TU_PASSWORD@localhost:5432/n_layer_store
```

Tambien debes crear previamente la base de datos `n_layer_store` en pgAdmin o con `psql`.

## Errores comunes

Si aparece `ModuleNotFoundError: No module named 'dotenv'`, instala las dependencias dentro del entorno virtual:

```powershell
python -m pip install -r requirements.txt
```

Si aparece `Either 'SQLALCHEMY_DATABASE_URI' or 'SQLALCHEMY_BINDS' must be set`, revisa que el archivo `.env` exista y tenga la variable `DATABASE_URL`.

Si aparece `TemplateNotFound: products/index.html`, revisa que en `app/__init__.py` Flask este configurado con:

```python
app = Flask(
    __name__,
    template_folder="presentation/templates",
    static_folder="presentation/static",
)
```
