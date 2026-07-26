import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from opportunity_radar.artifacts import initialize_run


class InitializeRunTests(unittest.TestCase):
    def test_creates_complete_default_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "research"
            created_at = datetime(2026, 7, 17, 8, 30, tzinfo=timezone.utc)

            initialize_run(output, created_at=created_at)

            self.assertEqual(
                sorted(path.name for path in output.iterdir()),
                ["brief.json", "candidates.json", "evidence.jsonl", "report.md"],
            )
            brief = json.loads((output / "brief.json").read_text(encoding="utf-8"))
            self.assertEqual(brief["market"], "global-en")
            self.assertEqual(brief["mvp_window_weeks"], [4, 6])
            self.assertEqual(brief["budget_class"], "low")
            self.assertEqual(brief["created_at"], "2026-07-17T08:30:00+00:00")
            self.assertEqual(
                json.loads((output / "candidates.json").read_text(encoding="utf-8")),
                {"schema_version": 1, "candidates": []},
            )
            self.assertEqual((output / "evidence.jsonl").read_text(encoding="utf-8"), "")
            root = Path(__file__).resolve().parents[2]
            template = (
                root
                / "skills"
                / "find-product-opportunities"
                / "assets"
                / "report-template.md"
            ).read_text(encoding="utf-8")
            self.assertEqual((output / "report.md").read_text(encoding="utf-8"), template)

    def test_rejects_non_empty_output_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "research"
            output.mkdir()
            (output / "keep.txt").write_text("user data", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "not empty"):
                initialize_run(output)

            self.assertEqual((output / "keep.txt").read_text(encoding="utf-8"), "user data")


if __name__ == "__main__":
    unittest.main()
