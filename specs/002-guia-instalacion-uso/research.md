# Research: Guía de instalación y uso para principiantes

## Decision 1: Instalar desde el repositorio local como ruta principal

- **Decision**: La guía instruirá descargar o clonar el repositorio, crear un
  entorno aislado y ejecutar `pip install .` desde la raíz del proyecto.
- **Rationale**: Es el flujo solicitado por el producto y está respaldado por
  `README.md` y `pyproject.toml`, que define el paquete y el comando
  `featurehero`.
- **Alternatives considered**: La instalación directa desde una URL remota o un
  artefacto publicado se mantiene fuera del recorrido principal.

## Decision 2: Mantener Poetry como ruta secundaria de desarrollo

- **Decision**: Poetry aparecerá en una sección separada para colaboradores y
  desarrollo local, no como requisito del recorrido principiante.
- **Rationale**: El README y el workflow de release usan Poetry para desarrollo,
  validación y construcción, mientras que el usuario final puede instalar el
  paquete local con `pip`.
- **Alternatives considered**: Hacer Poetry obligatorio fue rechazado porque
  añadiría una herramienta de desarrollo al camino básico sin ser necesaria.

## Decision 3: Validar primero Windows, macOS y Ubuntu/Debian

- **Decision**: La guía tendrá instrucciones completas para Windows, macOS y
  Ubuntu/Debian, con límites y adaptación general para otras distribuciones Linux.
- **Rationale**: Coincide con la aclaración aprobada y permite validar comandos,
  activación de entornos y rutas de archivos con un alcance concreto.
- **Alternatives considered**: Documentar recetas detalladas para todas las
  distribuciones Linux ampliaría el alcance sin evidencia de soporte equivalente.

## Decision 4: Usar el CLI existente como señal de instalación correcta

- **Decision**: La guía verificará la instalación con `featurehero --help` y
  `featurehero version`, y dirigirá al usuario a la ayuda específica de cada comando.
- **Rationale**: El entry point está declarado en `pyproject.toml` y el CLI expone
  `version`, `run`, `transform`, `analyze-results` y `jobs`.
- **Alternatives considered**: Verificar solo la presencia del entorno Python no
  demuestra que el paquete ni el comando estén disponibles.

## Decision 5: Construir un ejemplo pequeño y reproducible

- **Decision**: El inicio rápido usará un CSV pequeño creado por el usuario o
  incluido explícitamente por la implementación, con una transformación simple
  y un flujo de optimización con parámetros reducidos.
- **Rationale**: El repositorio no contiene actualmente un dataset de ejemplo
  dedicado; un archivo pequeño evita depender de datos externos.
- **Alternatives considered**: Usar `data/gold_price.csv` fue rechazado porque
  esa ruta aparece como ejemplo en el README pero no existe en el repositorio.

## Decision 6: Explicar las variantes de shell de Windows

- **Decision**: La ruta Windows distinguirá PowerShell y CMD para crear, activar
  el entorno y ejecutar la instalación.
- **Rationale**: La activación usa comandos distintos y una sola instrucción
  ambigüa puede bloquear a usuarios principiantes.
- **Alternatives considered**: Documentar solo PowerShell fue rechazado porque no
  cubre el shell clásico incluido en Windows.

## Decision 7: Tratar las inconsistencias observadas como validaciones de implementación

- **Decision**: La guía no prometerá resultados de release o versiones que no se
  hayan comprobado en una instalación limpia; las discrepancias entre metadata,
  README y workflow se resolverán o se documentarán como límites antes de publicar.
- **Rationale**: El workflow construye releases de GitHub, no publica automáticamente
  en PyPI, y la validación automática actual se centra en Ubuntu.
- **Alternatives considered**: Copiar literalmente todas las instrucciones del
  README fue rechazado porque contiene marcadores de repositorio y ejemplos no
  presentes en el árbol actual.
