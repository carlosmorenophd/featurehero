# Implementation Plan: Publicar Feature Hero para instalación con pip

**Branch**: `003-publish-pypi-package` | **Date**: 2026-11-22 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/003-publish-pypi-package/spec.md`

**Note**: This template is filled in by the `$speckit-plan` command; its definition describes the execution workflow.

## Summary

Publicar los artefactos de Feature Hero en PyPI para que una persona pueda ejecutar
`python -m pip install featurehero` sin descargar el repositorio. La publicación
se integrará en el workflow de release existente después de construir y validar
el wheel y el source distribution, usando Trusted Publishing/OIDC y conservando
la ruta desde fuente para desarrollo.

La configuración externa de PyPI debe registrar un Trusted Publisher asociado al
repositorio y workflow protegidos. Después de publicar, el workflow consultará
PyPI durante un máximo de 5 minutos, con intervalos de 15 segundos, y fallará
con un resultado identificable si la versión no aparece.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python `>=3.12,<4.0`; metadata de distribución PEP 621

**Primary Dependencies**: Poetry/poetry-core para construir; PyPA GitHub Action para publicar; dependencias runtime existentes

**Storage**: PyPI para artefactos públicos; `dist/` como salida temporal del build; sin almacenamiento runtime nuevo

**Testing**: `poetry check`, `poetry run pytest`, compilación, validación de metadata y dependencias del wheel/sdist, instalación limpia desde PyPI y smoke checks del CLI

**Target Platform**: Consumidores Windows PowerShell/CMD, macOS y Ubuntu/Debian; publicación desde GitHub Actions en Ubuntu

**Project Type**: Paquete Python con aplicación CLI y distribución pública

**Performance Goals**: Instalación pública verificable en menos de 5 minutos, excluyendo descargas lentas de dependencias; sin cambios en el rendimiento del CLI

**Constraints**: Mantener comandos y parámetros públicos; usar versiones únicas; no incluir secretos; publicar solo artefactos validados del commit aprobado; configurar Trusted Publishing fuera del código; verificar la disponibilidad en PyPI con reintentos acotados; no mezclar la ruta de desarrollo con la ruta pública

**Scale/Scope**: Metadata de paquete, workflow de release, publicación PyPI, verificación de instalación y actualización bilingüe de README/guía; sin cambios de lógica de negocio

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The plan passes the constitution gate:

- Developer-focused tooling: se distribuye el mismo CLI explícito y scriptable,
  sin añadir una interfaz de usuario.
- Performance and optimization: no se modifica la ejecución de transformaciones,
  selección genética, regresión ni análisis.
- Functional and measurable objectives: las tareas trazan a FR-001–FR-014 y
  SC-001–SC-008, incluyendo build, publicación, instalación y verificación.
- Specification fidelity and minimal scope: el cambio se limita a distribución,
  release, seguridad de publicación, documentación y validación.
- Critical improvement and delivery efficiency: se reutiliza `pyproject.toml`,
  el workflow existente y la metadata actual sin agregar abstracciones runtime.

## Project Structure

### Documentation (this feature)

```text
specs/003-publish-pypi-package/
├── plan.md              # This file ($speckit-plan command output)
├── research.md          # Phase 0 output ($speckit-plan command)
├── data-model.md        # Phase 1 output ($speckit-plan command)
├── quickstart.md        # Phase 1 output ($speckit-plan command)
├── contracts/           # Phase 1 output ($speckit-plan command)
├── release-evidence.md   # Release version, platform, artifact, and result evidence
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
pyproject.toml               # Package metadata, dependencies, entry point
.github/workflows/release.yml # Build, validate, GitHub Release, and PyPI publish
README.md                    # Public installation and development documentation
INSTALLATION_GUIDE.md        # Beginner installation and usage documentation
featurehero/                 # Existing CLI and processing logic; unchanged
tests/                       # Existing automated tests
specs/003-publish-pypi-package/ # Specification and design artifacts
.github/scripts/             # Release metadata and clean-install validators
```

**Structure Decision**: Mantener el paquete y el CLI existentes. La distribución
se implementará mediante metadata y workflow de release; los validadores se
ubicarán en `.github/scripts/` y no se crearán módulos runtime nuevos. La
evidencia se conservará en `specs/003-publish-pypi-package/release-evidence.md`.
README y guía se actualizarán para priorizar PyPI y conservar
claramente la ruta de desarrollo desde fuente.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | La feature agrega publicación y validación de la distribución sin ampliar la aplicación. |
