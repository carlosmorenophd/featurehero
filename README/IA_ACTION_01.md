# IA_ACTION_01 — Mejora del archivo de resultados finales

## Aclaración de alcance

El algoritmo genético y los modelos ya realizan el proceso necesario. **No se modificarán**:

- creación, selección, cruce o mutación de individuos;
- generaciones, población ni fitness;
- entrenamiento o evaluación de modelos;
- búsqueda de hiperparámetros;
- selección de variables realizada por el algoritmo;
- formato o lógica interna del proceso que genera el resultado original.

El trabajo se concentrará exclusivamente en **leer y analizar un archivo final de resultados ya generado**, y producir nuevos archivos de resumen que ayuden a interpretar la relevancia de las variables.

Contrato vigente del comando: recibe un `--file` con el CSV final y un
`--output-dir` obligatorio que debe representar una carpeta. El archivo debe
comenzar con las 18 columnas estándar, desde `machine_name` hasta
`accuracy_mape`, en orden exacto, y contener al menos dos columnas `feature_`.
Este contrato sustituye las propuestas iniciales de recibir múltiples archivos
en una sola invocación.

## Objetivo

Construir una etapa posterior al algoritmo que tome el CSV final y convierta sus filas en evidencia agregada sobre las variables seleccionadas.

El CSV original se conservará sin cambios. Los nuevos resultados serán archivos derivados.

## Interpretación del archivo actual

Las columnas se clasificarán así:

1. Identificación:
   - `machine_name`: modelo o máquina que produjo el individuo.
   - `index_metric`: métrica utilizada para ordenar o evaluar el individuo.
2. Métricas del individuo:
   - `d2_absolute_error_score`
   - `d2_pinball_score`
   - `d2_tweedie_score`
   - `explained_variance_score`
   - `max_error`
   - `mean_absolute_error`
   - `mean_absolute_percentage_error`
   - `mean_gamma_deviance`
   - `mean_poisson_deviance`
   - `mean_squared_error`
   - `mean_squared_log_error`
   - `median_absolute_error`
   - `r2_score`
   - `root_mean_squared_error`
   - `root_mean_squared_log_error`
   - `accuracy_mape`
3. Hiperparámetros:
   - columnas específicas de cada modelo, como `n_estimators_*`, `eta_*`, `gamma_*` y similares.
4. Selección de variables:
   - toda columna cuyo nombre comience con `feature_`;
   - `True` significa que el individuo seleccionó la variable;
   - `False` significa que el individuo no la seleccionó.

La muestra proporcionada contiene una sola fila. Permite validar la estructura, pero las frecuencias y coocurrencias sólo serán estadísticamente útiles al analizar un archivo final completo con múltiples individuos.

## Trabajo que se realizará

### 1. Crear un analizador independiente

Se agregará un módulo de postprocesamiento separado del algoritmo genético. Su responsabilidad será:

- cargar un CSV final;
- validar las columnas mínimas;
- reconocer automáticamente métricas, hiperparámetros y columnas `feature_`;
- convertir valores booleanos escritos como texto, booleanos reales o `0/1`;
- conservar `machine_name` para generar análisis globales y por modelo;
- no modificar ni sobrescribir los archivos originales.

Ubicación propuesta:

```text
featurehero/services/results/result_analyzer.py
```

### 2. Frecuencia de selección

Para cada variable se calculará:

```text
selection_rate = individuos que seleccionaron la variable / individuos analizados
```

Se producirán al menos:

- número de veces seleccionada;
- número total de individuos;
- frecuencia de selección entre `0` y `1`;
- frecuencia global;
- frecuencia separada por `machine_name`.

También se calculará la frecuencia dentro de los mejores individuos, usando un porcentaje configurable —por ejemplo, el mejor 10 %— según `index_metric`.

### 3. Frecuencia ponderada por calidad

No todos los individuos deben aportar la misma evidencia. Se normalizará la calidad del resultado y se calculará una frecuencia ponderada:

```text
weighted_selection = suma(calidad normalizada de individuos que seleccionan la variable)
                     / suma(calidad normalizada de todos los individuos)
```

El analizador deberá conocer la orientación de la métrica:

- mayor es mejor: `r2_score`, `accuracy_mape`, D2 y varianza explicada;
- menor es mejor: MAE, MAPE, MSE, RMSE, errores logarítmicos, desviancias y error máximo.

Si el archivo no indica con claridad qué representa `index_metric`, se permitirá seleccionar explícitamente la columna de ranking y su orientación.

### 4. Coocurrencia de variables

Se calculará cuántas veces dos variables aparecen juntas dentro de los individuos del archivo final.

Se entregarán dos medidas:

- frecuencia conjunta;
- similitud de Jaccard, para evitar que variables muy frecuentes parezcan relacionadas sólo por su frecuencia individual.

La coocurrencia se reportará como relación entre variables; no se sumará automáticamente a la importancia individual porque una alta coocurrencia también puede representar redundancia.

### 5. Estabilidad entre ejecuciones

Cada invocación recibe un único archivo final. Por ello, la estabilidad entre
ejecuciones se marcará como no disponible y no participará en el score. Los
pesos de los componentes disponibles se renormalizarán automáticamente.

### 6. Importancia del modelo, SHAP y permutation importance

Estas evidencias **no se recalcularán dentro del algoritmo genético**.

