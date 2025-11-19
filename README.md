# Feature Hero

## 1. Instalación y Uso

### 1.1. Instalación

#### Con Poetry (recomendado para desarrollo)

1.  **Instalar Python 3.12**: Asegúrate de tener Python 3.12 o una versión compatible instalada en tu sistema. Puedes descargarlo desde el sitio web oficial de Python.

2.  **Instalar Poetry**: Poetry es una herramienta para la gestión de dependencias y empaquetado en Python. Si no lo tienes instalado, puedes seguir las instrucciones en el sitio web oficial de Poetry. Una forma común de instalarlo es:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3.  **Configurar el entorno del proyecto**: Una vez que hayas clonado el repositorio, navega al directorio raíz del proyecto y ejecuta el siguiente comando para instalar todas las dependencias en un entorno virtual gestionado por Poetry:
    ```bash
    poetry install
    ```
    Este comando leerá el archivo `pyproject.toml`, resolverá las dependencias y las instalará.

#### Con pip (para usuarios finales desde el código fuente)

Si prefieres no usar Poetry para ejecutar la aplicación, puedes instalarla en un entorno virtual estándar de Python:

1.  **Crear y activar un entorno virtual (opcional pero recomendado)**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate # En Linux/macOS
    # .venv\Scripts\activate # En Windows
    ```
2.  **Instalar el paquete**: Desde la raíz del proyecto:
    ```bash
    pip install .
    ```

### 1.2. Uso de la Aplicación

Una vez instalado el proyecto (ya sea con Poetry o pip), puedes ejecutar los comandos de `featurehero`. Si usas Poetry, prefija los comandos con `poetry run`.

Si realizas cambios en `pyproject.toml` (como actualizar la versión o añadir dependencias), ejecuta `poetry install` (o `pip install .` si usas pip) de nuevo para actualizar el entorno.

#### `run`: Ejecutar el algoritmo genético

Ejecuta el algoritmo de optimización para la selección de variables y el modelo de machine learning.

```bash
poetry run featurehero run --file <ruta_al_archivo> --column <columna_objetivo>
```

**Ejemplo:**
```bash
poetry run featurehero run --file '/home/yeiden/Documents/athenaFTP/PrecioOro/precio_oro.csv' --column 'Adj Close'
```

#### `transform`: Transformar datos

Preprocesa tus datos, convirtiendo columnas de fecha en múltiples características o realizando codificación de etiquetas (label encoding) para columnas categóricas.

**Sintaxis:**
```bash
poetry run featurehero transform --file <ruta> --type <tipo> --columns <col1> [<col2> ...] [--out <nombre_archivo>]
```

*   `--type`: Puede ser `date` o `category`.
*   `--columns`: Una lista de columnas a transformar, separadas por espacios.
*   `--out`: (Opcional) El nombre para el archivo CSV de salida. Si no se proporciona, se creará un nuevo archivo con el sufijo `_transformed.csv` en el mismo directorio que el archivo de entrada.

**Ejemplos:**

```bash
# Transformar una columna de fecha
poetry run featurehero transform --file data.csv --type date --columns order_date

# Transformar múltiples columnas categóricas y guardar en un nuevo archivo
poetry run featurehero transform --file data.csv --type category --columns product_type region --out processed_data.csv
```

#### `version`: Mostrar la versión

Muestra la versión actual de la aplicación.

```bash
poetry run featurehero version
```

#### `help`: Mostrar ayuda

Muestra la ayuda general y los comandos disponibles.

```bash
poetry run featurehero help
```
Para obtener ayuda específica de un comando, puedes usar:
```bash
poetry run featurehero <comando> --help
# Ejemplo: poetry run featurehero run --help
```

## 2. Desarrollo y Modificación del Proyecto

Esta sección es para quienes desean contribuir o modificar el código fuente de `Feature Hero`.

### 2.1. Configuración del Entorno de Desarrollo

1.  **Clonar el repositorio**:
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd phen_ga_desktop # O el nombre de tu directorio
    ```
2.  **Instalar Python 3.12**: Asegúrate de tener Python 3.12 o una versión compatible.
3.  **Instalar Poetry**: Sigue las instrucciones en python-poetry.org.
4.  **Configurar el entorno del proyecto**: Desde la raíz del proyecto, ejecuta:
    ```bash
    poetry install --verbose
    ```
    Esto instalará todas las dependencias y el propio proyecto en modo editable, lo que te permitirá modificar el código y ver los cambios reflejados inmediatamente.

### 2.2. Construcción del Paquete

Para construir los paquetes de distribución (sdist y wheel) que pueden ser publicados o instalados con `pip`:

```bash
poetry build
```
Los archivos generados se encontrarán en el directorio `dist/`.

### 2.3. Consideraciones al Modificar el Código

*   **Formato de código**: Se recomienda seguir las convenciones de estilo de Python (PEP 8). Considera usar herramientas como `black` para el formateo automático y `pylint` o `flake8` para el análisis estático del código.
*   **Actualizar dependencias**: Si añades o modificas dependencias, usa `poetry add <paquete>` o `poetry update` para gestionar el archivo `pyproject.toml` y `poetry.lock`.
*   **Actualizar la versión**: Si cambias la versión en `pyproject.toml`, recuerda que `poetry install` actualizará el entorno virtual para reflejar la nueva versión.
