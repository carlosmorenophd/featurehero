# CLI Usage Contract for the Installation Guide

This contract records the public commands that the guide may use for installation
verification and first-use validation. It does not change the CLI.

## Installation contract

| Step | Command or action | Expected signal |
|---|---|---|
| Prepare | Create and activate a Python environment using platform-specific syntax | The environment is active and commands resolve inside it |
| Install | `python -m pip install .` from the repository root | Installation completes without an error |
| Verify help | `featurehero --help` | The CLI prints usage and available actions |
| Verify version | `featurehero version` | The installed package version is printed |

## Public first-use commands

| Command | Required inputs | Guide role |
|---|---|---|
| `featurehero transform` | `--file`, `--type`, `--columns`; optional `--out` | Lightweight first execution and output verification |
| `featurehero run` | `--file`, `--column`; optional `--background`, `--params` | Main optimization flow with a small valid dataset |
| `featurehero analyze-results` | `--file`, `--output-dir` | Advanced follow-up reference |
| `featurehero jobs` | `--list` or `--stop PID` | Background-job follow-up reference |
| `featurehero version` | None | Installation verification |

## Input contract

- `run` accepts `.csv`, `.xls`, `.xlsx`, and `.numbers` inputs.
- Optimization requires a numeric target column with values greater than zero and
  numeric predictor columns.
- `transform` accepts `.csv`, `.xls`, and `.xlsx` and writes CSV output.
- Paths and column names containing spaces must use shell-appropriate quoting.

## Stability rule

The guide must use commands and options exposed by the current CLI parser and must
link to `README.md` or command help for advanced parameters rather than inventing
additional public commands.

## Documentation navigation contract

| Document | Required navigation | Required link |
|---|---|---|
| `README.md` — español | Índice con requisitos, instalación, uso, problemas y referencia técnica | Enlace visible a la guía en español |
| `README.md` — English | Table of contents with requirements, installation, usage, troubleshooting and technical reference | Visible link to the guide in English |
| `INSTALLATION_GUIDE.md` — español | Índice con Windows, macOS, Ubuntu/Debian, inicio rápido y problemas | Enlace al README en español y al índice inglés |
| `INSTALLATION_GUIDE.md` — English | Table of contents with Windows, macOS, Ubuntu/Debian, quickstart and troubleshooting | Link to the English README and Spanish index |

Every index destination must resolve to an existing heading, and every language
section must expose a path to its equivalent section in the other language.