El CSV mostrado contiene métricas, hiperparámetros y selección de features, pero no contiene valores SHAP, permutation importance ni importancia nativa de cada variable. Por ello:

- si esos valores aparecen en archivos finales adicionales, el analizador podrá integrarlos;
- si no existen, se marcarán como `not_available` y no se inventarán ni se interpretarán a partir de los booleanos;
- no se volverán a entrenar modelos como parte de este plan;
- no se modificará el algoritmo para producir estas columnas.

La primera versión del análisis se basará en la evidencia realmente disponible: frecuencia, calidad de los individuos, modelos y coocurrencia.

### 7. Índice de Relevancia basado en resultados disponibles

Se calculará un índice compuesto sólo con componentes presentes en los archivos analizados:

```text
relevance_score =
    w_frequency * selection_rate
  + w_elite     * elite_selection_rate
  + w_weighted  * weighted_selection_rate
  + w_stability * stability
```

Pesos conceptuales del índice:

```text
frequency = 0.25
elite     = 0.30
weighted  = 0.25
stability = 0.20
```

En el contrato vigente se analiza un solo archivo, por lo que el componente de estabilidad no está disponible y los pesos restantes se renormalizan automáticamente.

Reglas del índice:

- resultado entre `0` y `1`;
- pesos configurables;
- conservar todos los componentes junto al score final;
- no convertir evidencia ausente en cero;
- incluir el número de individuos y archivos usados;
- generar rankings globales y por modelo.

Si posteriormente se reciben archivos con SHAP, permutación o importancia nativa, podrán agregarse como componentes opcionales sin cambiar el algoritmo genético.

## Archivos derivados propuestos

El proceso generará una carpeta de análisis junto al resultado, sin reemplazar el CSV original:

```text
analysis_results/
  feature_relevance.csv
  feature_relevance_by_model.csv
  feature_cooccurrence.csv
  analysis_summary.json
```

### `feature_relevance.csv`

Una fila por variable, con columnas semejantes a:

```text
feature
selected_count
individual_count
selection_rate
elite_selected_count
elite_selection_rate
weighted_selection_rate
stability
run_count
relevance_score
rank
```

### `feature_relevance_by_model.csv`

El mismo análisis separado por `machine_name`, para evitar mezclar directamente comportamientos de modelos distintos.

### `feature_cooccurrence.csv`

Formato largo para evitar una matriz excesivamente ancha:

```text
feature_a
feature_b
joint_count
joint_rate
jaccard_score
```

### `analysis_summary.json`

Guardará:

- archivos de entrada;
- número de individuos;
- modelos encontrados;
- métricas encontradas;
- número de features;
- métrica y orientación utilizadas para ordenar;
- porcentaje de élite;
- pesos del índice;
- advertencias y componentes no disponibles.

## Validaciones necesarias

Antes del cálculo se verificará:

- que exista `machine_name`;
- que exista por lo menos una columna `feature_`;
- que las features contengan valores booleanos reconocibles;
- que la métrica de ranking sea numérica;
- que todos los archivos combinados tengan features compatibles;
- que los nombres de variables se obtengan eliminando únicamente el prefijo `feature_`;
- que las filas duplicadas se reporten y su tratamiento sea configurable;
- que valores ausentes no sean convertidos silenciosamente en `False`.

## Pruebas

Se crearán pruebas independientes para el analizador:

1. clasificación correcta de columnas;
2. conversión segura de booleanos;
3. frecuencia global y por modelo;
4. selección dentro de la élite;
5. orientación de métricas de error y puntuación;
6. ponderación por calidad;
7. coocurrencia y Jaccard;
8. componente de estabilidad marcado como no disponible;
9. renormalización de pesos con componentes ausentes;
10. conservación intacta del archivo original.

## Orden de implementación

1. Lector y validador del CSV final.
2. Clasificación automática de columnas.
3. Frecuencia global, por élite y por modelo.
4. Normalización de calidad y frecuencia ponderada.
5. Coocurrencia.
6. Registro explícito de que la estabilidad entre ejecuciones no está disponible.
7. Índice de Relevancia.
8. Exportación de archivos derivados.
9. Pruebas y documentación de uso.

## Criterios de aceptación

- El algoritmo genético y los modelos permanecen sin cambios.
- El CSV original permanece sin cambios.
- El analizador puede trabajar con el formato actual.
- Cada score puede reconstruirse desde sus componentes.
- El resultado distingue análisis global de análisis por modelo.
- La ausencia de SHAP o permutation importance se informa explícitamente.
- Con un solo individuo no se presentan frecuencias como evidencia estable.
- La estabilidad entre ejecuciones se informa como no disponible porque cada invocación recibe un único archivo.

## Fuera de alcance

- corregir o rediseñar el algoritmo genético;
- modificar modelos o hiperparámetros;
- volver a entrenar modelos;
- cambiar el proceso de generación del CSV original;
- instrumentar generaciones o individuos dentro del algoritmo;
- agregar SHAP o permutation importance al entrenamiento;
- cambiar la división de datos, semillas, mutación, cruce o criterio de parada.

## Estado

Plan ejecutado. Se implementó el analizador independiente, el comando
`featurehero analyze-results`, la exportación de los cuatro archivos derivados
y las pruebas de frecuencia, élite, ponderación, coocurrencia, formato estricto,
carpeta de salida, validación y conservación del archivo original. El algoritmo
genético y los modelos permanecen sin cambios. Versión actual: `2026.2.1`.
