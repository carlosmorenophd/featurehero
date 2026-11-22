# Feature Specification: Guía de instalación y uso para principiantes

**Feature Branch**: `002-guia-instalacion-uso`

**Created**: 2026-11-22

**Status**: Draft

**Input**: User description: "Crear una guía detallada en Markdown para instalar y usar el proyecto desde cero en Windows, macOS y Linux, orientada a usuarios con poca experiencia de programación y complementaria al README técnico."

## Clarifications

### Session 2026-11-22

- Q: ¿Qué alcance debe tener la guía para Linux? → A: Ubuntu/Debian como ruta principal; orientación general para otras distribuciones.
- Q: ¿Cuál debe ser la ruta principal de instalación para una persona principiante? → A: Descargar el repositorio, crear un entorno aislado e instalar el paquete localmente con `pip install .`; Poetry queda como alternativa para desarrollo.
- Q: ¿Qué idiomas deben cubrir la guía y el README? → A: Ambos documentos deben ofrecer el contenido completo en español e inglés.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Instalar desde cero en cualquier plataforma (Priority: P1)

Una persona con poca experiencia de programación quiere preparar Feature Hero en su equipo sin depender de conocimientos previos ni de asistencia externa, pudiendo leer la guía en español o inglés.

**Why this priority**: La instalación es el requisito previo para cualquier uso y es la principal necesidad expresada por los usuarios.

**Independent Test**: Una persona que no haya usado el proyecto puede seguir una de las rutas de plataforma y terminar con una instalación funcional, confirmada por una comprobación explícita.

**Acceptance Scenarios**:

1. **Given** una persona con un equipo Windows, macOS o Linux y una copia del proyecto, **When** sigue la sección de su plataforma desde el primer paso, **Then** encuentra instrucciones ordenadas para preparar los requisitos, instalar el proyecto y comprobar que quedó disponible.
2. **Given** que una persona no sabe qué plataforma o requisito tiene instalado, **When** consulta la guía, **Then** encuentra cómo identificar la plataforma y cómo validar cada requisito antes de continuar.
3. **Given** que un paso de instalación falla, **When** la persona consulta la guía, **Then** encuentra una acción de recuperación o una referencia clara a la sección de solución de problemas.

---

### User Story 2 - Ejecutar el primer flujo de uso (Priority: P1)

Una persona recién instalada quiere ejecutar un ejemplo completo con datos de entrada, entender qué debe proporcionar y reconocer el resultado esperado.

**Why this priority**: La instalación solo entrega valor si el usuario puede completar su primera tarea con confianza.

**Independent Test**: Después de instalar el proyecto, una persona puede seguir el ejemplo inicial y confirmar que obtuvo un resultado reconocible sin consultar documentación técnica adicional.

**Acceptance Scenarios**:

1. **Given** una instalación verificada y un conjunto de datos de ejemplo, **When** la persona sigue el flujo de inicio rápido, **Then** puede preparar la entrada, ejecutar el comando indicado e identificar dónde se generan los resultados.
2. **Given** que la persona desconoce el significado de una entrada, opción o salida, **When** lee la guía en español o inglés, **Then** encuentra una explicación en lenguaje sencillo y una referencia al README en el idioma elegido para los detalles avanzados.

---

### User Story 3 - Resolver problemas frecuentes y continuar aprendiendo (Priority: P2)

Una persona encuentra un mensaje de error o necesita ampliar el uso básico y quiere recuperar el flujo sin perderse entre documentación técnica.

**Why this priority**: La orientación de recuperación reduce abandonos y permite que la guía siga siendo útil después del primer ejemplo.

**Independent Test**: A partir de problemas representativos de permisos, requisitos ausentes, rutas de archivos o datos inválidos, una persona puede localizar el síntoma y seguir una acción correctiva.

**Acceptance Scenarios**:

1. **Given** un error común durante la instalación o ejecución, **When** la persona busca el mensaje o síntoma en la sección de problemas frecuentes, **Then** encuentra causa probable, solución paso a paso y el siguiente diagnóstico recomendado.
2. **Given** que la persona completó el ejemplo inicial, **When** quiere consultar opciones avanzadas, **Then** la guía la dirige al README técnico en el idioma elegido sin duplicar su contenido ni contradecirlo.

### Edge Cases

