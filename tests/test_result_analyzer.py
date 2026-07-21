"""Tests for post-processing final optimization results."""

import json
import tempfile
import unittest
import warnings
from pathlib import Path

import pandas as pd

from featurehero.services.results.result_analyzer import (
    AnalysisConfig,
    RESULT_PREFIX_COLUMNS,
    ResultAnalyzer,
)


class ResultAnalyzerTest(unittest.TestCase):
    """Validate calculations without invoking the genetic algorithm."""

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def _write_run(self, name: str, rows: list[dict]) -> Path:
        path = self.directory / name
        normalized_rows = []
        for row in rows:
            normalized = {
                column: row.get(column, 0)
                for column in RESULT_PREFIX_COLUMNS
            }
            normalized.update({
                column: value for column, value in row.items()
                if column not in RESULT_PREFIX_COLUMNS
            })
            normalized_rows.append(normalized)
        pd.DataFrame(normalized_rows).to_csv(path, index=False)
        return path

    def test_frequency_elite_weight_stability_and_cooccurrence(self) -> None:
        run_one = self._write_run(
            "run_one.csv",
            [
                {"machine_name": "rf", "r2_score": 0.9,
                 "feature_A": True, "feature_B": "true"},
                {"machine_name": "rf", "r2_score": 0.8,
                 "feature_A": 1, "feature_B": 0},
                {"machine_name": "rf", "r2_score": 0.2,
                 "feature_A": False, "feature_B": "1"},
                {"machine_name": "rf", "r2_score": 0.1,
                 "feature_A": 0, "feature_B": False},
            ],
        )
        run_two = self._write_run(
            "run_two.csv",
            [
                {"machine_name": "rf", "r2_score": 0.7,
                 "feature_A": False, "feature_B": True},
                {"machine_name": "rf", "r2_score": 0.3,
                 "feature_A": True, "feature_B": False},
            ],
        )
        result = ResultAnalyzer(
            [run_one, run_two],
            AnalysisConfig(ranking_metric="r2_score", elite_fraction=0.4),
        ).analyze()

        relevance = result.feature_relevance.set_index("feature")
        self.assertEqual(relevance.loc["A", "selected_count"], 3)
        self.assertEqual(relevance.loc["B", "selected_count"], 3)
        self.assertAlmostEqual(relevance.loc["A", "selection_rate"], 0.5)
        self.assertAlmostEqual(relevance.loc["B", "selection_rate"], 0.5)
        self.assertAlmostEqual(relevance.loc["A", "stability"], 0.5)
        self.assertAlmostEqual(relevance.loc["B", "stability"], 1.0)
        self.assertGreater(
            relevance.loc["B", "relevance_score"],
            relevance.loc["A", "relevance_score"],
        )

        pair = result.feature_cooccurrence.iloc[0]
        self.assertEqual(pair["joint_count"], 1)
        self.assertAlmostEqual(pair["joint_rate"], 1 / 6)
        self.assertAlmostEqual(pair["jaccard_score"], 0.2)

    def test_minimize_metric_selects_lowest_value_as_elite(self) -> None:
        run = self._write_run(
            "errors.csv",
            [
                {"machine_name": "xgb", "mean_absolute_error": 10,
                 "feature_A": True, "feature_B": False},
                {"machine_name": "xgb", "mean_absolute_error": 1,
                 "feature_A": False, "feature_B": True},
            ],
        )
        result = ResultAnalyzer(
            [run],
            AnalysisConfig(
                ranking_metric="mean_absolute_error",
                elite_fraction=0.5,
            ),
        ).analyze()
        row = result.feature_relevance.set_index("feature").loc["A"]
        self.assertEqual(row["elite_selected_count"], 0)
        self.assertLess(row["weighted_selection_rate"], 0.01)
        self.assertTrue(pd.isna(row["stability"]))

    def test_ambiguous_index_metric_requires_direction(self) -> None:
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            ResultAnalyzer(
                [self.directory / "unused.csv"],
                AnalysisConfig(ranking_metric="index_metric"),
            )

    def test_invalid_boolean_and_missing_values_are_rejected(self) -> None:
        invalid = self._write_run(
            "invalid.csv",
            [{"machine_name": "rf", "r2_score": 0.5,
              "feature_A": "yes", "feature_B": True}],
        )
        with self.assertRaisesRegex(ValueError, "invalid boolean"):
            ResultAnalyzer([invalid], AnalysisConfig(ranking_metric="r2_score")).analyze()

        missing = self._write_run(
            "missing.csv",
            [
                {"machine_name": "rf", "r2_score": 0.5,
                 "feature_A": True, "feature_B": False},
                {"machine_name": "rf", "r2_score": 0.4,
                 "feature_A": None, "feature_B": True},
            ],
        )
        with self.assertRaisesRegex(ValueError, "missing values"):
            ResultAnalyzer([missing], AnalysisConfig(ranking_metric="r2_score")).analyze()

    def test_incompatible_features_are_rejected(self) -> None:
        first = self._write_run(
            "first.csv",
            [{"machine_name": "rf", "r2_score": 0.5,
              "feature_A": True, "feature_shared": False}],
        )
        second = self._write_run(
            "second.csv",
            [{"machine_name": "rf", "r2_score": 0.6,
              "feature_B": True, "feature_shared": False}],
        )
        with self.assertRaisesRegex(ValueError, "Incompatible feature"):
            ResultAnalyzer(
                [first, second], AnalysisConfig(ranking_metric="r2_score")
            ).analyze()

    def test_requires_exact_result_prefix_and_two_features(self) -> None:
        invalid_order = self.directory / "invalid_order.csv"
        columns = RESULT_PREFIX_COLUMNS.copy()
        columns[0], columns[1] = columns[1], columns[0]
        row = {column: 0 for column in columns}
        row.update({"feature_A": True, "feature_B": False})
        pd.DataFrame([row], columns=columns + ["feature_A", "feature_B"]).to_csv(
            invalid_order, index=False
        )
        with self.assertRaisesRegex(ValueError, "exact order"):
            ResultAnalyzer(
                [invalid_order],
                AnalysisConfig(ranking_metric="r2_score"),
            ).analyze()

        one_feature = self._write_run(
            "one_feature.csv",
            [{"machine_name": "rf", "r2_score": 0.5, "feature_A": True}],
        )
        with self.assertRaisesRegex(ValueError, "At least two"):
            ResultAnalyzer(
                [one_feature],
                AnalysisConfig(ranking_metric="r2_score"),
            ).analyze()

    def test_output_path_must_be_a_directory(self) -> None:
        source = self._write_run(
            "valid.csv",
            [{"machine_name": "rf", "r2_score": 0.5,
              "feature_A": True, "feature_B": False}],
        )
        result = ResultAnalyzer(
            [source], AnalysisConfig(ranking_metric="r2_score")
        ).analyze()
        output_file = self.directory / "not_a_directory"
        output_file.write_text("existing file", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "must be a directory"):
            result.export(output_file)

    def test_wide_result_does_not_emit_fragmentation_warning(self) -> None:
        features = {f"feature_{index}": index % 2 == 0 for index in range(200)}
        source = self._write_run(
            "wide.csv",
            [{"machine_name": "xgb", "r2_score": 0.8, **features}],
        )
        with warnings.catch_warnings():
            warnings.simplefilter("error", pd.errors.PerformanceWarning)
            ResultAnalyzer(
                [source], AnalysisConfig(ranking_metric="r2_score")
            ).analyze()

    def test_export_creates_reports_and_preserves_source(self) -> None:
        source = self._write_run(
            "optimization.csv",
            [
                {"machine_name": "xgb", "r2_score": 0.8,
                 "feature_A": True, "feature_B": False},
                {"machine_name": "xgb", "r2_score": 0.7,
                 "feature_A": False, "feature_B": True},
            ],
        )
        original_bytes = source.read_bytes()
        output = self.directory / "analysis_results"
        result = ResultAnalyzer(
            [source],
            AnalysisConfig(ranking_metric="r2_score", elite_fraction=0.5),
        ).analyze()
        destination = result.export(output)

        self.assertEqual(Path(destination), output.resolve())
        self.assertEqual(source.read_bytes(), original_bytes)
        expected = {
            "feature_relevance.csv",
            "feature_relevance_by_model.csv",
            "feature_cooccurrence.csv",
            "analysis_summary.json",
        }
        self.assertEqual({path.name for path in output.iterdir()}, expected)
        summary = json.loads((output / "analysis_summary.json").read_text())
        self.assertEqual(summary["individual_count"], 2)
        self.assertIn("cross-run stability is unavailable", " ".join(summary["warnings"]))


if __name__ == "__main__":
    unittest.main()
