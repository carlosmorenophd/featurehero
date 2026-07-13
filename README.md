# Feature Hero

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

### Desde el repositorio local

```bash
python -m venv .venv
source .venv/bin/activate
pip install .
```

En Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install .
```

### Desde GitHub

Instalacion directa desde la rama principal:

```bash
pip install git+https://github.com/<OWNER>/<REPO>.git
```

Instalacion desde un tag:

```bash
pip install git+https://github.com/<OWNER>/<REPO>.git@2026.07.01
pip install git+https://github.com/<OWNER>/<REPO>.git@release/2026.07.01
```

### Para desarrollo con Poetry

```bash
poetry install
poetry run featurehero --help
```

## Comandos Disponibles

```bash
featurehero run
featurehero transform
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

Se ejecuta solo al publicar tags con alguno de estos patrones:

- `YYYY.MM.DD`, por ejemplo `2026.07.01`
- `release/YYYY.MM.DD`, por ejemplo `release/2026.07.01`

Ejemplo:

```bash
git tag 2026.07.01
git push origin 2026.07.01
```

Tambien puede publicarse con namespace `release/`:

```bash
git tag release/2026.07.01
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

El wheel generado puede instalarse con:

```bash
pip install featurehero-<version>-py3-none-any.whl
```

## Documentacion para IA

El archivo [IA_ARCHITECTURE.md](IA_ARCHITECTURE.md) contiene el contexto tecnico para
agentes IA y personas que mantengan el proyecto. `DEVELOPMENT.md` fue sustituido
por ese documento.

## Licencia

MIT. Ver [LICENSE](LICENSE).