- El usuario no tiene permisos suficientes para instalar dependencias o crear archivos en la ubicación elegida.
- El usuario utiliza una versión no compatible del requisito principal o una arquitectura distinta de la asumida por los pasos.
- La ruta del proyecto o de los datos contiene espacios, caracteres especiales o una ubicación sincronizada.
- El usuario parte de una instalación parcial o de una versión anterior y necesita saber si debe limpiarla o actualizarla.
- El conjunto de datos de entrada falta, está en una ubicación equivocada o no cumple el formato esperado.
- La guía debe indicar qué hacer si un comando no se reconoce y cómo reportar un problema cuando las soluciones no funcionan.
- Una sección está traducida parcialmente, omite pasos o utiliza términos distintos entre español e inglés.
- Un enlace interno lleva al idioma equivocado, a una sección inexistente o a contenido desactualizado en uno de los dos idiomas.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El proyecto MUST incluir una guía independiente en formato Markdown, enlazable desde la documentación de entrada del proyecto, que explique instalación y uso para personas con poca experiencia de programación.
- **FR-015**: La guía MUST ofrecer el contenido completo de instalación, primer uso, solución de problemas y alcance en español e inglés, con secciones claramente identificadas por idioma.
- **FR-016**: El README MUST ofrecer en español e inglés el contenido necesario para orientar al usuario hacia la guía y consultar la referencia técnica, manteniendo equivalencia funcional entre ambos idiomas.
- **FR-002**: La guía MUST comenzar desde cero e indicar cómo identificar la plataforma, preparar los requisitos, descargar el repositorio, entrar en su directorio raíz, crear un entorno aislado, instalar el paquete localmente con `pip install .` y verificar la instalación.
- **FR-003**: La guía MUST proporcionar un recorrido paso a paso específico para Windows.
- **FR-004**: La guía MUST proporcionar un recorrido paso a paso específico para macOS.
- **FR-005**: La guía MUST proporcionar un recorrido paso a paso específico para Ubuntu/Debian como ruta principal de Linux, e indicar las diferencias relevantes y los límites de soporte para otras distribuciones cuando afecten al recorrido.
- **FR-006**: La guía MUST incluir un inicio rápido común que muestre cómo preparar una entrada de ejemplo, ejecutar el flujo principal y localizar o interpretar sus resultados.
- **FR-007**: Cada paso que requiera una acción MUST indicar qué debe hacer la persona y cómo reconocer que el paso terminó correctamente.
- **FR-008**: La guía MUST explicar en lenguaje sencillo los conceptos mínimos necesarios para el primer uso y MUST enlazar al README técnico para opciones, parámetros y escenarios avanzados.
- **FR-009**: La guía MUST incluir una sección de solución de problemas con síntomas, causas probables, acciones correctivas y criterios para solicitar ayuda.
- **FR-010**: La guía MUST advertir sobre requisitos previos, permisos, rutas de archivos, formatos de entrada y mensajes de error que puedan bloquear el recorrido.
- **FR-011**: La guía MUST mantener consistencia con los comandos, requisitos, formatos y comportamiento documentados por el proyecto; las instrucciones duplicadas que diverjan del README MUST corregirse antes de publicar la guía.
- **FR-012**: La guía MUST indicar el alcance de su contenido y señalar qué temas quedan fuera del recorrido inicial para evitar que un usuario principiante confunda instrucciones avanzadas con pasos obligatorios.
- **FR-013**: La guía MUST ser navegable mediante títulos, tabla de contenido o enlaces internos suficientes para llegar rápidamente a la plataforma, inicio rápido y solución de problemas.
- **FR-014**: La guía MUST presentar la instalación desde el repositorio local como el recorrido principal y MUST identificar Poetry como una alternativa destinada al desarrollo del proyecto, sin mezclar ambos recorridos como si fueran requisitos equivalentes.
- **FR-017**: La guía y el README MUST mantener equivalencia de comandos, requisitos, advertencias, enlaces y límites de alcance entre las versiones en español e inglés; una corrección en un idioma MUST reflejarse en el otro antes de publicar.
- **FR-018**: La guía y el README MUST usar una estructura de navegación que permita cambiar entre español e inglés sin perder la sección equivalente ni el contexto del recorrido.
- **FR-019**: El README MUST incluir, tanto en español como en inglés, un enlace visible hacia la guía de instalación y uso bilingüe.
- **FR-020**: El README y la guía de instalación y uso MUST incluir un índice o tabla de contenidos en cada idioma, con enlaces internos que permitan saltar directamente a la plataforma, instalación, inicio rápido, solución de problemas y referencia técnica correspondientes.

