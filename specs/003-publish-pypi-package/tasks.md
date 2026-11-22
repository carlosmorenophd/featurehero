---

description: "Task list for publishing Feature Hero to PyPI"
---

# Tasks: Publicar Feature Hero para instalación con pip

**Input**: Design documents from `/specs/003-publish-pypi-package/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/pypi-release.md`, and `quickstart.md`

**Organization**: Tasks are grouped by user story so each increment can be implemented and validated independently.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the release and documentation files that the feature will modify.

- [x] T001 Confirm the release scope and define the evidence matrix for version, commit, artifacts, platforms, Python versions, commands, results, and exceptions in `specs/003-publish-pypi-package/release-evidence.md`
- [x] T002 [P] Create the minimal release-validation command structure under `.github/scripts/` without changing runtime modules in `featurehero/`
- [x] T003 [P] Create the single evidence template `specs/003-publish-pypi-package/release-evidence.md` before release work begins, including sections for scope, version, commit, artifacts, platforms, Python versions, commands, results, and exceptions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Provide common package and release invariants before the user stories are completed.

**⚠️ CRITICAL**: User-story work depends on these package invariants and validation conventions.

- [x] T004 Define the package invariant checks in `.github/scripts/validate_release.py` for distribution name `featurehero`, Python requirement `>=3.12,<4.0`, entry point `featurehero = "featurehero.main:main"`, and exact parity between declared and packaged runtime dependencies
- [x] T005 Implement artifact checks in `.github/scripts/validate_release.py` requiring a version-matching wheel and source distribution when both are generated, with no missing or duplicate release version
- [x] T006 Add the pre-publication validation sequence to `.github/scripts/validate_release.py` for `poetry check`, `poetry run pytest -q`, `poetry build`, `poetry run featurehero --help`, and `poetry run featurehero version`

**Checkpoint**: Shared metadata, artifact, and pre-publication validation rules are defined.

---

## Phase 3: User Story 1 - Instalar desde PyPI sin descargar el repositorio (Priority: P1) 🎯 MVP

**Goal**: Make the public package installable with pip and verify that the installed CLI works without the source repository.

**Independent Test**: In a clean compatible environment outside the repository, run `python -m pip install featurehero`, then run `featurehero --help` and `featurehero version`; the reported version must match the installed distribution metadata.

### Implementation for User Story 1

- [x] T007 [US1] Align package metadata in `pyproject.toml` with the public installation contract: distribution name `featurehero`, Python `>=3.12,<4.0`, runtime dependencies, README metadata, and entry point `featurehero = "featurehero.main:main"`
- [x] T008 [US1] Add a clean-environment installation verification command in `.github/scripts/verify_pypi_install.py` that installs `featurehero` from the public index outside the repository and checks package metadata, `featurehero --help`, and `featurehero version`
- [x] T009 [US1] Make `.github/scripts/verify_pypi_install.py` report platform, Python version, installed version, command results, and actionable failures for unsupported Python versions, dependency resolution errors, missing PATH entry, or absent CLI output
- [ ] T010 [US1] Validate the public installation flow from `specs/003-publish-pypi-package/quickstart.md` in a clean environment without importing code from the repository

**Checkpoint**: A published `featurehero` package can be installed and its CLI can be verified independently of the repository.

---

## Phase 4: User Story 2 - Publicar una versión instalable y verificable (Priority: P1)

**Goal**: Build, validate, and publish a unique approved version with wheel and source distribution using protected PyPI publishing.

**Independent Test**: A clean approved commit produces validated artifacts, the release workflow publishes them to PyPI with protected OIDC permissions, and a clean installation reports the expected version.

### Implementation for User Story 2

- [x] T011 [US2] Increment the release version in `pyproject.toml` using the required `yyyy.mayor.minor.micro` format and ensure the release tag, package metadata, and CLI version all use that same value
- [x] T012 [US2] Update `.github/workflows/release.yml` to run tests, compile checks, Poetry validation, metadata/artifact validation, and CLI smoke checks before any publication step
- [x] T013 [US2] Add distribution integrity validation to `.github/workflows/release.yml` using the generated wheel and source distribution, rejecting missing artifacts, invalid metadata, duplicate versions, or a version different from `pyproject.toml`
- [x] T014 [US2] Configure the protected GitHub `pypi` environment and verify the external PyPI publisher or `PYPI_TOKEN` repository secret, then configure `.github/workflows/release.yml` without storing the credential value in the repository
- [x] T015 [US2] Publish the validated `dist/*.whl` and `dist/*.tar.gz` artifacts in `.github/workflows/release.yml` with the official PyPA PyPI publishing action while preserving the existing GitHub Release upload
- [x] T016 [US2] Add a post-publication verification job to `.github/workflows/release.yml` that retries the public-index lookup every 15 seconds for at most 5 minutes, fails with an identifiable result if the version is absent, then installs the released version in a clean environment and runs `featurehero --help` and `featurehero version`
- [x] T017 [US2] Complete `specs/003-publish-pypi-package/release-evidence.md` with Trusted Publisher configuration, duplicate-version rejection, incomplete-artifact failure, dependency-resolution results, missing publishing permission, and failed post-publication verification recovery guidance

