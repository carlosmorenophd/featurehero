# Feature Hero

## 1. Installation and Usage

### 1.1. Installation

#### With Poetry (recommended for development)

1.  **Install Python 3.12**: Make sure you have Python 3.12 or a compatible version installed on your system. You can download it from the official Python website.

2.  **Install Poetry**: Poetry is a tool for dependency management and packaging in Python. If you don't have it installed, you can follow the instructions on the official Poetry website. A common way to install it is:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3.  **Set up the project environment**: Once you have cloned the repository, navigate to the project's root directory and run the following command to install all dependencies in a virtual environment managed by Poetry:
    ```bash
    poetry install
    ```
    This command will read the `pyproject.toml` file, resolve the dependencies, and install them.

#### With pip (for end-users from source code)

If you prefer not to use Poetry to run the application, you can install it in a standard Python virtual environment:

1.  **Create and activate a virtual environment (optional but recommended)**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate # On Linux/macOS
    # .venv\Scripts\activate # On Windows
    ```
2.  **Install the package**: From the project root:
    ```bash
    pip install .
    ```

### 1.2. Application Usage

Once the project is installed (either with Poetry or pip), you can run the `featurehero` commands. If you use Poetry, prefix the commands with `poetry run`.

If you make changes to `pyproject.toml` (like updating the version or adding dependencies), run `poetry install` (or `pip install .` if using pip) again to update the environment.

#### `run`: Execute the genetic algorithm

Runs the optimization algorithm for feature selection and the machine learning model.

```bash
poetry run featurehero run --file <path_to_file> --column <target_column>
```

**Ejemplo:**
```bash
poetry run featurehero run --file '/home/yeiden/Documents/athenaFTP/PrecioOro/precio_oro.csv' --column 'Adj Close'
```

#### `transform`: Transformar datos

Preprocesses your data, converting date columns into multiple features or performing label encoding for categorical columns.

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

Display the currente version of the application.

```bash
poetry run featurehero version
```

#### `help`: Mostrar ayuda

Display the general help and common commands.
```bash
poetry run featurehero help
```
To get information from spseficic command you can run 
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

### 2.2. Building the Package

To build the distribution packages (sdist and wheel) that can be published or installed with `pip`:

```bash
poetry build
```
Los archivos generados se encontrarán en el directorio `dist/`.

### 2.3. Consideraciones al Modificar el Código

*   **Code Formatting**: It is recommended to follow Python's style conventions (PEP 8). Consider using tools like `black` for automatic formatting and `pylint` or `flake8` for static code analysis.
*   **Updating Dependencies**: If you add or modify dependencies, use `poetry add <package>` or `poetry update` to manage the `pyproject.toml` and `poetry.lock` files.
*   **Updating the Version**: If you change the version in `pyproject.toml`, remember that `poetry install` will update the virtual environment to reflect the new version.


