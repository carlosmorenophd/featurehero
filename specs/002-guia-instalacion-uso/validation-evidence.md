# Validation Evidence: Bilingual Installation and Usage Guide

This file records validation evidence required by the implementation plan.

| Platform | Shell | Language | Command or scenario | Date | Result | Observations | Success criterion |
|---|---|---|---|---|---|---|---|
| Ubuntu 26.04 | Bash | Spanish | `python3 --version`, local install, `featurehero --help`, `featurehero version` | 2026-11-22 | PASS | Python 3.14.4; package installed from the repository; version reported `2026.2.1.10` | SC-001, SC-002, SC-007, SC-008, SC-009 |
| Ubuntu 26.04 | Bash | English | README and guide index/link review | 2026-11-22 | PASS | English headings, indexes, language links, and README-to-guide links reviewed | SC-002, SC-007, SC-008, SC-009 |
| Ubuntu 26.04 | Bash | Spanish/English | `poetry check`, `poetry run pytest -q`, CLI help, CLI version, `poetry build` | 2026-11-22 | PASS | `9 passed`; package build produced sdist and wheel | SC-005, SC-007 |
| Ubuntu 26.04 | Bash | Spanish/English | `featurehero transform` with a temporary four-row CSV | 2026-11-22 | PASS | `processed.csv` was created with the `log1p` transformation | SC-003, SC-004 |
| Windows PowerShell | PowerShell | Spanish/English | Full installation and usage walkthrough | 2026-11-22 | NOT RUN | Windows is not available in the current execution environment | SC-001, SC-007, SC-008, SC-009 |
| Windows CMD | CMD | Spanish/English | Full installation and usage walkthrough | 2026-11-22 | NOT RUN | Windows is not available in the current execution environment | SC-001, SC-007, SC-008, SC-009 |
| macOS | Terminal | Spanish/English | Full installation and usage walkthrough | 2026-11-22 | NOT RUN | macOS is not available in the current execution environment | SC-001, SC-007, SC-008, SC-009 |

## Required validation matrix

- Windows PowerShell
- Windows CMD
- macOS
- Ubuntu/Debian

Other Linux distributions are guidance-only unless a separate record is added.
