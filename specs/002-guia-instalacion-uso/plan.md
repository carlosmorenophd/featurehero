# Implementation Plan: Guía de instalación y uso para principiantes

**Branch**: `002-guia-instalacion-uso` | **Date**: 2026-11-22 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/002-guia-instalacion-uso/spec.md`

**Note**: This template is filled in by the `$speckit-plan` command; its definition describes the execution workflow.

## Summary

Crear una guía independiente en Markdown para que personas con poca experiencia
puedan descargar el repositorio, instalar el paquete localmente con `pip install .`,
verificar el CLI y completar un primer flujo de uso en Windows, macOS y Linux.
La guía se añadirá como `INSTALLATION_GUIDE.md` en la raíz y se enlazará desde
`README.md` en ambos idiomas. Tanto el README como la guía tendrán índices
bilingües con enlaces internos a sus secciones equivalentes; Poetry se documentará
únicamente como alternativa de desarrollo.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python `>=3.12,<4.0`; documentación Markdown

**Primary Dependencies**: Dependencias existentes declaradas en `pyproject.toml`; no se añadirán dependencias de ejecución

**Storage**: No aplica al documento; la aplicación usa archivos de entrada y resultados locales

**Testing**: `poetry run pytest`, comprobaciones del CLI (`--help`, `version`, comandos principales) y revisión multiplataforma de instrucciones

**Target Platform**: Windows, macOS y Ubuntu/Debian; orientación general para otras distribuciones Linux

**Project Type**: Aplicación CLI Python con documentación para usuarios principiantes

**Performance Goals**: No introducir cambios en el rendimiento de ejecución; el inicio rápido debe usar datos pequeños y parámetros reducidos cuando ejecute optimización

**Constraints**: Mantener comandos y comportamiento públicos; documentar primero la instalación local desde el repositorio; no prometer soporte detallado fuera de Ubuntu/Debian; evitar contradicciones entre `README.md` y `INSTALLATION_GUIDE.md`; mantener índices y enlaces internos funcionales en español e inglés

**Scale/Scope**: Un documento de instalación y primer uso bilingüe, un README bilingüe actualizado, índices en ambos documentos, tres recorridos de plataforma, un inicio rápido, solución de problemas y enlaces a la referencia técnica; sin cambios de runtime

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The plan passes the constitution gate:

- Developer-focused tooling: la guía explica el uso explícito y scriptable del CLI
  sin introducir una interfaz de usuario nueva.
- Performance and optimization: no se modifica el camino de ejecución ni la lógica
  de procesamiento; el ejemplo usa entradas pequeñas para validación.
- Functional and measurable objectives: los artefactos y validaciones trazan a
  FR-001–FR-020 y SC-001–SC-009.
- Specification fidelity and minimal scope: el cambio se limita a la guía, su
  enlace, contratos de uso y validaciones documentales.
- Critical improvement and delivery efficiency: se reutiliza la estructura actual
  y el flujo de empaquetado existente, sin añadir dependencias ni refactorizar código.

## Project Structure

### Documentation (this feature)

```text
specs/002-guia-instalacion-uso/
├── plan.md              # This file ($speckit-plan command output)
├── research.md          # Phase 0 output ($speckit-plan command)
├── data-model.md        # Phase 1 output ($speckit-plan command)
├── quickstart.md        # Phase 1 output ($speckit-plan command)
├── contracts/           # Phase 1 output ($speckit-plan command)
└── tasks.md             # Phase 2 output ($speckit-tasks command - NOT created by $speckit-plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
INSTALLATION_GUIDE.md        # Guía bilingüe, índice y recorridos de instalación/uso
README.md                     # README bilingüe, índice y enlace a la guía
featurehero/                 # CLI y lógica existente; sin cambios de runtime
tests/                       # Pruebas existentes y validaciones de humo
specs/002-guia-instalacion-uso/  # Especificación y artefactos de diseño
```

**Structure Decision**: Mantener el proyecto Python CLI existente sin crear
directorios de aplicación ni dependencias nuevas. La guía se ubicará en la raíz
para que sea visible junto al README y pueda enlazarse desde sus secciones en
español e inglés. Cada documento tendrá un índice por idioma con enlaces internos
a las secciones principales. Los artefactos de diseño permanecerán dentro de la
feature.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | La feature permanece dentro del proyecto y solo agrega documentación y validación. |
