# Feature Specification: Project Documentation and Repository Synchronization

**Feature Branch**: `001-documentation-sync`

**Created**: 2026-11-21

**Status**: Draft

**Input**: User description: "001 documentar todo lo de IA en los .md, leer el codigo, documentar lo hecho y preparar la sincronizacion; al finalizar eliminar los documentos de IA y retirar archivos que por seguridad no deben ir al repositorio"

## Clarifications

### Session 2026-11-21

- Q: Después de eliminar `IA_ARCHITECTURE.md` y `README/IA_ACTION_01.md`, ¿dónde debe conservarse la documentación consolidada? → A: Migrarla también a `README.md` antes de eliminar los archivos IA.
- Q: ¿Qué archivos deben eliminarse durante la auditoría de seguridad y limpieza del repositorio? → A: Eliminar solo archivos rastreados con evidencia de riesgo o generación innecesaria.
- Q: ¿Qué nivel de detalle debe conservarse en `README.md` después de eliminar los documentos IA? → A: Incluir una guía de uso y comandos básicos, un resumen de la aplicación y los aspectos técnicos relevantes.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Understand the implemented system (Priority: P1)

As a developer or maintainer, I want the current behavior of the project to be
documented in one consistent technical reference so that I can understand what
already exists before starting another specification.

**Why this priority**: The project must have a reliable baseline before any
future work is specified or implemented.

**Independent Test**: A maintainer can read the technical reference and identify
the CLI capabilities, supported input data, processing flow, model options,
outputs, validations, and current test coverage without inspecting every source
file first.

**Acceptance Scenarios**:

1. **Given** the current source tree, **When** a maintainer reads the technical
   reference, **Then** every public command and implemented processing area is
   represented with its current behavior and limitations.
2. **Given** an implemented behavior is not supported or is unavailable,
   **When** it is documented, **Then** it is explicitly marked as unavailable
   rather than described as planned functionality.

### User Story 2 - Keep the documentation synchronized (Priority: P1)

As a developer, I want the architecture reference and the IA action document to
describe the same current system so that they do not provide conflicting guidance.

**Why this priority**: Conflicting documentation causes incorrect changes and
breaks the project rule of working only from an accurate specification.

**Independent Test**: A reviewer compares both documents against the source tree
and finds no contradictory command names, file paths, supported formats,
processing stages, outputs, or claims about completed work.

**Acceptance Scenarios**:

   1. **Given** the current code and existing documents, **When** the documentation
   is synchronized, **Then** `IA_ARCHITECTURE.md` contains the complete technical
   inventory, `README/IA_ACTION_01.md` records the relevant completed action, and
   `README.md` receives a basic usage guide, an application summary, and the
   relevant technical reference needed after cleanup.
2. **Given** a documented command or output, **When** it is checked against the
   CLI and service code, **Then** its name, input, output, and validation rules
   match the implementation.

### User Story 3 - Close the documentation-only feature safely (Priority: P2)

As a repository maintainer, I want the temporary IA documents and unsafe tracked
artifacts removed only after the documentation is complete and reviewed so that
the repository ends in a clean, safe state without deleting source functionality.

**Why this priority**: Cleanup is required by this feature, but it must not
precede the synchronization or remove valid project code.

**Independent Test**: After the final cleanup, the two temporary IA documents are
absent, no confirmed sensitive or generated artifact remains tracked, source files
remain intact, and the repository history records the cleanup as part of this
feature.

**Acceptance Scenarios**:

1. **Given** both documentation artifacts are complete, **When** the feature is
   closed, **Then** `IA_ARCHITECTURE.md` and `README/IA_ACTION_01.md` are removed
   from the working tree and Git tracking.
2. **Given** a tracked file appears security-sensitive or generated, **When** it
   is audited, **Then** it is removed from Git only when evidence confirms it
   should not be versioned; source files without such evidence are preserved.
3. **Given** the cleanup is complete, **When** the project is validated, **Then**
   the existing CLI package and tests remain usable and no unrelated application
   behavior has changed.

### Edge Cases

- Documentation describes behavior that exists in comments or plans but is not
  implemented in executable code.
- A command has different behavior in the README, architecture document, and
  source code.
- A file name appears security-sensitive but contains no credentials or private
  data; it must not be removed without evidence.
- Generated distributions, caches, logs, local environments, or credentials are
  present locally but are not tracked by Git.