### Key Entities

- **Guía de usuario**: Documento orientado a instalación y primer uso, con secciones comunes y recorridos por plataforma.
- **Recorrido de plataforma**: Secuencia ordenada de requisitos, acciones, verificaciones y recuperación para Windows, macOS o Linux.
- **Inicio rápido**: Ejemplo reproducible que conecta una instalación verificada con una primera ejecución y sus resultados.
- **Problema frecuente**: Combinación de síntoma, causa probable, solución y siguiente paso de diagnóstico.
- **Referencia técnica**: Enlace al README u otra documentación existente para detalles avanzados que no deben duplicarse.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Al menos 4 de 5 personas que representan al público objetivo pueden completar la instalación y la verificación en Windows, macOS o Linux sin ayuda externa y sin consultar el README técnico durante el recorrido inicial.
- **SC-002**: Una persona del público objetivo puede localizar la sección de su plataforma, el inicio rápido y la solución de problemas en menos de 30 segundos usando la navegación del documento.
- **SC-003**: Al menos 90% de las instrucciones ejecutables incluyen una señal observable de éxito o un siguiente paso cuando la acción falla.
- **SC-004**: Al menos 4 de 5 personas que completan la instalación pueden ejecutar el inicio rápido y localizar sus resultados en menos de 15 minutos, excluyendo el tiempo de descarga de requisitos.
- **SC-005**: La revisión de contenido no encuentra instrucciones de instalación o uso que contradigan los comandos, requisitos, formatos o comportamiento vigente del proyecto.
- **SC-006**: En una revisión con usuarios principiantes, al menos 80% califica la guía como clara y suficiente para repetir la instalación y el primer uso sin acompañamiento.
- **SC-007**: Una revisión de equivalencia encuentra el mismo 100% de los pasos críticos, comandos, advertencias y enlaces funcionales en español e inglés tanto en la guía como en el README.
- **SC-008**: Al menos 90% de los usuarios de prueba puede cambiar de idioma y llegar a la sección equivalente en menos de 30 segundos.
- **SC-009**: El 100% de los revisores puede localizar desde el README la guía bilingüe y saltar desde el índice de cualquiera de los dos documentos a cada sección principal en menos de 30 segundos.

## Assumptions

- La guía acompañará al README técnico existente y no sustituirá la referencia completa de parámetros y capacidades.
- La primera versión cubrirá los sistemas de escritorio Windows, macOS y Linux; no incluirá dispositivos móviles ni despliegues remotos.
- Las instrucciones se basarán en los requisitos y comandos oficialmente soportados por la versión del proyecto durante su implementación; la instalación principal seguirá el flujo local `pip install .` definido por el paquete.
- La instalación directa con `pip` desde una URL remota o desde artefactos publicados no será el recorrido principal de esta versión; podrá mencionarse solo como contexto si ya está respaldada por la documentación vigente.
- Los usuarios tendrán acceso a Internet para obtener el proyecto y sus requisitos, además de permisos para trabajar en una carpeta de usuario.
- El inicio rápido utilizará datos de ejemplo seguros y pequeños, o describirá cómo obtenerlos si el repositorio ya los proporciona.
- Ubuntu/Debian será la ruta Linux validada paso a paso; para otras distribuciones se ofrecerá orientación general y se explicará cómo identificar incompatibilidades, sin prometer una receta detallada para cada distribución.
- La documentación se actualizará junto con cambios que alteren la instalación, el primer uso o los problemas frecuentes cubiertos por esta especificación.
- Cada documento será bilingüe dentro de su propio archivo, con secciones claramente separadas en español e inglés; no se crearán versiones independientes que puedan divergir silenciosamente.
- La traducción conservará los nombres de comandos, opciones, rutas y mensajes técnicos exactamente cuando deban copiarse en una terminal.
- Los índices podrán ser tablas de contenido manuales o equivalentes generados por el formato Markdown, siempre que sus enlaces internos funcionen en el visor principal del repositorio.
