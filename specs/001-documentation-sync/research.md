# Research: Project Documentation and Repository Synchronization

## Decision 1: Treat executable source as the authority

- **Decision**: Document behavior from `featurehero/`, `tests/`, `pyproject.toml`,
  and the release configuration. Existing IA documents are reconciled against
  that evidence.
- **Rationale**: The feature requires documenting what is implemented, not what
  earlier plans proposed. This prevents unsupported behavior from becoming part
  of the permanent README.
- **Alternatives considered**: Treating the existing IA documents as authoritative
  was rejected because `README/IA_ACTION_01.md` contains planned-work language
  even though the analyzer is now implemented.

## Decision 2: Use README.md as the permanent three-layer reference

- **Decision**: Preserve three sections in `README.md`: basic usage and commands,
  an application summary, and the relevant technical reference.
- **Rationale**: This directly resolves clarification Q3 while keeping the public
  entry point useful for both operators and maintainers.
- **Alternatives considered**: Keeping all detail only in the spec was rejected
  because the README is the documented entry point for the installed CLI.

## Decision 3: Keep cleanup evidence-based

- **Decision**: Remove the two requested IA documents at closure. Remove any
  additional tracked file only when the audit demonstrates a security risk or
  unnecessary generated content. Preserve source and reproducibility files.
- **Rationale**: A suspicious filename is not proof of sensitive content, and the
  constitution requires minimal, functional changes.
- **Alternatives considered**: Removing every file with a key, cache, or artifact
  name was rejected as unsafe and overly broad.

## Decision 4: Validate with existing behavior checks

- **Decision**: Use the existing pytest suite, CLI help/version smoke checks, and
  a source-to-document cross-review. No new runtime dependency or application
  test behavior is required by this documentation-only feature.
- **Rationale**: The feature must prove that cleanup did not alter the application
  while keeping the implementation minimal.
- **Alternatives considered**: Adding new application tests or refactoring code
  for documentation purposes was rejected as outside the specification.