**Checkpoint**: An approved version is published only after validation and can be installed and verified from PyPI.

---

## Phase 5: User Story 3 - Mantener documentación y rutas de desarrollo coherentes (Priority: P2)

**Goal**: Make the public pip route obvious in Spanish and English while preserving clearly separated source and Poetry development routes.

**Independent Test**: A documentation review finds equivalent bilingual instructions, a README index linking to the guide, the public pip command as the primary route, and non-conflicting source/Poetry alternatives.

### Implementation for User Story 3

- [x] T018 [P] [US3] Update the Spanish sections and table of contents in `README.md` with `python -m pip install featurehero`, requirements, CLI verification, troubleshooting, and links to the Spanish installation guide sections
- [x] T019 [P] [US3] Update the English sections and table of contents in `README.md` with `python -m pip install featurehero`, requirements, CLI verification, troubleshooting, and links to the English installation guide sections
- [x] T020 [P] [US3] Add or update the Spanish installation and usage sections in `INSTALLATION_GUIDE.md` for Windows PowerShell, Windows CMD, macOS, and Ubuntu/Debian, including public pip, source, Poetry, verification, and recovery routes
- [x] T021 [P] [US3] Add or update the English installation and usage sections in `INSTALLATION_GUIDE.md` for Windows PowerShell, Windows CMD, macOS, and Ubuntu/Debian, including public pip, source, Poetry, verification, and recovery routes
- [x] T022 [US3] Cross-check `README.md` and `INSTALLATION_GUIDE.md` for equivalent bilingual commands, package name, CLI name, Python requirement, version verification, links, and warnings before release

**Checkpoint**: End users see PyPI as the primary route, while contributors can still follow source and Poetry development instructions.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validate the complete feature and preserve the existing CLI contract.

- [x] T023 [P] Run the existing test suite in `tests/` and confirm no public CLI command, parameter, or input/output format changed
- [ ] T024 [P] Run the release validation and clean-install scenarios from `specs/003-publish-pypi-package/quickstart.md` on Windows PowerShell, Windows CMD, macOS, and Ubuntu/Debian, recording any unsupported platform explicitly in `specs/003-publish-pypi-package/release-evidence.md`
- [x] T025 Scan `.github/workflows/release.yml`, `.github/scripts/`, `pyproject.toml`, generated distributions, and Git history for PyPI tokens, passwords, or private credentials before release
- [x] T026 Verify that the final README and installation guide links, indexes, commands, and version references are consistent with the published package and `specs/003-publish-pypi-package/contracts/pypi-release.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; establishes the files and scope.
- **Foundational (Phase 2)**: Depends on Setup and blocks user-story implementation.
- **User Story 1 (Phase 3)**: Depends on Foundational; delivers the MVP installation and CLI verification path.
- **User Story 2 (Phase 4)**: Depends on Foundational and the US1 verification command; publishes the version consumed by US1.
- **User Story 3 (Phase 5)**: Depends on the final package command and can be developed in parallel with US1/US2 after the public commands are fixed.
- **Polish (Phase 6)**: Depends on all required user stories and the release candidate.

### User Story Dependencies

- **US1 (P1)**: Depends on Phase 2; no dependency on documentation completion.
- **US2 (P1)**: Depends on Phase 2 and integrates the US1 clean-install verifier into the release workflow.
- **US3 (P2)**: Depends on the final public package name and commands; otherwise independent of release implementation.

### Parallel Opportunities

- T002 and T003 can run in parallel during Setup.
- T018, T019, T020, and T021 can run in parallel because each targets a distinct language section/file region.
- T023 and T024 can run in parallel after the release candidate exists.
- US3 documentation work can proceed in parallel with US1 package verification and US2 workflow work once the public command contract is fixed.

## Parallel Example: User Story 1

```text
Task T007: Align pyproject.toml metadata and entry point
Task T008: Implement the clean PyPI installation verifier in .github/scripts/verify_pypi_install.py
```

T009 follows T008, and T010 follows T007-T009 because it validates the complete public installation path.

## Parallel Example: User Story 3

```text
Task T018: Update Spanish README sections
Task T019: Update English README sections
Task T020: Update Spanish installation guide sections
Task T021: Update English installation guide sections
```

T022 follows all four documentation edits and performs the parity review.

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup and Foundational phases.
2. Complete US1 package metadata and clean-install verification.
3. Publish or use a test release in a clean environment.
4. Validate `python -m pip install featurehero`, `featurehero --help`, and `featurehero version` without the repository.

### Incremental Delivery

1. Add US1 to establish the installable package contract.
2. Add US2 to automate validated PyPI publication and post-publication verification.
3. Add US3 to synchronize bilingual end-user and contributor documentation.
4. Run the cross-platform and security checks before declaring the version ready.

## Notes

- Every task follows the required checklist format with a sequential ID and exact file path.
- `[P]` marks tasks that can be performed in parallel without editing the same incomplete dependency.
- No runtime business logic changes are planned under `featurehero/`.
- The feature branch remains open until the user explicitly requests closure.
