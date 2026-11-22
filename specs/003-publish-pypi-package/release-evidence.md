# Release Evidence: Feature Hero PyPI

Use this record for each release. Never write the value of `PYPI_TOKEN` here.

## Scope matrix

| Area | Evidence | Result |
|---|---|---|
| Package name | `featurehero` | Pending |
| Version | `pyproject.toml`, release tag, and `featurehero version` | `2026.2.1.14` locally; PyPI pending |
| Commit | Approved Git commit | Pending |
| Artifacts | One wheel and one source distribution | Pending |
| Metadata | Name, version, Python requirement, entry point, dependencies | Pending |
| Platforms | Windows PowerShell, Windows CMD, macOS, Ubuntu/Debian | Pending |
| Publication identity | GitHub secret `PYPI_TOKEN` or configured Trusted Publisher; record only the configuration type | `PYPI_TOKEN` configured externally; value not recorded |
| Verification | Clean installation and CLI smoke checks | Pending |

## Release record

- Version: `2026.2.1.14`
- Commit:
- Tag:
- PyPI URL:
- Date:
- Workflow run:

## Artifact and dependency checks

- [x] `poetry check` passed
- [x] Tests passed (`9 passed`)
- [x] Wheel metadata matches `pyproject.toml`
- [x] Source distribution metadata matches `pyproject.toml`
- [x] Packaged dependencies match declared dependencies
- [ ] Clean installation resolved all dependencies from PyPI
- [x] Duplicate-version check passed; project does not exist yet

## Platform verification

| Platform | Python | Install command | `--help` | `version` | Result/exception |
|---|---|---|---|---|---|
| Windows PowerShell | | | | | |
| Windows CMD | | | | | |
| macOS | | | | | |
| Ubuntu/Debian | | | | | |

## Failure and recovery evidence

- Duplicate version rejected:
- Missing or incomplete artifact rejected:
- Dependency resolution failure:
- Missing PyPI permission or secret:
- Post-publication verification failure and recovery:

## Security review

- [x] No token or password is present in source files.
- [x] No token or password is present in generated distributions.
- [x] No token value is recorded in this file or workflow logs.
- [ ] The GitHub environment or PyPI publisher configuration is protected.
