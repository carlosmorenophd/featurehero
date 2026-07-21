"""Analyze final genetic optimization CSV files without retraining models."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Mapping, Sequence

import numpy as np
import pandas as pd


MetricDirection = Literal["auto", "maximize", "minimize"]
DuplicatePolicy = Literal["keep", "drop", "error"]

FEATURE_PREFIX = "feature_"
RESULT_PREFIX_COLUMNS = [
    "machine_name",
    "index_metric",
    "d2_absolute_error_score",
    "d2_pinball_score",
    "d2_tweedie_score",
    "explained_variance_score",
    "max_error",
    "mean_absolute_error",
    "mean_absolute_percentage_error",
    "mean_gamma_deviance",
    "mean_poisson_deviance",
    "mean_squared_error",
    "mean_squared_log_error",
    "median_absolute_error",
    "r2_score",
    "root_mean_squared_error",
    "root_mean_squared_log_error",
    "accuracy_mape",
]
DEFAULT_WEIGHTS = {
    "frequency": 0.25,
    "elite": 0.30,
    "weighted": 0.25,
    "stability": 0.20,
}

MAXIMIZE_METRICS = {
    "accuracy_mape",
    "d2_absolute_error_score",
    "d2_pinball_score",
    "d2_tweedie_score",
    "explained_variance_score",
    "r2_score",
}
MINIMIZE_METRICS = {
    "max_error",
    "mean_absolute_error",
    "mean_absolute_percentage_error",
    "mean_gamma_deviance",
    "mean_poisson_deviance",
    "mean_squared_error",
    "mean_squared_log_error",
    "median_absolute_error",
    "root_mean_squared_error",
    "root_mean_squared_log_error",
}
KNOWN_METRICS = MAXIMIZE_METRICS | MINIMIZE_METRICS


@dataclass(frozen=True)
class AnalysisConfig:
    """Configuration for analysis of one or more result files."""

    ranking_metric: str = "index_metric"
    metric_direction: MetricDirection = "auto"
    elite_fraction: float = 0.10
    weights: Mapping[str, float] = field(
        default_factory=lambda: DEFAULT_WEIGHTS.copy()
    )
    duplicate_policy: DuplicatePolicy = "keep"

    def __post_init__(self) -> None:
        if not 0 < self.elite_fraction <= 1:
            raise ValueError("elite_fraction must be greater than 0 and at most 1")
        if self.metric_direction not in {"auto", "maximize", "minimize"}:
            raise ValueError("metric_direction must be auto, maximize, or minimize")
        if self.duplicate_policy not in {"keep", "drop", "error"}:
            raise ValueError("duplicate_policy must be keep, drop, or error")
        unknown = set(self.weights) - set(DEFAULT_WEIGHTS)
        if unknown:
            raise ValueError(f"Unknown relevance weights: {sorted(unknown)}")
        if any(not np.isfinite(value) or value < 0 for value in self.weights.values()):
            raise ValueError("Relevance weights must be finite and non-negative")
        if sum(self.weights.values()) <= 0:
            raise ValueError("At least one relevance weight must be greater than zero")


@dataclass
class ResultAnalysis:
    """All derived tables and metadata produced by an analysis."""

    feature_relevance: pd.DataFrame
    feature_relevance_by_model: pd.DataFrame
    feature_cooccurrence: pd.DataFrame
    summary: dict

    def export(self, output_dir: str | Path) -> Path:
        """Write derived files to a new directory and return its path."""
        destination = Path(output_dir).expanduser().resolve()
        if destination.exists() and not destination.is_dir():
            raise ValueError(
                f"Output path must be a directory, but it is a file: {destination}"
            )
        destination.mkdir(parents=True, exist_ok=True)
        self.feature_relevance.to_csv(
            destination / "feature_relevance.csv", index=False
        )
        self.feature_relevance_by_model.to_csv(
            destination / "feature_relevance_by_model.csv", index=False
        )
        self.feature_cooccurrence.to_csv(
            destination / "feature_cooccurrence.csv", index=False
        )
        with (destination / "analysis_summary.json").open(
            "w", encoding="utf-8"
        ) as summary_file:
            json.dump(self.summary, summary_file, indent=2, ensure_ascii=False)
        return destination


class ResultAnalyzer:
    """Read final result CSV files and derive feature relevance evidence."""

    def __init__(
        self,
        input_files: Sequence[str | Path],
        config: AnalysisConfig | None = None,
    ) -> None:
        if not input_files:
            raise ValueError("At least one input CSV file is required")
        self._input_files = [Path(path).expanduser().resolve() for path in input_files]
        self._config = config or AnalysisConfig()
        self._warnings: list[str] = []
        self._direction = self._resolve_direction()

    def analyze(self) -> ResultAnalysis:
        """Validate inputs and calculate all output tables."""
        runs, feature_columns = self._load_runs()
        combined = pd.concat(runs, ignore_index=True)
        normalized_weights = self._normalized_weights(len(runs))

        relevance = self._aggregate_relevance(
            combined,
            runs,
            feature_columns,
            normalized_weights,
        )
        by_model_frames = []
        for machine_name in sorted(combined["machine_name"].astype(str).unique()):
            model_runs = []
            for run in runs:
                model_run = run[
                    run["machine_name"].astype(str) == machine_name
                ].copy().reset_index(drop=True)
                if model_run.empty:
                    continue
                model_run["__quality"] = self._quality(
                    model_run[self._config.ranking_metric]
                )
                model_run["__is_elite"] = self._elite_mask(model_run)
                model_runs.append(model_run)
            model_combined = pd.concat(model_runs, ignore_index=True)
            model_weights = self._normalized_weights(len(model_runs))
            model_result = self._aggregate_relevance(
                model_combined,
                model_runs,
                feature_columns,
                model_weights,
            )
            model_result.insert(0, "machine_name", machine_name)
            by_model_frames.append(model_result)

        by_model = pd.concat(by_model_frames, ignore_index=True)
        cooccurrence = self._cooccurrence(combined, feature_columns)
        metrics_found = [column for column in combined.columns if column in KNOWN_METRICS]
        summary = {
            "input_files": [str(path) for path in self._input_files],
            "individual_count": int(len(combined)),
            "run_count": len(runs),
            "models": sorted(combined["machine_name"].astype(str).unique().tolist()),
            "metrics_found": sorted(metrics_found),
            "feature_count": len(feature_columns),
            "ranking_metric": self._config.ranking_metric,
            "metric_direction": self._direction,
            "elite_fraction": self._config.elite_fraction,
            "effective_weights": normalized_weights,
            "duplicate_policy": self._config.duplicate_policy,
            "components_not_available": [
                "model_native_importance",
                "permutation_importance",
                "shap",
            ],
            "warnings": self._warnings,
        }
        if len(combined) == 1:
            summary["warnings"].append(
                "Only one individual was analyzed; selection rates are not "
                "evidence of stable relevance."
            )
        if len(runs) == 1:
            summary["warnings"].append(
                "Only one result file was analyzed; cross-run stability is unavailable."
            )
        return ResultAnalysis(relevance, by_model, cooccurrence, summary)

    def _resolve_direction(self) -> Literal["maximize", "minimize"]:
        direction = self._config.metric_direction
        if direction != "auto":
            return direction
        metric = self._config.ranking_metric.lower()
        if metric in MAXIMIZE_METRICS:
            return "maximize"
        if metric in MINIMIZE_METRICS:
            return "minimize"
        if metric == "index_metric":
            raise ValueError(
                "The direction of index_metric is ambiguous. Set metric_direction "
                "to 'maximize' or 'minimize', or choose a known ranking metric."
            )
        raise ValueError(
            f"Cannot infer direction for ranking metric '{self._config.ranking_metric}'"
        )

    def _load_runs(self) -> tuple[list[pd.DataFrame], list[str]]:
        runs: list[pd.DataFrame] = []
        expected_features: set[str] | None = None
        ordered_features: list[str] = []
        for run_index, path in enumerate(self._input_files, start=1):
            if not path.is_file():
                raise FileNotFoundError(f"Result file not found: {path}")
            if path.suffix.lower() != ".csv":
                raise ValueError(f"Result file must be CSV: {path}")
            frame = pd.read_csv(path)
            if frame.empty:
                raise ValueError(f"Result file has no individuals: {path}")
            actual_prefix = list(frame.columns[:len(RESULT_PREFIX_COLUMNS)])
            if actual_prefix != RESULT_PREFIX_COLUMNS:
                raise ValueError(
                    "Invalid FeatureHero result format in "
                    f"{path}. The first {len(RESULT_PREFIX_COLUMNS)} columns must be, "
                    f"in this exact order: {RESULT_PREFIX_COLUMNS}. Found: "
                    f"{actual_prefix}"
                )
            if self._config.ranking_metric not in frame.columns:
                raise ValueError(
                    f"Ranking metric '{self._config.ranking_metric}' is missing in {path}"
                )
            frame[self._config.ranking_metric] = pd.to_numeric(
                frame[self._config.ranking_metric], errors="coerce"
            )
            if frame[self._config.ranking_metric].isna().any():
                raise ValueError(
                    f"Ranking metric '{self._config.ranking_metric}' contains "
                    f"missing or non-numeric values in {path}"
                )
            if not np.isfinite(frame[self._config.ranking_metric]).all():
                raise ValueError(
                    f"Ranking metric '{self._config.ranking_metric}' contains "
                    f"non-finite values in {path}"
                )
            feature_columns = [
                column for column in frame.columns if column.startswith(FEATURE_PREFIX)
            ]
            if len(feature_columns) < 2:
                raise ValueError(
                    f"At least two feature_ columns are required in {path}; "
                    f"found {len(feature_columns)}"
                )
            current_features = set(feature_columns)
            if expected_features is None:
                expected_features = current_features
                ordered_features = feature_columns
            elif current_features != expected_features:
                missing_features = sorted(expected_features - current_features)
                extra_features = sorted(current_features - expected_features)
                raise ValueError(
                    f"Incompatible feature columns in {path}; missing={missing_features}, "
                    f"extra={extra_features}"
                )
            parsed_features = pd.DataFrame(
                {
                    column: self._parse_boolean_feature(
                        frame[column], column, path
                    )
                    for column in feature_columns
                },
                index=frame.index,
            )
            frame = pd.concat(
                [frame.drop(columns=feature_columns), parsed_features],
                axis=1,
            ).copy()

            duplicate_count = int(frame.duplicated().sum())
            if duplicate_count:
                if self._config.duplicate_policy == "error":
                    raise ValueError(f"Found {duplicate_count} duplicate rows in {path}")
                self._warnings.append(
                    f"{path}: found {duplicate_count} duplicate rows "
                    f"(policy={self._config.duplicate_policy})."
                )
                if self._config.duplicate_policy == "drop":
                    frame = frame.drop_duplicates().reset_index(drop=True)
            frame = frame.assign(
                __run_id=run_index,
                __quality=self._quality(frame[self._config.ranking_metric]),
            )
            frame["__is_elite"] = self._elite_mask(frame)
            runs.append(frame)
        return runs, ordered_features

    @staticmethod
    def _parse_boolean_feature(
        series: pd.Series, column: str, path: Path
    ) -> pd.Series:
        if series.isna().any():
            raise ValueError(f"Feature column '{column}' contains missing values in {path}")
        accepted = {
            True: True,
            False: False,
            1: True,
            0: False,
            1.0: True,
            0.0: False,
            "true": True,
            "false": False,
            "1": True,
            "0": False,
        }

        def convert(value: object) -> bool:
            key = value.strip().lower() if isinstance(value, str) else value
            if key not in accepted:
                raise ValueError(
                    f"Feature column '{column}' contains invalid boolean value "
                    f"{value!r} in {path}"
                )
            return accepted[key]

        return series.map(convert).astype(bool)

    def _quality(self, metric: pd.Series) -> pd.Series:
        minimum = float(metric.min())
        maximum = float(metric.max())
        if math.isclose(minimum, maximum):
            return pd.Series(np.ones(len(metric)), index=metric.index, dtype=float)
        quality = (metric - minimum) / (maximum - minimum)
        if self._direction == "minimize":
            quality = 1.0 - quality
        # Keep the worst row in the denominator without allowing all-zero weights.
        return quality.astype(float) + np.finfo(float).eps

    def _elite_mask(self, frame: pd.DataFrame) -> pd.Series:
        elite_size = max(1, math.ceil(len(frame) * self._config.elite_fraction))
        ascending = self._direction == "minimize"
        elite_indices = frame[self._config.ranking_metric].sort_values(
            ascending=ascending, kind="stable"
        ).head(elite_size).index
        return pd.Series(frame.index.isin(elite_indices), index=frame.index)

    def _normalized_weights(self, run_count: int) -> dict[str, float]:
        available = dict(self._config.weights)
        if run_count < 2:
            available.pop("stability", None)
        total = sum(available.values())
        if total <= 0:
            raise ValueError("Available relevance weights sum to zero")
        return {name: value / total for name, value in available.items()}

    def _aggregate_relevance(
        self,
        combined: pd.DataFrame,
        runs: Sequence[pd.DataFrame],
        feature_columns: Sequence[str],
        weights: Mapping[str, float],
    ) -> pd.DataFrame:
        rows = []
        elite = combined[combined["__is_elite"]]
        quality_total = float(combined["__quality"].sum())
        for column in feature_columns:
            selected = combined[column]
            selection_rate = float(selected.mean())
            elite_rate = float(elite[column].mean())
            weighted_rate = float(
                combined.loc[selected, "__quality"].sum() / quality_total
            )
            stability = None
            if len(runs) >= 2:
                stable_runs = sum(
                    bool(run.loc[run["__is_elite"], column].any()) for run in runs
                )
                stability = stable_runs / len(runs)
            components = {
                "frequency": selection_rate,
                "elite": elite_rate,
                "weighted": weighted_rate,
                "stability": stability,
            }
            relevance_score = sum(
                weights[name] * float(components[name]) for name in weights
            )
            rows.append(
                {
                    "feature": column.removeprefix(FEATURE_PREFIX),
                    "selected_count": int(selected.sum()),
                    "individual_count": int(len(combined)),
                    "selection_rate": selection_rate,
                    "elite_selected_count": int(elite[column].sum()),
                    "elite_individual_count": int(len(elite)),
                    "elite_selection_rate": elite_rate,
                    "weighted_selection_rate": weighted_rate,
                    "stability": stability,
                    "run_count": len(runs),
                    "relevance_score": relevance_score,
                }
            )
        result = pd.DataFrame(rows).sort_values(
            ["relevance_score", "feature"], ascending=[False, True], kind="stable"
        )
        result.insert(len(result.columns), "rank", range(1, len(result) + 1))
        return result.reset_index(drop=True)

    @staticmethod
    def _cooccurrence(
        combined: pd.DataFrame, feature_columns: Sequence[str]
    ) -> pd.DataFrame:
        rows = []
        individual_count = len(combined)
        for left_index, left in enumerate(feature_columns):
            for right in feature_columns[left_index + 1:]:
                left_selected = combined[left]
                right_selected = combined[right]
                joint_count = int((left_selected & right_selected).sum())
                union_count = int((left_selected | right_selected).sum())
                rows.append(
                    {
                        "feature_a": left.removeprefix(FEATURE_PREFIX),
                        "feature_b": right.removeprefix(FEATURE_PREFIX),
                        "joint_count": joint_count,
                        "joint_rate": joint_count / individual_count,
                        "jaccard_score": (
                            joint_count / union_count if union_count else 0.0
                        ),
                    }
                )
        return pd.DataFrame(
            rows,
            columns=[
                "feature_a",
                "feature_b",
                "joint_count",
                "joint_rate",
                "jaccard_score",
            ],
        ).sort_values(
            ["jaccard_score", "joint_count", "feature_a", "feature_b"],
            ascending=[False, False, True, True],
            kind="stable",
        ).reset_index(drop=True)
