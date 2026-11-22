# Research: Publicar Feature Hero para instalación con pip

## Decision 1: Publicar el paquete existente sin cambiar el CLI

- **Decision**: Usar la metadata actual de `pyproject.toml`, el paquete `featurehero`
  y el entry point `featurehero = "featurehero.main:main"` como fuente de la
  distribución pública.
- **Rationale**: El proyecto ya construye wheel y source distribution con Poetry;
  la feature debe hacerlos accesibles desde PyPI sin modificar la lógica de la
  aplicación.
- **Alternatives considered**: Crear un paquete wrapper o cambiar el nombre del
  CLI fue rechazado porque rompería la interfaz pública existente.

## Decision 2: Usar Trusted Publishing para PyPI

- **Decision**: Publicar desde GitHub Actions con Trusted Publishing/OIDC y una
  configuración de entorno protegida para PyPI; no guardar tokens en el repositorio.
- **Rationale**: La documentación oficial de PyPA recomienda Trusted Publishing
  para CI/CD compatible porque usa credenciales de corta duración y evita tokens
  persistentes. Referencias: [PyPA tool recommendations](https://packaging.python.org/en/latest/guides/tool-recommendations/),
  [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/).
- **Alternatives considered**: Un token API almacenado como secret es una opción
  de recuperación, pero se deja fuera del camino principal por su mayor riesgo
  operativo.

## Decision 3: Mantener el workflow de GitHub Release como punto de publicación

- **Decision**: Extender `.github/workflows/release.yml` para validar el build,
  publicar el mismo contenido en PyPI y conservar la creación de la GitHub Release.
- **Rationale**: El workflow ya construye `dist/*.whl` y `dist/*.tar.gz` desde el
  commit etiquetado, por lo que evita dos procesos de build potencialmente distintos.
- **Alternatives considered**: Publicar manualmente desde la estación de desarrollo
  fue rechazado por menor reproducibilidad y mayor exposición de credenciales.

## Decision 4: Validar antes de publicar y después instalar desde el índice

- **Decision**: Antes de publicar se ejecutan metadata checks, tests, build y
  verificación de artefactos; después se instala la versión publicada en un
  entorno limpio y se ejecutan `featurehero --help` y `featurehero version`.
- **Rationale**: La instalación pública debe demostrar tanto la integridad del
  artefacto como la disponibilidad del entry point y dependencias.
- **Alternatives considered**: Verificar solo que el job de publicación terminó
  fue rechazado porque no prueba el consumo real del paquete.

## Decision 5: Conservar la separación entre usuarios y desarrollo

- **Decision**: README y guía mostrarán `python -m pip install featurehero` como
  ruta principal; clonar el repositorio, `pip install .` y Poetry quedarán como
  rutas de desarrollo.
- **Rationale**: Los usuarios finales no necesitan Git ni el árbol fuente, mientras
  que colaboradores sí necesitan reproducir el entorno local.
- **Alternatives considered**: Presentar todas las rutas con la misma prioridad
  fue rechazado por aumentar la confusión del flujo principal.

## Decision 6: Mantener la versión del proyecto como autoridad

- **Decision**: La versión de `pyproject.toml` será única, nueva y coincidirá con
  la metadata instalada, el comando `featurehero version` y la distribución subida.
- **Rationale**: PyPI no permite reutilizar una versión publicada y la discrepancia
  entre metadata y CLI genera instalaciones difíciles de diagnosticar.
- **Alternatives considered**: Derivar la versión solo del tag fue rechazado porque
  el proyecto ya mantiene una versión explícita en `pyproject.toml`.
