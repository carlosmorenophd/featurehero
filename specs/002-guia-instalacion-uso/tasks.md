---

description: "Task list for the bilingual installation and usage documentation"
---

# Tasks: Guía bilingüe de instalación y uso

**Input**: Design documents from `/specs/002-guia-instalacion-uso/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Organization**: Tasks are grouped by user story so each story can be implemented and validated independently.

## Phase 1: Setup (Shared Documentation Structure)

**Purpose**: Establish the bilingual document structure and source-of-truth references.

- [ ] T001 Review `README.md`, `pyproject.toml`, `featurehero/main.py`, `.github/workflows/release.yml`, and `specs/002-guia-instalacion-uso/contracts/cli-usage.md` to record the commands, requirements, package metadata, and output behavior that documentation must preserve.
- [ ] T002 Create the bilingual document skeleton in `INSTALLATION_GUIDE.md` with clearly separated Spanish and English sections, language links, and stable headings for platform setup, installation, quickstart, troubleshooting, and technical reference.
- [ ] T003 Define the shared heading, anchor, terminology, and language-switch conventions in `README.md` and `INSTALLATION_GUIDE.md` so equivalent sections can be linked and compared reliably.

---

## Phase 2: Foundational (Blocking Documentation Prerequisites)

**Purpose**: Establish shared content rules before implementing individual user stories.

**⚠️ CRITICAL**: Complete this phase before user-story documentation work.

- [ ] T004 Verify the installation and CLI facts used by both documents against `pyproject.toml`, `README.md`, `featurehero/main.py`, and `specs/002-guia-instalacion-uso/contracts/cli-usage.md`, including Python `>=3.12,<4.0`, local `pip install .`, optional Poetry development setup, `featurehero --help`, and `featurehero version`.
- [ ] T005 Define the Spanish-to-English parity checklist in `specs/002-guia-instalacion-uso/quickstart.md` for commands, requirements, warnings, links, headings, and scope boundaries.
- [ ] T006 Prepare the shared navigation targets in `README.md` and `INSTALLATION_GUIDE.md`, including one index per language and visible links between the equivalent language sections and documents.

**Checkpoint**: Shared facts, terminology, anchors, and navigation targets are ready for story implementation.

---

## Phase 3: User Story 1 - Instalar desde cero en cualquier plataforma (Priority: P1) 🎯 MVP

**Goal**: A beginner can choose a language and platform, download the repository, install the local package, and verify the CLI.

**Independent Test**: A reviewer can follow one language section of `INSTALLATION_GUIDE.md` on Windows, macOS, or Ubuntu/Debian and complete installation without consulting undocumented steps.

### Implementation for User Story 1

- [ ] T007 [US1] Write the complete Spanish installation path in `INSTALLATION_GUIDE.md`, covering platform identification, Python requirement, repository download, project-root navigation, isolated environment creation, activation, `python -m pip install .`, optional Poetry development setup, and success signals.
- [ ] T008 [US1] Write the complete English installation path in `INSTALLATION_GUIDE.md` with the same steps, commands, warnings, optional Poetry path, and success signals as the Spanish path.
- [ ] T009 [US1] Add the complete Spanish README content, index, platform orientation, technical reference, and visible link to the Spanish guide section in `README.md`.
- [ ] T010 [US1] Add the complete English README content, table of contents, platform orientation, technical reference, and visible link to the English guide section in `README.md`.
- [ ] T011 [US1] Add separate PowerShell and Windows CMD activation instructions plus macOS and Ubuntu/Debian command variants in `INSTALLATION_GUIDE.md`, preserving equivalent Spanish and English sections.
- [ ] T012 [US1] Validate the installation walkthrough and README links against `specs/002-guia-instalacion-uso/contracts/cli-usage.md` and `specs/002-guia-instalacion-uso/quickstart.md` on the supported platform paths.

**Checkpoint**: The bilingual installation MVP is independently usable and navigable from `README.md`.

---

## Phase 4: User Story 2 - Ejecutar el primer flujo de uso (Priority: P1)

**Goal**: A newly installed user can create or use a small valid dataset, run the first transformation and main flow, and locate the outputs in either language.

**Independent Test**: After completing US1, a reviewer can follow either language's quickstart and identify the expected input, command, output, and next reference.

### Implementation for User Story 2

- [ ] T013 [US2] Write the Spanish quickstart in `INSTALLATION_GUIDE.md`, including a small valid CSV example, `featurehero transform`, the main `featurehero run` flow with reduced parameters, expected outputs, and links to the Spanish README reference.
- [ ] T014 [US2] Write the English quickstart in `INSTALLATION_GUIDE.md` with equivalent data requirements, commands, outputs, and links to the English README reference.
- [ ] T015 [US2] Complete the Spanish README usage and technical-reference sections in `README.md`, covering `run`, `transform`, `analyze-results`, `jobs`, `version`, supported input formats, outputs, troubleshooting links, and the Spanish guide quickstart.
- [ ] T016 [US2] Complete the English README usage and technical-reference sections in `README.md` with equivalent commands, input rules, outputs, troubleshooting links, and the English guide quickstart.
- [ ] T017 [US2] Cross-check the bilingual quickstart against `specs/002-guia-instalacion-uso/contracts/cli-usage.md`, `specs/002-guia-instalacion-uso/data-model.md`, and the implemented CLI in `featurehero/main.py`; correct unsupported commands or nonexistent example paths.

**Checkpoint**: The bilingual first-use flow is independently runnable after US1.

---

## Phase 5: User Story 3 - Resolver problemas frecuentes y continuar aprendiendo (Priority: P2)

**Goal**: A user can recover from common setup or usage failures and continue to the appropriate technical reference in either language.

**Independent Test**: A reviewer can locate a symptom, corrective action, verification step, and escalation path from either language's troubleshooting index.

### Implementation for User Story 3

- [ ] T018 [US3] Write the Spanish troubleshooting section in `INSTALLATION_GUIDE.md` for missing Python, unrecognized commands, environment activation, permissions, paths, unsupported formats, invalid columns, and incomplete installation.
- [ ] T019 [US3] Write the English troubleshooting section in `INSTALLATION_GUIDE.md` with equivalent symptoms, causes, corrective actions, verification steps, and escalation guidance.
- [ ] T020 [US3] Add Spanish README troubleshooting links, scope boundaries, and technical-reference navigation in `README.md`.
- [ ] T021 [US3] Add English README troubleshooting links, scope boundaries, and technical-reference navigation in `README.md`.
- [ ] T022 [US3] Perform a complete Spanish-English parity audit across `README.md` and `INSTALLATION_GUIDE.md`, comparing commands, requirements, warnings, links, headings, scope, and troubleshooting entries; record and correct every discrepancy.

**Checkpoint**: Users can recover from common failures and reach the correct technical reference independently in both languages.

---

## Phase 6: Polish & Cross-Cutting Validation

**Purpose**: Verify the complete documentation feature against the specification and existing project behavior.

- [ ] T023 Create `specs/002-guia-instalacion-uso/validation-evidence.md` with platform, shell, language, command or scenario, date, result, observations, and related success criterion fields.
- [ ] T024 [P] Validate every internal link, language switch, README-to-guide link, and index destination in `README.md` and `INSTALLATION_GUIDE.md`.
- [ ] T025 Run `poetry check`, `poetry run pytest`, `poetry run featurehero --help`, `poetry run featurehero version`, and `poetry build` from `specs/002-guia-instalacion-uso/quickstart.md` and record the outcomes in `specs/002-guia-instalacion-uso/validation-evidence.md`.
- [ ] T026 Review `README.md` and `INSTALLATION_GUIDE.md` against `specs/002-guia-instalacion-uso/spec.md`, `specs/002-guia-instalacion-uso/contracts/cli-usage.md`, and the constitution; remove unsupported claims and unrequested content.
- [ ] T027 Execute the complete platform and bilingual walkthrough from `specs/002-guia-instalacion-uso/quickstart.md` for the mandatory matrix of Windows PowerShell, Windows CMD, macOS, and Ubuntu/Debian; record every result in `specs/002-guia-instalacion-uso/validation-evidence.md`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; establishes the document structure.
- **Foundational (Phase 2)**: Depends on Phase 1; blocks all user-story work.
- **User Story 1 (Phase 3)**: Depends on Phase 2 and is the MVP.
- **User Story 2 (Phase 4)**: Depends on US1 installation and can then be validated independently.
- **User Story 3 (Phase 5)**: Depends on US1 and US2 terminology and links so troubleshooting points to valid content.
- **Polish (Phase 6)**: Depends on all selected user stories.

### User Story Dependencies

- **US1 (P1)**: No dependency on another story after the foundational phase.
- **US2 (P1)**: Depends on US1's verified installation path.
- **US3 (P2)**: Depends on the documented terms and links from US1 and US2.

### Parallel Opportunities

- T007–T010 must run sequentially or through coordinated ownership because they modify the shared `README.md` and `INSTALLATION_GUIDE.md` files.
- T013–T016 must run sequentially or through coordinated ownership because they modify shared bilingual documents.
- T018–T021 must run sequentially or through coordinated ownership because they modify shared bilingual documents.
- T023 must complete before T025 and T027; T024 can run in parallel with T025 once the relevant documents are stable.

---

## Parallel Example: User Story 1

```text
Task: T007 [US1] Write the Spanish installation path in INSTALLATION_GUIDE.md
Task: T008 [US1] Write the English installation path in INSTALLATION_GUIDE.md
Task: T009 [US1] Add the complete Spanish README content in README.md
Task: T010 [US1] Add the complete English README content in README.md
```

These tasks use shared files and therefore must be executed sequentially or with
explicit ownership and merge coordination; the shared heading and anchor
conventions from T003 must remain unchanged.

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational documentation rules.
3. Complete Phase 3: User Story 1.
4. Validate installation, indexes, language switching, and README-to-guide links.
5. Stop and review the bilingual installation MVP before adding usage details.

### Incremental Delivery

1. Add US1 for bilingual installation and navigation.
2. Add US2 for bilingual first use and CLI reference.
3. Add US3 for bilingual troubleshooting and technical-reference links.
4. Complete Phase 6 cross-cutting validation.

## Notes

- Every task uses the required checklist format with a sequential ID and explicit file path.
- `[P]` marks tasks that can be performed in parallel when shared-file conflicts are coordinated.
- No runtime code or new dependencies are required by this feature.
- The final result must keep Spanish and English content equivalent and navigable.
