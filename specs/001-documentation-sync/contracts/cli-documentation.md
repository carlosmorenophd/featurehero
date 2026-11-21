# CLI Documentation Contract

This contract records the public CLI surface that documentation must describe.
It does not change the application interface.

## Commands

| Command | Required inputs | Main behavior |
|---|---|---|
| `featurehero run` | `--file`, `--column` | Prepare a supported dataset and run genetic regression optimization. |
| `featurehero transform` | `--file`, `--type`, `--columns` | Transform selected columns and write a CSV result. |
| `featurehero analyze-results` | `--file`, `--output-dir` | Analyze one final optimization CSV and export derived reports. |
| `featurehero jobs` | One of `--list` or `--stop PID` | List or stop background jobs. |
| `featurehero version` | None | Print the installed package version. |

## Documented options

- `run`: `--background` and JSON `--params`; internal daemon options are not
  public usage instructions.
- `transform`: `--out` is optional; supported types are `date`, `date_seasonal`,
  `category`, `dummy`, `log1p`, and `sqrt`.
- `analyze-results`: `--metric`, `--direction`, `--elite-fraction`, `--weights`,
  and `--duplicates` control result analysis.

## Input and output constraints

- Optimization accepts `.csv`, `.xls`, `.xlsx`, and `.numbers` inputs and requires
  a numeric positive target column with numeric, non-date feature columns.
- Transformations write CSV output and preserve the input file.
- Result analysis writes relevance, model, cooccurrence, and summary artifacts to
  the required output directory without modifying the source CSV.
