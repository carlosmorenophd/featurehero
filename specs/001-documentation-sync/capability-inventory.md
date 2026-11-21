# Capability Inventory

This inventory treats executable source and tests as authoritative.

## Public CLI

| Capability | Source | Current behavior | Evidence |
|---|---|---|---|
| `run` | `featurehero/main.py`, `worker/pip_worker.py` | Validates a dataset, prepares a workspace, runs genetic regression optimization, reports progress, and exports results. | CLI parser and optimization flow |
| `transform` | `featurehero/main.py`, `core/files/transform_file.py` | Applies date, seasonal-date, category, dummy, log1p, or sqrt transformations and writes CSV. | CLI choices and transform branches |
| `analyze-results` | `featurehero/main.py`, `services/results/result_analyzer.py` | Validates a final optimization CSV and writes relevance, model, cooccurrence, and summary reports. | CLI dispatch and result analyzer tests |
| `jobs` | `featurehero/main.py`, `core/job_manager.py` | Lists active registered jobs or stops a job by PID; cleans stale entries. | JobManager implementation |
| `version` | `featurehero/main.py`, `featurehero/__init__.py` | Prints installed package metadata version. | Package metadata lookup |

## Data preparation and transformation

- `run` accepts `.csv`, `.xls`, `.xlsx`, and `.numbers` files.
- Excel and Numbers inputs must contain one sheet.
- The target column must exist, be numeric, and contain values greater than zero.
- Predictor columns must not be text or date columns.
- Transformations require existing columns and always write CSV output.
- `log1p` and `sqrt` preserve the original column, preserve missing values, and
  reject negative or non-numeric values.

## Optimization

- The genetic algorithm creates populations, selects feature chromosomes, mutates
  features and hyperparameters, crosses individuals, evaluates models, orders
  individuals by the selected metric, and exports results.
- Supported models are Lasso, Extreme Gradient Boosting, Random Forest, Support
  Vector Regression, and Bayesian Ridge Regression.
- Population size must be at least 10 and a multiple of 10; generations must be
  at least 10.
- The default optimization metric is `r2_score`.
- Metrics include D2 scores, explained variance, error metrics, R2, root errors,
  and `accuracy_mape`.
- Foreground progress is reported through a queue; background runs write log and
  status files and register the PID under `~/.featurehero/jobs.pids`.

## Result analysis

- The analyzer reads one final optimization CSV without retraining models or
  modifying the source file.
- It requires the standard result prefix and at least two `feature_` columns.
- It accepts configurable ranking metric, direction, elite fraction, weights, and
  duplicate policy.
- It calculates global and per-model selection relevance, weighted quality,
  elite selection, feature cooccurrence, and Jaccard similarity.
- SHAP, permutation importance, native model importance, and cross-run stability
  are reported unavailable when absent from the input.

## Outputs

- Optimization workspaces contain the normalized input, optimization CSVs,
  plots, serialized best model/features, and optional background logs/status.
- Result analysis creates `feature_relevance.csv`,
  `feature_relevance_by_model.csv`, `feature_cooccurrence.csv`, and
  `analysis_summary.json`.

## Tests and unavailable behavior

- `tests/test_result_analyzer.py` covers column validation, boolean conversion,
  metric direction, relevance aggregation, duplicates, output validation, and
  source preservation.
- No complete end-to-end optimization test suite is present; optimization
  behavior is documented from executable source, not claimed as fully tested.
- SHAP, permutation importance, and native model importance are unavailable in
  the current result contract.
