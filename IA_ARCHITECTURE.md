# IA_ARCHITECTURE.md

Este documento es el contexto operativo de `Feature Hero` para agentes IA y
personas que mantengan el proyecto. Su objetivo es reducir el tiempo de lectura
del repositorio, fijar invariantes del sistema y dejar claro que partes pueden
modificarse sin romper la CLI.

`README.md` es la documentacion para usuarios. Este archivo es documentacion
tecnica interna.

## 1. Resumen del Sistema

`Feature Hero` es un paquete Python que instala una CLI llamada `featurehero`.
La CLI prepara datos tabulares, transforma columnas y ejecuta un algoritmo
genetico para seleccionar variables y optimizar modelos de regresion.

Comandos publicos:

```bash
featurehero run
featurehero transform
featurehero jobs
featurehero version
```

No cambiar estos nombres ni sus parametros sin actualizar tambien README,
validaciones, pruebas manuales y este documento.

## 2. Metadata del Paquete

Archivo principal:

```text
pyproject.toml
```

El proyecto usa metadata PEP 621 en `[project]` y Poetry como backend:

```toml
[project]
name = "featurehero"
version = "2026.1.1"
requires-python = ">=3.12,<4.0"

[project.scripts]
featurehero = "featurehero.main:main"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

La API publica minima esta en:

```text
featurehero/__init__.py
```

Actualmente solo exporta:

```python
__version__
```

La version se toma desde la metadata instalada con `importlib.metadata`.

## 3. Stack

- Python `>=3.12,<4.0`
- Poetry / poetry-core
- `argparse` para la CLI
- `pandas` y `numpy` para datos
- `numbers-parser` para archivos `.numbers`
- `scikit-learn` y `xgboost` para modelos
- `matplotlib` y `seaborn` para graficas
- `psutil` para gestion de procesos en background

## 4. Estructura del Repositorio

```text
featurehero/
  __init__.py
  main.py
  config/
  core/
    files/
      access_file.py
      machine_file.py
      transform_file.py
      work_space_file.py
    metrics/
      metric.py
      metric_enums.py
    job_manager.py
    key_env.py
    result_genetic.py
  services/
    machines/
      machine.py
      machine_build.py
      machine_enums.py
    optimizations/
      optimization.py
      optimization_enum.py
      optimization_features.py
      optimization_genetic_algorithm.py
  worker/
    pip_worker.py
```

Archivos de documentacion y release:

```text
README.md
IA_ARCHITECTURE.md
LICENSE
.github/workflows/release.yml
```

`DEVELOPMENT.md` fue sustituido por `IA_ARCHITECTURE.md`.

## 5. Flujo de la CLI

Archivo:

```text
featurehero/main.py
```

Responsabilidades:

- crear el parser de `argparse`
- validar `--params`
- despachar comandos
- ejecutar foreground/background
- imprimir version
- llamar transformaciones y jobs

Flujo de `run`:

```text
main.py
  -> handle_run_action()
  -> run_worker() o run_worker_background()
  -> prepare_work_space_file()
  -> worker.pip_worker.genetic_algorithm()
  -> optimization_run_from_task()
  -> GeneticAlgorithm.run()
  -> GeneticAlgorithm.export()
```

Flujo de `transform`:

```text
main.py
  -> run_transform()
  -> transform_data()
```

Flujo de `jobs`:

```text
main.py
  -> handle_jobs_action()
  -> JobManager
