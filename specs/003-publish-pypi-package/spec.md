# Feature Specification: Publicar Feature Hero para instalación con pip

**Feature Branch**: `003-publish-pypi-package`

**Created**: 2026-11-22

**Status**: Draft

**Input**: User description: "Se desea que la aplicación ya esté en pip para su instalación sin necesidad de bajar el repositorio, solo con el comando de pip."

## Clarifications

### Session 2026-11-22

- Q: ¿Cómo debe configurarse la identidad de Trusted Publishing en PyPI para permitir que GitHub Actions publique `featurehero`? → A: Configurar un Trusted Publisher de PyPI vinculado al repositorio, workflow, rama o entorno protegido de GitHub Actions, y registrar la evidencia en `release-evidence.md`.
- Q: ¿Qué estrategia debe usar el workflow para verificar la disponibilidad del paquete en PyPI después de publicarlo? → A: Reintentar durante un máximo de 5 minutos, con intervalos de 15 segundos; fallar con un mensaje identificable si la versión no aparece.
- Q: ¿Cómo debe organizarse la validación de release para evitar duplicar la tarea de crear la estructura y la implementación de los checks? → A: Mantener el scaffolding mínimo de `.github/scripts/` como preparación y dejar las tareas posteriores para la implementación funcional de las validaciones.
- Q: ¿Cómo debe organizarse el archivo de evidencia del release para evitar duplicar la plantilla y su llenado? → A: Crear la plantilla única `specs/003-publish-pypi-package/release-evidence.md` durante Setup y completarla durante la publicación.
- Q: ¿Qué nivel de detalle debe tener la validación de dependencias publicadas frente a las declaradas en `pyproject.toml`? → A: Comparar dependencias declaradas y empaquetadas, y verificar que todas se resuelven durante la instalación limpia desde PyPI.
- Q: ¿Qué resultado verificable deben producir las tareas de preparación T001 y T003? → A: T001 actualiza la matriz de alcance en `release-evidence.md`; T003 crea ese archivo con secciones para versión, commit, artefactos, plataformas, Python, comandos, resultados y excepciones.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Instalar desde PyPI sin descargar el repositorio (Priority: P1)

Una persona que quiere usar Feature Hero desea instalarlo como un paquete público con un comando de pip, sin clonar ni descargar el repositorio fuente.

**Why this priority**: Es el objetivo principal de la feature y elimina la barrera más importante del flujo actual de instalación.

**Independent Test**: En un entorno Python compatible que no contenga una copia del repositorio, una persona ejecuta el comando de instalación pública, verifica el CLI y puede consultar su ayuda.

**Acceptance Scenarios**:

1. **Given** un equipo con Python compatible, Internet y pip disponible, **When** la persona ejecuta `python -m pip install featurehero`, **Then** el paquete y sus dependencias se instalan sin exigir una copia del repositorio.
2. **Given** que la instalación pública terminó correctamente, **When** la persona ejecuta `featurehero --help` y `featurehero version`, **Then** el CLI responde y muestra la versión instalada.
3. **Given** que la persona instala en Windows, macOS, Ubuntu/Debian u otra plataforma compatible, **When** sigue el comando de instalación pública, **Then** encuentra instrucciones y una señal de verificación para su entorno.

---

### User Story 2 - Publicar una versión instalable y verificable (Priority: P1)

Una persona mantenedora quiere publicar una versión del paquete con metadata, artefactos y dependencias correctos para que el registro público pueda instalarla de forma reproducible.

**Why this priority**: Sin un proceso de publicación verificable, el comando público puede instalar una versión incompleta, equivocada o no reproducible.

**Independent Test**: Una versión construida desde el estado aprobado del proyecto puede publicarse, localizarse en el registro público y ser instalada en un entorno limpio con la versión esperada.

**Acceptance Scenarios**:

