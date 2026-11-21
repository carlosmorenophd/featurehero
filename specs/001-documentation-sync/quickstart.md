# Quickstart: Validate Documentation Synchronization

## Prerequisites

- Python `>=3.12,<4.0`.
- Poetry installed.
- Repository checked out on branch `001-documentation-sync`.

## Validation sequence

1. Install the existing development environment:

   ```bash
   poetry install
   ```

2. Run the automated tests:

   ```bash
   poetry run pytest -q
   ```

   Expected result: all existing tests pass.

3. Verify the public CLI surface:

   ```bash
   poetry run featurehero --help
   poetry run featurehero run --help
   poetry run featurehero transform --help
   poetry run featurehero analyze-results --help
   poetry run featurehero jobs --help
   poetry run featurehero version
   ```

4. Cross-check documentation against the source contract in
   [`contracts/cli-documentation.md`](contracts/cli-documentation.md), the
   implementation under `featurehero/`, and the tests under `tests/`.

5. Confirm that `README.md` contains the three permanent layers: basic usage and
   commands, application summary, and technical reference.

6. Audit tracked files for credentials, private configuration, caches, and
   unnecessary generated content. Remove only candidates with evidence, and
   record each disposition in the implementation handoff.

7. At feature closure, confirm `IA_ARCHITECTURE.md` and
   `README/IA_ACTION_01.md` are absent from the working tree and Git index, then
   rerun steps 2 and 3.
