# Feature Hero

> **Español** | [English](#english)
>
> Guía bilingüe de instalación y uso: [Español](INSTALLATION_GUIDE.md#espanol)
> | [English](INSTALLATION_GUIDE.md#english)

## Índice — Español

- [Características](#caracteristicas)
- [Requisitos e instalación](#requisitos)
- [Comandos disponibles](#comandos-disponibles)
- [Transformación de datos](#transformacion-de-datos)
- [Optimización](#optimizacion)
- [Análisis de resultados](#analisis-de-resultados)
- [Jobs](#jobs)
- [Versión](#version)
- [Artefactos de optimización](#artefactos-de-optimizacion)
- [Desarrollo](#desarrollo)
- [Release en GitHub](#release-en-github)
- [Referencia técnica](#referencia-tecnica)
- [Guía de instalación y uso](INSTALLATION_GUIDE.md#espanol)

## English Index

- [Features](#english-features)
- [Requirements and installation](#english-requirements)
- [Available commands](#english-available-commands)
- [Data transformation](#english-data-transformation)
- [Optimization](#english-optimization)
- [Result analysis](#english-result-analysis)
- [Jobs](#english-jobs)
- [Version](#english-version)
- [Optimization artifacts](#english-optimization-artifacts)
- [Development](#english-development)
- [GitHub release](#english-github-release)
- [Technical reference](#english-technical-reference)
- [Installation and usage guide](INSTALLATION_GUIDE.md#english)

`Feature Hero` es una herramienta de linea de comandos para preparar datos
tabulares y ejecutar seleccion de variables mediante un algoritmo genetico sobre
modelos de regresion.

El paquete instala el comando:

```bash
featurehero
```

## Caracteristicas

- Transformacion de columnas de fecha, categorias y variables numericas.
- Validacion del dataset antes de ejecutar optimizacion.
- Seleccion de variables mediante algoritmo genetico.
- Evaluacion de modelos de regresion con metricas de error y ajuste.
- Ejecucion en foreground o background.
- Exportacion de resultados, graficas, mejor modelo y mejores features.
- Empaquetado con Poetry y release automatico en GitHub Actions.

## Requisitos

- Python `>=3.12,<4.0`
- Poetry para desarrollo local

Dependencias principales:

- `pandas`
- `numpy`
- `scikit-learn`
- `xgboost`
- `matplotlib`
- `seaborn`
- `numbers-parser`
- `psutil`

## Instalacion

### Instalacion publica desde PyPI

Para usar Feature Hero sin descargar el repositorio:

```bash
python -m pip install featurehero
featurehero --help
featurehero version
```

La versión de Python compatible es `>=3.12,<4.0`. Consulta la [guía bilingüe de
instalación y uso](INSTALLATION_GUIDE.md#espanol) para instrucciones paso a paso
en Windows, macOS y Linux.

### Instalacion desde el repositorio para desarrollo

#### Desde el repositorio local

En macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
```

En Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install .
```

En Windows CMD:

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install .
```

#### Desde GitHub

Instalacion directa desde la rama principal:

```bash
python -m pip install git+https://github.com/carlosmorenophd/featurehero.git
```

Instalacion desde un tag o rama de release:

```bash
python -m pip install git+https://github.com/carlosmorenophd/featurehero.git@2026.07.01
python -m pip install git+https://github.com/carlosmorenophd/featurehero.git@release/2026.07.01
```

#### Para desarrollo con Poetry

```bash
poetry install
poetry run featurehero --help
```

## Comandos Disponibles

```bash
featurehero run
featurehero transform
featurehero analyze-results
featurehero jobs
featurehero version
```

Para ver la ayuda general:

```bash
featurehero --help
```

Para ver la ayuda de un comando especifico:

```bash
featurehero run --help
featurehero transform --help
featurehero analyze-results --help
featurehero jobs --help
```

Si se trabaja con Poetry:

```bash
poetry run featurehero run --help
```

## Transformacion de Datos

El comando `transform` genera un nuevo CSV con las transformaciones solicitadas.

Sintaxis:

```bash
featurehero transform --file <ruta> --type <tipo> --columns <col1> [<col2> ...] [--out <archivo.csv>]
```

Tipos soportados:

| Tipo | Descripcion |
| --- | --- |
| `date` | Expande una fecha en anio, mes, dia, dia de semana y dia del anio. |
| `date_seasonal` | Convierte fechas `MM/yyyy` en dummies de anio y mes. |
| `category` | Convierte categorias en codigos numericos. |
| `dummy` | Crea columnas one-hot/dummy para categorias. |
| `log1p` | Crea `<columna>_log1p` con `log(x + 1)`. |
| `sqrt` | Crea `<columna>_sqrt` con raiz cuadrada. |

Ejemplos:

```bash
featurehero transform --file data.csv --type date --columns order_date
featurehero transform --file data.csv --type date_seasonal --columns planting_month
featurehero transform --file data.csv --type category --columns product_type region --out processed.csv
featurehero transform --file data.csv --type dummy --columns product_type region --out processed.csv
featurehero transform --file data.csv --type log1p --columns "Farmers total land area (acres)"
featurehero transform --file data.csv --type sqrt --columns "Plant stand ; plot 1"
```

Reglas importantes:

- El archivo debe existir.
- Las columnas indicadas deben existir.
- `log1p` y `sqrt` conservan la columna original.
- `log1p` y `sqrt` preservan valores faltantes.
- `log1p` y `sqrt` fallan si encuentran valores negativos o no numericos.
- Si no se indica `--out`, la salida usa el sufijo `_transformed.csv`.

## Optimizacion

El comando `run` ejecuta el algoritmo genetico para seleccionar variables y
optimizar modelos de regresion.

Sintaxis:

```bash
featurehero run --file <archivo> --column <target>
```

Ejemplo:

```bash
featurehero run --file data/gold_price.csv --column "Adj Close"
```

Formatos soportados:

- `.csv`
- `.xls`
- `.xlsx`
- `.numbers`

Validaciones del dataset:

- La columna target debe existir.
- Las columnas predictoras deben ser numericas.
- Las columnas predictoras no deben ser texto ni fechas.
- La columna target debe ser numerica.
- Todos los valores del target deben ser mayores que `0`.

### Ejecucion en background

```bash
featurehero run --file data/prices.csv --column price --background
```

Cuando se usa `--background`, Feature Hero registra el proceso y escribe logs y
estado de avance junto al archivo de entrada.

### Parametros avanzados

`--params` recibe un objeto JSON.

```bash
featurehero run --file data.csv --column target --params '{"number_generation": 50, "number_population": 200}'
```

Parametros soportados:

| Parametro | Tipo | Descripcion |
| --- | --- | --- |
| `number_generation` | entero >= 10 | Numero de generaciones. |
| `number_population` | entero >= 10, multiplo de 10 | Tamano de poblacion. |
| `machines` | lista de strings | Modelos a evaluar. |
| `metric` | string | Metrica usada para ordenar resultados. |

Modelos validos:

- `lasso_regression`
- `extreme_gradient_boost_regression`
- `random_forest_regression`
- `support_vector_regression`
- `bayesian_prediction_regression`

Ejemplo con modelos y metrica:

```bash
featurehero run \
  --file data.csv \
  --column target \
  --params '{"number_generation": 30, "number_population": 80, "machines": ["random_forest_regression", "lasso_regression"], "metric": "r2_score"}'
```

Metricas comunes:

- `r2_score`
- `mean_absolute_error`
- `mean_squared_error`
- `mean_absolute_percentage_error`
- `accuracy_mape`

## Analisis de Resultados

El comando `analyze-results` procesa un CSV final producido por Feature Hero.
No vuelve a entrenar modelos y no modifica el archivo original. Tanto el path
del archivo como la carpeta de salida son obligatorios.

Ejemplo para un resultado:

```bash
featurehero analyze-results \
  --file optimization_original.csv \
  --output-dir analysis_results
```

La carpeta se crea si no existe. Si el path de salida existe como archivo, el
comando falla. Las salidas son:

- `feature_relevance.csv`: ranking global y componentes del score;
- `feature_relevance_by_model.csv`: ranking separado por modelo;
- `feature_cooccurrence.csv`: frecuencia conjunta y Jaccard;
- `analysis_summary.json`: configuración, cobertura y advertencias.

Opciones importantes:

| Opcion | Descripcion |
| --- | --- |
| `--file` | Path obligatorio del CSV final de Feature Hero. |
| `--output-dir` | Path obligatorio de la carpeta de resultados. |
| `--metric` | Columna numerica utilizada para ordenar individuos. |
| `--direction` | `auto`, `maximize` o `minimize`. |
| `--elite-fraction` | Proporcion de mejores individuos; por defecto `0.10`. |
| `--duplicates` | Tratamiento de duplicados: `keep`, `drop` o `error`. |
| `--weights` | Pesos del indice como objeto JSON. |

Cuando se usa `index_metric`, su direccion no puede inferirse del nombre y debe
indicarse expresamente:

```bash
featurehero analyze-results \
  --file optimization_original.csv \
  --output-dir analysis_results \
  --metric index_metric \
  --direction maximize
```

Ejemplo de pesos personalizados:

```bash
featurehero analyze-results \
  --file optimization_original.csv \
  --output-dir analysis_results \
  --weights '{"frequency": 0.25, "elite": 0.30, "weighted": 0.25, "stability": 0.20}'
```

El analizador exige que las primeras 18 columnas sean las columnas estándar del
resultado Feature Hero, en su orden original desde `machine_name` hasta
`accuracy_mape`, y requiere al menos dos columnas `feature_`. SHAP, permutation
importance e importancia nativa se marcan como no disponibles; el analizador no
inventa esos valores.

## Jobs

Listar jobs registrados:

```bash
featurehero jobs --list
```

Detener un job por PID:

```bash
featurehero jobs --stop <PID>
```

Los jobs se registran en:

```text
~/.featurehero/jobs.pids
```

## Version

```bash
featurehero version
```

## Artefactos de Optimizacion

Cada ejecucion de `run` crea un workspace junto al archivo original:

```text
work_space_featurehero/YYYYMMDD_HHMMSS/
```

Dentro pueden generarse:

- `original.csv`
- `optimization_original.csv`
- `optimization_overlap_original.csv`
- graficas `.png`
- `best_model_original.pkl`
- `best_features_original.pkl`
- archivos `.log` y `.status` cuando corre en background

## Desarrollo

Instalar dependencias:

```bash
poetry install
```

Validar sintaxis:

```bash
python3 -m compileall -q featurehero
```

Validar metadata:

```bash
poetry check
```

Ejecutar CLI:

```bash
poetry run featurehero --help
```

Construir paquete:

```bash
poetry build
```

La construccion genera:

```text
dist/featurehero-<version>.tar.gz
dist/featurehero-<version>-py3-none-any.whl
```

## Release en GitHub

El workflow de release esta en:

```text
.github/workflows/release.yml
```

Se ejecuta solo en dos casos:

- Al publicar un tag `YYYY.MM.DD`, por ejemplo `2026.07.01`.
- Al hacer push a una rama `release/YYYY.MM.DD`, por ejemplo `release/2026.07.01`.

Ejemplo:

```bash
git tag 2026.07.01
git push origin 2026.07.01
```

Tambien puede publicarse desde una rama `release/`:

```bash
git checkout -b release/2026.07.01
git push origin release/2026.07.01
```

El workflow:

- instala Python 3.12
- instala Poetry
- instala dependencias
- ejecuta validaciones
- construye wheel y source distribution
- sube los artefactos
- crea un GitHub Release con `dist/*.whl` y `dist/*.tar.gz`

Cuando el workflow se ejecuta desde una rama `release/YYYY.MM.DD`, el release
usa ese mismo nombre como `tag_name` y apunta al commit que disparo el workflow.

El wheel generado puede instalarse con:

```bash
pip install featurehero-<version>-py3-none-any.whl
```

## Referencia tecnica

Esta sección consolida el contexto técnico necesario para mantener la aplicación.
La fuente de verdad es el código ejecutable y las pruebas existentes.

### Estructura y flujo

```text
featurehero/main.py
  -> prepara argumentos y despacha comandos
  -> worker.pip_worker.genetic_algorithm()
  -> services.optimizations.optimization_run_from_task()
  -> GeneticAlgorithm.run() y GeneticAlgorithm.export()
```

Componentes principales:

- `featurehero/core/files/`: lectura, validación, transformación y preparación
  de datasets.
- `featurehero/core/metrics/`: cálculo y enumeración de métricas de regresión.
- `featurehero/core/job_manager.py`: registro, listado y detención de trabajos
  en segundo plano.
- `featurehero/services/machines/`: construcción de modelos y mutación de
  hiperparámetros.
- `featurehero/services/optimizations/`: algoritmo genético y selección de
  variables.
- `featurehero/services/results/result_analyzer.py`: análisis posterior de CSV
  finales sin reentrenar modelos.
- `tests/test_result_analyzer.py`: pruebas del contrato y resultados del análisis.

### Contrato de optimización

`run` acepta `.csv`, `.xls`, `.xlsx` y `.numbers`. Excel y Numbers deben tener
una sola hoja. La columna objetivo debe existir, ser numérica y contener valores
mayores que cero; las columnas predictoras no pueden ser texto ni fechas.

El algoritmo genético crea poblaciones, selecciona variables mediante cromosomas
booleanos, muta variables e hiperparámetros, cruza individuos, evalúa modelos,
ordena por la métrica seleccionada y exporta los resultados. Los modelos
disponibles son:

- `lasso_regression`
- `extreme_gradient_boost_regression`
- `random_forest_regression`
- `support_vector_regression`
- `bayesian_prediction_regression`

`number_generation` debe ser un entero mayor o igual a 10. `number_population`
debe ser un entero mayor o igual a 10 y múltiplo de 10. La métrica por defecto
es `r2_score`. El sistema calcula scores D2, varianza explicada, errores
absolutos, porcentuales, cuadrados, logarítmicos, desviancias, error máximo,
mediana, raíz del error cuadrático y `accuracy_mape`.

### Transformaciones y jobs

`transform` soporta `date`, `date_seasonal`, `category`, `dummy`, `log1p` y
`sqrt`. La salida siempre es CSV; `log1p` y `sqrt` preservan la columna original,
valores faltantes y rechazan valores negativos o no numéricos.

Los trabajos en segundo plano se registran en `~/.featurehero/jobs.pids`.
`run --background` crea archivos `.log` y `.status`; `jobs --list` elimina
registros cuyo PID ya no existe y `jobs --stop PID` termina el proceso registrado.

### Contrato de análisis de resultados

`analyze-results` recibe un CSV final y una carpeta de salida. Exige las 18
columnas estándar desde `machine_name` hasta `accuracy_mape` en orden y al menos
dos columnas con prefijo `feature_`. No modifica el archivo original ni vuelve a
entrenar modelos.

Genera:

- `feature_relevance.csv`: selección global, élite, ponderación y ranking.
- `feature_relevance_by_model.csv`: el mismo análisis separado por modelo.
- `feature_cooccurrence.csv`: frecuencia conjunta y similitud de Jaccard.
- `analysis_summary.json`: configuración, métricas, modelos, advertencias y
  componentes disponibles.

El analizador valida booleanos, métrica de ranking, dirección, features
compatibles, duplicados y carpeta de salida. SHAP, permutation importance,
importancia nativa y estabilidad entre ejecuciones se informan como no
disponibles cuando no existen en los datos; no se inventan valores.

### Archivos generados, pruebas y límites

Cada ejecución de optimización crea un workspace con el CSV normalizado, CSV de
resultados, gráficas, archivos serializados del mejor modelo y mejores variables,
y logs/status cuando corresponde. `dist/`, workspaces, logs y cachés son artefactos
generados, no fuente del proyecto.

La validación local recomendada es:

```bash
python3 -m compileall -q featurehero
poetry check
poetry run pytest -q
poetry run featurehero --help
poetry run featurehero version
```

Las pruebas actuales cubren el analizador de resultados: clasificación de
columnas, booleanos, dirección de métricas, relevancia, duplicados, exportación,
validación de salida y preservación del archivo original. No existe una suite
completa de extremo a extremo para todo el algoritmo genético.

El paquete es una herramienta para desarrolladores y personas con conocimientos
de datos; no es una aplicación orientada a usuarios finales. No se debe cambiar
la interfaz CLI, la división de datos, el algoritmo genético ni los modelos sin
una especificación explícita.

## Licencia

MIT. Ver [LICENSE](LICENSE).

---

<a id="english"></a>

# Feature Hero — English

[Español](#feature-hero) | **English**

Feature Hero is a command-line tool for preparing tabular data and selecting
variables through a genetic algorithm over regression models.

The package installs the following command:

```bash
featurehero
```

### English Features

- Transform date, categorical, and numeric columns.
- Validate datasets before optimization.
- Select variables with a genetic algorithm.
- Evaluate regression models with error and fit metrics.
- Run jobs in the foreground or background.
- Export results, charts, the best model, and the best features.
- Build packages with Poetry and publish releases through GitHub Actions.

### English Requirements

- Python `>=3.12,<4.0`.
- Poetry for local development only.

Main dependencies:

- `pandas`
- `numpy`
- `scikit-learn`
- `xgboost`
- `matplotlib`
- `seaborn`
- `numbers-parser`
- `psutil`

### English Installation

### Public installation from PyPI

To use Feature Hero without downloading the repository:

```bash
python -m pip install featurehero
featurehero --help
featurehero version
```

The supported Python range is `>=3.12,<4.0`. See the [bilingual installation
and usage guide](INSTALLATION_GUIDE.md#english) for step-by-step instructions
for Windows, macOS, and Linux.

### Repository installation for development

#### From the local repository

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
```

On Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install .
```

On Windows CMD:

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install .
```

#### From GitHub

Direct installation from the main branch:

```bash
python -m pip install git+https://github.com/carlosmorenophd/featurehero.git
```

Installation from a release tag or branch:

```bash
python -m pip install git+https://github.com/carlosmorenophd/featurehero.git@2026.07.01
python -m pip install git+https://github.com/carlosmorenophd/featurehero.git@release/2026.07.01
```

#### Development with Poetry

```bash
poetry install
poetry run featurehero --help
```

### English Available Commands

```bash
featurehero run
featurehero transform
featurehero analyze-results
featurehero jobs
featurehero version
```

For general help:

```bash
featurehero --help
```

For command-specific help:

```bash
featurehero run --help
featurehero transform --help
featurehero analyze-results --help
featurehero jobs --help
```

When using Poetry:

```bash
poetry run featurehero run --help
```

### English Data Transformation

The `transform` command creates a new CSV with the requested transformations.

Syntax:

```bash
featurehero transform --file <path> --type <type> --columns <col1> [<col2> ...] [--out <file.csv>]
```

Supported types:

| Type | Description |
| --- | --- |
| `date` | Expands a date into year, month, day, weekday, and day of year. |
| `date_seasonal` | Converts `MM/yyyy` dates into year and month dummies. |
| `category` | Converts categories into numeric codes. |
| `dummy` | Creates one-hot/dummy columns for categories. |
| `log1p` | Creates `<column>_log1p` with `log(x + 1)`. |
| `sqrt` | Creates `<column>_sqrt` with the square root. |

Examples:

```bash
featurehero transform --file data.csv --type date --columns order_date
featurehero transform --file data.csv --type date_seasonal --columns planting_month
featurehero transform --file data.csv --type category --columns product_type region --out processed.csv
featurehero transform --file data.csv --type dummy --columns product_type region --out processed.csv
featurehero transform --file data.csv --type log1p --columns "Farmers total land area (acres)"
featurehero transform --file data.csv --type sqrt --columns "Plant stand ; plot 1"
```

Important rules:

- The file must exist.
- The specified columns must exist.
- `log1p` and `sqrt` preserve the original column.
- `log1p` and `sqrt` preserve missing values.
- `log1p` and `sqrt` fail when negative or non-numeric values are found.
- When `--out` is omitted, the output uses the `_transformed.csv` suffix.

### English Optimization

The `run` command executes the genetic algorithm to select variables and optimize
regression models.

Syntax:

```bash
featurehero run --file <file> --column <target>
```

Example:

```bash
featurehero run --file data/gold_price.csv --column "Adj Close"
```

Supported formats:

- `.csv`
- `.xls`
- `.xlsx`
- `.numbers`

Dataset validation:

- The target column must exist.
- Predictor columns must be numeric.
- Predictor columns must not be text or dates.
- The target column must be numeric.
- All target values must be greater than `0`.

#### Background execution

```bash
featurehero run --file data/prices.csv --column price --background
```

With `--background`, Feature Hero registers the process and writes logs and
progress status next to the input file.

#### Advanced parameters

`--params` receives a JSON object.

```bash
featurehero run --file data.csv --column target --params '{"number_generation": 50, "number_population": 200}'
```

Supported parameters:

| Parameter | Type | Description |
| --- | --- | --- |
| `number_generation` | integer >= 10 | Number of generations. |
| `number_population` | integer >= 10, multiple of 10 | Population size. |
| `machines` | list of strings | Models to evaluate. |
| `metric` | string | Metric used to order results. |

Valid models:

- `lasso_regression`
- `extreme_gradient_boost_regression`
- `random_forest_regression`
- `support_vector_regression`
- `bayesian_prediction_regression`

Example with models and a metric:

```bash
featurehero run \
  --file data.csv \
  --column target \
  --params '{"number_generation": 30, "number_population": 80, "machines": ["random_forest_regression", "lasso_regression"], "metric": "r2_score"}'
```

Common metrics:

- `r2_score`
- `mean_absolute_error`
- `mean_squared_error`
- `mean_absolute_percentage_error`
- `accuracy_mape`

### English Result Analysis

The `analyze-results` command processes a final CSV produced by Feature Hero. It
does not retrain models or modify the original file. Both the input path and the
output directory are required.

Example:

```bash
featurehero analyze-results \
  --file optimization_original.csv \
  --output-dir analysis_results
```

The directory is created if it does not exist. If the output path is an existing
file, the command fails. Outputs include:

- `feature_relevance.csv`: global ranking and score components.
- `feature_relevance_by_model.csv`: ranking separated by model.
- `feature_cooccurrence.csv`: joint frequency and Jaccard similarity.
- `analysis_summary.json`: configuration, coverage, and warnings.

Important options:

| Option | Description |
| --- | --- |
| `--file` | Required path to the final Feature Hero CSV. |
| `--output-dir` | Required output directory path. |
| `--metric` | Numeric column used to order individuals. |
| `--direction` | `auto`, `maximize`, or `minimize`. |
| `--elite-fraction` | Proportion of the best individuals; default `0.10`. |
| `--duplicates` | Duplicate policy: `keep`, `drop`, or `error`. |
| `--weights` | Index weights as a JSON object. |

When using `index_metric`, its direction cannot be inferred from the name and
must be specified explicitly:

```bash
featurehero analyze-results \
  --file optimization_original.csv \
  --output-dir analysis_results \
  --metric index_metric \
  --direction maximize
```

Example with custom weights:

```bash
featurehero analyze-results \
  --file optimization_original.csv \
  --output-dir analysis_results \
  --weights '{"frequency": 0.25, "elite": 0.30, "weighted": 0.25, "stability": 0.20}'
```

The analyzer requires the first 18 columns to be the standard Feature Hero result
columns, in their original order from `machine_name` through `accuracy_mape`, and
requires at least two `feature_` columns. SHAP, permutation importance, and native
importance are marked unavailable; the analyzer does not invent those values.

### English Jobs

List registered jobs:

```bash
featurehero jobs --list
```

Stop a job by PID:

```bash
featurehero jobs --stop <PID>
```

Jobs are registered in:

```text
~/.featurehero/jobs.pids
```

### English Version

```bash
featurehero version
```

### English Optimization Artifacts

Each `run` execution creates a workspace next to the original file:

```text
work_space_featurehero/YYYYMMDD_HHMMSS/
```

It may contain:

- `original.csv`
- `optimization_original.csv`
- `optimization_overlap_original.csv`
- `.png` charts
- `best_model_original.pkl`
- `best_features_original.pkl`
- `.log` and `.status` files for background execution

### English Development

Install dependencies:

```bash
poetry install
```

Validate syntax:

```bash
python3 -m compileall -q featurehero
```

Validate metadata:

```bash
poetry check
```

Run the CLI:

```bash
poetry run featurehero --help
```

Build the package:

```bash
poetry build
```

The build creates:

```text
dist/featurehero-<version>.tar.gz
dist/featurehero-<version>-py3-none-any.whl
```

### English GitHub Release

The release workflow is located at:

```text
.github/workflows/release.yml
```

It runs in two cases:

- When a `YYYY.MM.DD` tag is published, such as `2026.07.01`.
- When code is pushed to a `release/YYYY.MM.DD` branch, such as `release/2026.07.01`.

Example:

```bash
git tag 2026.07.01
git push origin 2026.07.01
```

It can also be published from a `release/` branch:

```bash
git checkout -b release/2026.07.01
git push origin release/2026.07.01
```

The workflow:

- installs Python 3.12;
- installs Poetry;
- installs dependencies;
- runs validations;
- builds a wheel and source distribution;
- uploads the artifacts; and
- creates a GitHub Release with `dist/*.whl` and `dist/*.tar.gz`.

When the workflow runs from a `release/YYYY.MM.DD` branch, the release uses the
same name as `tag_name` and points to the commit that triggered the workflow.

The generated wheel can be installed with:

```bash
python -m pip install featurehero-<version>-py3-none-any.whl
```

### English Technical Reference

This section consolidates the technical context needed to maintain the application.
Executable code and existing tests are the source of truth.

#### Structure and flow

```text
featurehero/main.py
  -> prepares arguments and dispatches commands
  -> worker.pip_worker.genetic_algorithm()
  -> services.optimizations.optimization_run_from_task()
  -> GeneticAlgorithm.run() and GeneticAlgorithm.export()
```

Main components:

- `featurehero/core/files/`: dataset reading, validation, transformation, and preparation.
- `featurehero/core/metrics/`: regression metric calculation and enumeration.
- `featurehero/core/job_manager.py`: background job registration, listing, and stopping.
- `featurehero/services/machines/`: model construction and hyperparameter mutation.
- `featurehero/services/optimizations/`: genetic algorithm and variable selection.
- `featurehero/services/results/result_analyzer.py`: post-processing of final CSVs without retraining.
- `tests/test_result_analyzer.py`: analyzer contract and result tests.

#### Optimization contract

`run` accepts `.csv`, `.xls`, `.xlsx`, and `.numbers`. Excel and Numbers files
must contain one sheet. The target column must exist, be numeric, and contain
values greater than zero; predictor columns must not be text or dates.

The genetic algorithm creates populations, selects variables through boolean
chromosomes, mutates variables and hyperparameters, crosses individuals, evaluates
models, orders them by the selected metric, and exports results. Available models are:

- `lasso_regression`
- `extreme_gradient_boost_regression`
- `random_forest_regression`
- `support_vector_regression`
- `bayesian_prediction_regression`

`number_generation` must be an integer greater than or equal to 10.
`number_population` must be an integer greater than or equal to 10 and a multiple
of 10. The default metric is `r2_score`.

#### Transformations and jobs

`transform` supports `date`, `date_seasonal`, `category`, `dummy`, `log1p`, and
`sqrt`. Output is always CSV; `log1p` and `sqrt` preserve the original column and
missing values and reject negative or non-numeric values.

Background jobs are registered in `~/.featurehero/jobs.pids`.
`run --background` creates `.log` and `.status` files; `jobs --list` removes
records whose PID no longer exists, and `jobs --stop PID` terminates a registered process.

#### Result analysis contract

`analyze-results` receives a final CSV and an output directory. It requires the 18
standard columns from `machine_name` through `accuracy_mape` in order and at least
two columns prefixed with `feature_`. It does not modify the original file or retrain models.

It generates:

- `feature_relevance.csv`: global, elite, weighted, and ranking analysis.
- `feature_relevance_by_model.csv`: the same analysis separated by model.
- `feature_cooccurrence.csv`: joint frequency and Jaccard similarity.
- `analysis_summary.json`: configuration, metrics, models, warnings, and available components.

The analyzer validates booleans, ranking metrics, direction, compatible features,
duplicates, and the output directory. SHAP, permutation importance, native
importance, and cross-run stability are reported unavailable when absent; values
are not invented.

#### Generated files, tests, and limits

Each optimization run creates a workspace with the normalized CSV, result CSVs,
charts, serialized best model and best variables, and logs/status when applicable.
`dist/`, workspaces, logs, and caches are generated artifacts, not project source.

Recommended local validation:

```bash
python3 -m compileall -q featurehero
poetry check
poetry run pytest -q
poetry run featurehero --help
poetry run featurehero version
```

Current tests cover result analyzer classification, booleans, metric direction,
relevance, duplicates, export, output validation, and original-file preservation.
There is no complete end-to-end suite for the entire genetic algorithm and job flow.

The package is a tool for developers and people with data knowledge; it is not an
end-user application. Do not change the CLI interface, data split, genetic algorithm,
or models without an explicit specification.

## English License

MIT. See [LICENSE](LICENSE).