1. **Given** una versión aprobada y un árbol de trabajo limpio, **When** se construyen y publican los artefactos de distribución, **Then** el registro muestra la versión y los archivos esperados.
2. **Given** una versión ya publicada, **When** se instala en un entorno limpio, **Then** las dependencias declaradas se resuelven y la metadata instalada coincide con la versión publicada.
3. **Given** que una publicación falla, **When** la persona mantenedora revisa el proceso, **Then** recibe un resultado identificable y no se presenta una versión incompleta como disponible.

---

### User Story 3 - Mantener documentación y rutas de desarrollo coherentes (Priority: P2)

Una persona usuaria o colaboradora quiere saber cuándo usar la instalación pública y cuándo descargar el repositorio para desarrollo, consultando la información en español o inglés.

**Why this priority**: La nueva ruta pública debe simplificar el uso sin romper el flujo local requerido para desarrollo y contribuciones.

**Independent Test**: Una revisión de README y guía puede distinguir la instalación pública, la instalación desde fuente y la ruta opcional de Poetry sin instrucciones contradictorias.

**Acceptance Scenarios**:

1. **Given** el README y la guía bilingües, **When** una persona busca instalar Feature Hero para usarlo, **Then** encuentra `python -m pip install featurehero` como ruta principal.
2. **Given** que una persona quiere modificar o desarrollar el proyecto, **When** consulta la documentación, **Then** encuentra la ruta desde el repositorio y Poetry claramente identificadas como alternativas de desarrollo.
3. **Given** una actualización de versión, **When** se revisan README y guía, **Then** los comandos, versión, enlaces y advertencias coinciden en español e inglés.

### Edge Cases

- El nombre del paquete público no coincide con el nombre del comando CLI.
- La versión publicada ya existe y el registro rechaza una nueva publicación con el mismo número.
- El entorno del usuario usa una versión de Python no compatible.
- Una dependencia no está disponible para una de las plataformas soportadas.
- La publicación contiene solo un formato de artefacto y falla en un entorno que necesita otro.
- La instalación termina, pero `featurehero` no queda disponible en el PATH del entorno activo.
- Una versión publicada tiene documentación o metadata distinta de la versión del código.
- Las credenciales o permisos de publicación no están disponibles, caducaron o fueron expuestos.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El proyecto MUST publicar Feature Hero en un registro público de paquetes Python con el nombre instalable `featurehero`.
- **FR-002**: Una persona MUST poder instalar la versión publicada sin descargar ni clonar el repositorio, ejecutando `python -m pip install featurehero` desde un entorno Python compatible.
- **FR-003**: La distribución publicada MUST incluir la metadata de versión, dependencias y punto de entrada CLI necesarios para que `featurehero` quede disponible después de la instalación.
- **FR-004**: La distribución MUST publicar los artefactos necesarios para los entornos de instalación soportados, incluyendo un wheel y un source distribution cuando el proyecto los genere.
- **FR-005**: La versión instalada mediante pip MUST coincidir con la versión aprobada y publicada del proyecto.
- **FR-006**: La instalación pública MUST poder verificarse ejecutando `featurehero --help` y `featurehero version` sin requerir el repositorio fuente.
- **FR-007**: El proceso de publicación MUST validar antes de publicar que la metadata, dependencias declaradas y empaquetadas, artefactos y punto de entrada corresponden al código aprobado, y que las dependencias se resuelven en una instalación limpia.
- **FR-008**: El proceso MUST impedir o identificar una publicación con una versión ya existente, incompleta o diferente de la versión aprobada.
- **FR-009**: Las credenciales y permisos de publicación MUST manejarse fuera del código fuente mediante un Trusted Publisher de PyPI o un secreto protegido de GitHub Actions; no MUST incluir secretos en el repositorio ni en los artefactos publicados.
- **FR-010**: El README y la guía de instalación y uso MUST presentar `python -m pip install featurehero` como ruta principal para usuarios finales en español e inglés.
- **FR-011**: El README y la guía MUST conservar la instalación desde el repositorio y Poetry como rutas claramente separadas para desarrollo y contribución.
- **FR-012**: La documentación MUST indicar los requisitos de Python, el nombre del paquete, el comando CLI, la verificación de instalación y las acciones de recuperación para fallos de publicación o instalación.
- **FR-013**: La publicación MUST conservar los nombres de comandos CLI, parámetros públicos y formatos de entrada existentes salvo cambios aprobados por una especificación.
- **FR-014**: La versión publicada MUST poder instalarse y verificarse en Windows PowerShell, Windows CMD, macOS y Ubuntu/Debian, o el proceso MUST registrar explícitamente la plataforma no validada antes de declarar la versión lista.

