Aplicacion web sencilla en Python usando arquitectura web de n-capas.

El ejemplo usa un inventario de productos, parecido a un dominio e-commerce, pero reducido para que sea facil de entender, ejecutar y explicar.

La aplicacion permite registrar, listar, editar y eliminar productos. Cada producto tiene nombre, precio y stock.

## Estructura del proyecto

La carpeta principal que se abre en VS Code es `NCAPAS`. Dentro se encuentra el entorno virtual `.venv` y el proyecto `n_layer_store`.

```text
NCAPAS/
├── .venv/
└── n_layer_store/
    ├── app/
    │   ├── presentation/
    │   ├── business/
    │   ├── domain/
    │   ├── data/
    │   └── infrastructure/
    ├── instance/
    ├── tests/
    ├── .env
    ├── .gitignore
    ├── README.md
    ├── requirements.txt
    └── run.py
```

La carpeta `instance` es creada por Flask/SQLAlchemy para guardar archivos locales de la aplicacion. En este caso ahi puede almacenarse la base de datos SQLite.

## Capas

| Capa | Carpeta | Responsabilidad |
| --- | --- | --- |
| Presentacion | `app/presentation` | Rutas Flask, formularios HTML y respuestas al usuario. |
| Negocio | `app/business` | Reglas: validar nombre, precio y stock antes de guardar. |
| Dominio | `app/domain` | Entidad `Product`, independiente de Flask y de la base de datos. |
| Acceso a datos | `app/data` | Repositorio y modelo SQLAlchemy para consultar, crear, editar y eliminar productos. |
| Infraestructura | `app/infrastructure` | Configuracion de la conexion a la base de datos. |

## Por que es una arquitectura n-capas

Es una arquitectura n-capas porque el sistema esta dividido en partes con responsabilidades diferentes. La interfaz web no contiene las reglas de negocio ni accede directamente a la base de datos.

El flujo principal es:

```text
Usuario
  -> Capa de presentacion
  -> Capa de negocio
  -> Capa de acceso a datos
  -> Base de datos
```

Ejemplo dentro del proyecto:

1. El usuario llena el formulario de producto en la pagina web.
2. La ruta Flask en `app/presentation/routes.py` recibe los datos.
3. La clase `ProductService` en `app/business/product_service.py` valida las reglas de negocio.
4. La entidad `Product` en `app/domain/product.py` representa el producto del sistema.
5. El repositorio `SqlAlchemyProductRepository` en `app/data/product_repository.py` guarda o consulta los datos.
6. La configuracion de base de datos esta en `app/infrastructure/database.py`.

Gracias a esta separacion, si se cambia la interfaz o la base de datos, la logica principal del negocio puede mantenerse mas ordenada.

## Base de datos utilizada

Actualmente el proyecto usa SQLite para facilitar la ejecucion local.

La conexion se configura en el archivo `.env`:

```env
FLASK_SECRET_KEY=dev-secret-change-me
DATABASE_URL=sqlite:///n_layer_store.db
```

SQLite no requiere crear un servidor ni una base manualmente. Cuando se ejecuta la aplicacion, SQLAlchemy crea automaticamente la base de datos y la tabla `products` si todavia no existen.

Tambien se puede usar PostgreSQL cambiando la variable `DATABASE_URL`, pero para esta version de prueba local se usa SQLite.

## Requisitos

- Python 3.9+
- SQLite para correr localmente
- Visual Studio Code

## Inicializar el proyecto desde VS Code

Abre en VS Code la carpeta:

```text
C:\Users\Usuario\Documents\Carpeta\ncapas
```

Luego abre una terminal integrada.

Si el entorno virtual `.venv` ya existe, activalo:

```powershell
.\.venv\Scripts\activate
```

Si no existe, crealo y luego activalo:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Entra a la carpeta del proyecto:

```powershell
cd .\n_layer_store
```

Instala las dependencias:

```powershell
python -m pip install -r requirements.txt
```

Si no existe el archivo `.env`, crealo dentro de `n_layer_store` con este contenido:

```env
FLASK_SECRET_KEY=dev-secret-change-me
DATABASE_URL=sqlite:///n_layer_store.db
```

Ejecuta la aplicacion:

```powershell
python run.py
```

Abre en el navegador:

```text
http://localhost:5000
```





La aplicacion se inicia en `http://localhost:5000` y muestra el inventario de productos.
