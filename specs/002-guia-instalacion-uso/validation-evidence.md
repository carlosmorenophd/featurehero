# Validation Evidence: Bilingual Installation and Usage Guide

This file records validation evidence required by the implementation plan.

| Platform | Shell | Language | Command or scenario | Date | Result | Observations | Success criterion |
|---|---|---|---|---|---|---|---|
| Ubuntu 26.04 | Bash | Spanish | `python3 --version`, local install, `featurehero --help`, `featurehero version` | 2026-11-22 | PASS | Python 3.14.4; package installed from the repository; version reported `2026.2.1.10` | SC-001, SC-002, SC-007, SC-008, SC-009 |
| Ubuntu 26.04 | Bash | English | README and guide index/link review | 2026-11-22 | PASS | English headings, indexes, language links, and README-to-guide links reviewed | SC-002, SC-007, SC-008, SC-009 |
| Ubuntu 26.04 | Bash | Spanish/English | `poetry check`, `poetry run pytest -q`, CLI help, CLI version, `poetry build` | 2026-11-22 | PASS | `9 passed`; package build produced sdist and wheel | SC-005, SC-007 |
| Ubuntu 26.04 | Bash | Spanish/English | `featurehero transform` with a temporary four-row CSV | 2026-11-22 | PASS | `processed.csv` was created with the `log1p` transformation | SC-003, SC-004 |
| Windows PowerShell | PowerShell 5.1 | Spanish/English | Python 3.12.10 virtual environment, local install, CLI help/version, `transform`, and reduced `run` walkthrough | 2026-11-24 | PASS | Activation policy block reproduced and recovered with a process-only policy; the corrected 20-row, two-predictor example completed 10 generations with `lasso_regression` and produced workspace outputs | SC-001, SC-003, SC-004, SC-005, SC-007 |
| Windows CMD | CMD 10.0 | Spanish/English | Virtual-environment activation, CLI help/version, `transform`, and reduced `run` walkthrough | 2026-11-24 | PASS | CMD quoting for JSON was validated; `processed-cmd.csv` and optimization workspace outputs were created | SC-001, SC-003, SC-004, SC-005, SC-007 |
| macOS | Terminal | Spanish/English | Full installation and usage walkthrough | 2026-11-24 | NOT RUN | No macOS host or runner is available from the current Windows environment | SC-001, SC-007, SC-008, SC-009 |
| Windows 10 | PowerShell | Spanish/English | Internal Markdown links, language switches, README-to-guide links, and index destinations | 2026-11-24 | PASS | Every local file and anchor target resolved in `README.md` and `INSTALLATION_GUIDE.md` | SC-002, SC-007, SC-008, SC-009 |
| Windows 10 | PowerShell | Spanish/English | `python -m pytest -q` | 2026-11-24 | PASS | `9 passed` with Python 3.12.10 | SC-005 |
| Windows 10 | PowerShell | Spanish/English | Reinstall package, `featurehero version`, `poetry check`, and `poetry build` | 2026-11-24 | PASS | Wheel and sdist built as `2026.2.1.16`; CLI reported `2026.2.1.16`; Poetry reported `All set!` | SC-005, SC-007 |

## Required validation matrix

- Windows PowerShell
- Windows CMD
- macOS
- Ubuntu/Debian

Other Linux distributions are guidance-only unless a separate record is added.

T027 remains open until the macOS walkthrough is executed on a real macOS
environment and its result is recorded here.