```

## 6. Transformaciones

Archivo:

```text
featurehero/core/files/transform_file.py
```

Tipos soportados:

- `date`
- `date_seasonal`
- `category`
- `dummy`
- `log1p`
- `sqrt`

Reglas:

- La entrada debe existir.
- La extension se resuelve por `_read_file`.
- CSV y Excel estan soportados en transformaciones.
- Las columnas solicitadas deben existir.
- La salida siempre se guarda como CSV.
- Si `--out` no se define, se usa `<base>_transformed.csv`.
- `log1p` y `sqrt` agregan columnas y preservan la original.
- `log1p` y `sqrt` rechazan valores negativos y no numericos.

Si se agrega una transformacion:

- agregar funcion o rama en `transform_file.py`
- agregar el valor en `choices` de `main.py`
- documentar en `README.md`
- documentar en este archivo
- validar con un CSV pequeno

## 7. Preparacion del Dataset para Optimizacion

Archivo:

```text
featurehero/core/files/work_space_file.py
```

Funcion clave:

```python
prepare_work_space_file(file_path: str, target_column: str) -> tuple[str, str]
```

Extensiones soportadas para `run`:

- `.csv`
- `.xls`
- `.xlsx`
- `.numbers`

La funcion crea:

```text
work_space_featurehero/YYYYMMDD_HHMMSS/original.csv
```

Validaciones:

- `file_path` no puede estar vacio.
- El archivo debe existir.
- La extension debe estar permitida.
- Excel y Numbers deben tener una sola hoja.
- La columna target debe existir.
- Las features no pueden ser texto.
- Las features no pueden ser fecha.
- El target debe ser numerico.
- El target debe tener todos los valores `> 0`.

No relajar estas validaciones sin entender el impacto en metricas como Poisson,
Gamma y log error.

## 8. Datos para Modelos

Archivo:

```text
featurehero/core/files/machine_file.py
```

Clases importantes:

- `FileDataRegression`
- `TrainingData`
- `DatasetOptimizationData`
- `FileMachine`

Punto sensible:

```python
TrainingData.test_size = 0.8
```

Esto significa 80% test y 20% entrenamiento. Es atipico; no cambiarlo sin una
decision explicita.

`FileMachine.get_dataset()` aplica `train_test_split` y puede filtrar columnas
mediante un cromosoma booleano.

## 9. Modelos

Archivos:

```text
featurehero/services/machines/machine.py
featurehero/services/machines/machine_build.py
featurehero/services/machines/machine_enums.py
```

Modelos soportados por nombre publico:

- `lasso_regression`
- `extreme_gradient_boost_regression`
- `random_forest_regression`
- `support_vector_regression`
- `bayesian_prediction_regression`

Si se agrega un modelo:

- agregar clase en `machine.py`
- agregar enum en `machine_enums.py`
- agregar builder en `machine_build.py`
- actualizar validacion de `machines` en `main.py`
- actualizar `README.md`
- actualizar este archivo

## 10. Metricas

Archivos:

```text
featurehero/core/metrics/metric.py
featurehero/core/metrics/metric_enums.py
```

La clase `Metric` calcula todas las metricas disponibles al crearse.

Metrica por defecto del algoritmo genetico:

```text
r2_score
```

Ordenamiento actual:

- Mayor es mejor: `accuracy_mape`, `r2_score`
- Menor es mejor: `mean_absolute_error`, `mean_squared_error`

El ordenamiento se define en:

```text
featurehero/services/optimizations/optimization_genetic_algorithm.py
```

Si se agrega una metrica:

- agregar enum
- calcularla en `Metric`
- decidir si mayor o menor es mejor
- actualizar README y este archivo

## 11. Algoritmo Genetico

Archivo principal:

```text
featurehero/services/optimizations/optimization_genetic_algorithm.py
```

Clases clave:

- `GeneticIndividual`
- `LogGenetic`
- `GeneticAlgorithm`

Responsabilidades:

- crear poblacion inicial
- seleccionar features por cromosoma booleano
- mutar features e hiperparametros
- cruzar individuos
- evaluar modelos
- ordenar por metrica
- exportar resultados

No modificar esta logica durante tareas de documentacion, release o packaging.

## 12. Exportacion de Resultados

Durante `GeneticAlgorithm.export()` se generan archivos en el workspace:

- `optimization_original.csv`
- `optimization_overlap_original.csv`
- graficas `.png`
- `best_model_original.pkl`
- `best_features_original.pkl`

Las graficas se generan desde:

```text
featurehero/core/result_genetic.py
```

## 13. Jobs en Background

Archivo:

```text
featurehero/core/job_manager.py
```

Registro de jobs:

```text
~/.featurehero/jobs.pids
```

`run --background` relanza el proceso con:

```text
--run-as-daemon
```

El proceso daemon escribe log y status. `jobs --list` limpia entradas obsoletas
si el PID ya no existe.

## 14. Release y Distribucion

Workflow:

```text
.github/workflows/release.yml
```

Trigger:

```yaml
on:
  push:
    tags:
      - "[0-9][0-9][0-9][0-9].[0-9][0-9].[0-9][0-9]"
```

Los releases del proyecto usan tags sin prefijo `v`, con formato de fecha:

```text
YYYY.MM.DD
```

Ejemplo:

```text
2026.07.01
```

El workflow debe:

- usar `actions/checkout`
- usar `actions/setup-python` con Python 3.12
- instalar Poetry
- cachear pip y Poetry
- ejecutar `poetry install`
- ejecutar `python -m compileall -q featurehero`
- ejecutar `poetry check`
- ejecutar `poetry run featurehero --help`
- ejecutar `poetry build`
- subir `dist/*.whl` y `dist/*.tar.gz`
- crear un GitHub Release con esos archivos

No publicar en PyPI todavia. El workflow debe quedar preparado para agregar ese
paso en el futuro con `PYPI_API_TOKEN`.

## 15. Validacion Local Recomendada

Antes de cerrar cambios:

```bash
python3 -m compileall -q featurehero
poetry check
poetry install
poetry run featurehero --help
poetry run featurehero version
poetry build
```

Si se modifica `transform_file.py`, crear un CSV temporal y probar el comando
afectado.

Si se modifica `main.py`, probar:

```bash
poetry run featurehero --help
poetry run featurehero run --help
poetry run featurehero transform --help
poetry run featurehero jobs --help
```

## 16. Reglas para Agentes IA

- No revertir cambios del usuario sin permiso.
- No cambiar la interfaz publica de CLI salvo instruccion explicita.
- No modificar el algoritmo genetico si la tarea es documentacion, packaging o
  release.
- Preferir cambios pequenos y localizados.
- Mantener README orientado a usuarios.
- Mantener IA_ARCHITECTURE orientado a contexto tecnico interno.
- Actualizar ambos documentos cuando cambie un comando, parametro, modelo,
  metrica, transformacion o flujo de release.
- Tratar `dist/`, workspaces y logs como artefactos generados, no como fuente.
- Si una validacion falla por entorno local, reportar el motivo exacto.

## 17. Problemas Conocidos o Puntos a Vigilar

- El entorno local puede tener un Python distinto a 3.12; el paquete declara
  soporte `>=3.12,<4.0`.
- Matplotlib puede advertir sobre `MPLCONFIGDIR` si el home no es escribible en
  sandboxes.
- `poetry install` escribe en el virtualenv de Poetry, normalmente bajo
  `~/.cache/pypoetry`.
- `poetry.lock` debe regenerarse si cambia significativamente `pyproject.toml`.
- Los jobs escriben fuera del repositorio, en `~/.featurehero`.