### Key Entities

- **Distribución pública**: Paquete instalable desde el registro, con nombre, versión, metadata, dependencias y artefactos.
- **Versión publicada**: Identificador único que relaciona código aprobado, artefactos, documentación y release.
- **Proceso de publicación**: Secuencia de validación, construcción, autorización, carga y verificación de una distribución.
- **Instalación pública**: Estado de un entorno donde el paquete fue instalado sin el repositorio fuente y el CLI responde.
- **Ruta documental**: Instrucciones bilingües que distinguen uso final, desarrollo desde fuente y publicación.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Al menos 4 de 5 personas del público objetivo pueden instalar Feature Hero desde el registro público sin descargar el repositorio y verificar el CLI en menos de 5 minutos, excluyendo descargas lentas de dependencias.
- **SC-002**: Una instalación limpia puede resolver todas las dependencias declaradas y dejar disponible `featurehero` sin pasos manuales adicionales en al menos 4 de 5 intentos.
- **SC-003**: El 100% de las versiones declaradas como publicadas muestra la misma versión en metadata del paquete y en `featurehero version`.
- **SC-004**: Cada publicación aprobada contiene los artefactos de distribución requeridos y puede instalarse desde el registro en un entorno limpio.
- **SC-005**: La revisión previa a publicación detecta el 100% de los casos de versión duplicada, metadata inválida, dependencia ausente o artefacto faltante antes de declarar una versión lista.
- **SC-006**: README y guía muestran el comando público como ruta principal y mantienen equivalencia funcional en español e inglés en el 100% de las secciones de instalación.
- **SC-007**: La instalación pública y la verificación del CLI se validan en Windows PowerShell, Windows CMD, macOS y Ubuntu/Debian, o cada excepción queda registrada antes de la publicación.
- **SC-008**: No se encuentra ningún secreto de publicación en el código fuente, historial del repositorio ni artefactos distribuidos durante la revisión de release.

## Assumptions

- El registro público objetivo será PyPI y el nombre público del paquete será `featurehero`.
- La versión seguirá el formato de proyecto `yyyy.mayor.minor.micro` y cada publicación usará una versión nueva.
- La publicación se realizará desde una rama y un commit aprobados, con el árbol de trabajo limpio.
- El flujo público con pip será la ruta recomendada para usuarios finales; descargar el repositorio y usar Poetry seguirá siendo una ruta de desarrollo.
- El proyecto mantendrá compatibilidad con Python `>=3.12,<4.0`.
- La publicación requerirá una cuenta o identidad mantenedora con permisos en PyPI, pero ningún secreto se almacenará en el repositorio.
- La identidad Trusted Publisher o el secreto protegido `PYPI_TOKEN` deberá configurarse antes del release y el repositorio, workflow y entorno protegido deberán quedar registrados en la evidencia de publicación sin registrar el valor del secreto.
- La verificación post-publicación consultará PyPI durante un máximo de 5 minutos, con intervalos de 15 segundos, y fallará de forma identificable si la versión no aparece.
- Las validaciones multiplataforma podrán ejecutarse en automatización o entornos disponibles; una plataforma no validada deberá quedar registrada antes de publicar.
- Esta feature no cambia la lógica de transformación, selección genética, regresión, análisis de resultados ni los comandos públicos existentes.