- A documentation statement cannot be verified from the current repository; it
  must be marked as unknown or omitted instead of presented as fact.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The documentation MUST describe the project's reason, objective,
  intended developer audience, and non-end-user scope.
- **FR-002**: The documentation MUST inventory every public CLI command currently
  implemented, including its purpose, required inputs, optional parameters,
  outputs, and validation behavior.
- **FR-003**: The documentation MUST describe the supported data formats,
  transformations, dataset preparation, target-column rules, and generated files.
- **FR-004**: The documentation MUST describe the genetic optimization flow,
  population and generation controls, feature selection behavior, mutation and
  crossover behavior, metrics, progress reporting, and export behavior that are
  present in the code.
- **FR-005**: The documentation MUST identify every implemented regression model,
  its role in optimization, and the model-specific configuration exposed by the
  project.
- **FR-006**: The documentation MUST describe background job registration,
  listing, stopping, status handling, and the local files used by that behavior.
- **FR-007**: The documentation MUST describe result analysis, including input
  contract, metric direction, elite selection, weighted relevance, cooccurrence,
  duplicate handling, warnings, and exported reports.
- **FR-008**: The documentation MUST identify current tests and the behavior they
  verify, while distinguishing tested behavior from untested behavior.
- **FR-009**: `IA_ARCHITECTURE.md` and `README/IA_ACTION_01.md` MUST be updated
  so their claims, terminology, paths, commands, and outputs are synchronized
  with the current source code. Before those files are removed, `README.md` MUST
  receive three permanent layers of content: basic usage and commands, an
  application summary, and the relevant technical reference.
- **FR-010**: Before cleanup, the repository MUST be audited for tracked
  credentials, tokens, private configuration, generated artifacts, caches, and
  other files that should not be versioned.
- **FR-011**: At feature closure, the two temporary IA documents MUST be removed
  and confirmed absent from Git. Additional files MAY be removed only when they
  are tracked and the audit provides evidence of a security risk or unnecessary
  generated content.
- **FR-012**: The cleanup MUST NOT alter application source behavior, public CLI
  contracts, dependencies, tests, or generated business results beyond the
  explicitly approved repository-hygiene changes.

### Key Entities

- **Implemented Capability**: A command, module, service, model, transformation,
  validation, job operation, or report that exists in the current source tree.
- **Documentation Reference**: A statement in either IA document that must be
  traceable to an implemented capability or explicitly marked as unavailable.
- **Repository Hygiene Candidate**: A tracked or untracked file examined for
  credentials, private data, generated output, cache content, or other material
  that should not be versioned.
- **Synchronization Baseline**: The reviewed set of source behavior, documented
  behavior, tests, and approved cleanup decisions at feature closure.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A maintainer can locate the purpose, audience, CLI commands, data
  flow, models, outputs, and validation rules in the synchronized documentation
  without needing to inspect more than the documented source references.
- **SC-002**: 100% of public CLI subcommands and documented supported data formats
  found in the source are represented accurately in the documentation.
- **SC-003**: 100% of documented completed behaviors are traceable to source code,
  tests, or an explicit unavailable-status statement.
- **SC-004**: A cross-document review finds zero contradictions in command names,
  paths, input contracts, output contracts, or completion status.
- **SC-005**: After cleanup, the two temporary IA documents are absent and every
  removed additional file has a recorded security or repository-hygiene reason.
- **SC-006**: Existing automated tests pass after the cleanup, and no application
  source file outside the explicitly approved cleanup scope is changed.

## Assumptions

- The current source tree is the authority for implemented behavior; existing
  documentation is evidence to reconcile, not authority when it conflicts with
  executable code.
- The feature is documentation and repository hygiene work; no new application
  capability is requested.
- `IA_ARCHITECTURE.md` and `README/IA_ACTION_01.md` are temporary documents that
  must be removed only after their relevant content has been incorporated into
  `README.md`, the synchronized feature record, and the review evidence.
- `README.md` is the permanent entry point and MUST combine basic usage,
  application summary, and technical reference content without claiming
  unsupported behavior.
- A file with a suspicious name alone is insufficient evidence for deletion;
  source code and reproducibility files MUST be preserved unless the audit proves
  they are unsafe or unnecessary to version.
- Existing release, packaging, and Speckit configuration remain in scope for
  inventory but are not to be redesigned by this feature.
