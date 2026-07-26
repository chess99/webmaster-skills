import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from opportunity_radar.cli import main
from opportunity_radar.scoring import SCORE_WEIGHTS


class CliTests(unittest.TestCase):
    def test_directory_entrypoint_runs_as_documented(self) -> None:
        root = Path(__file__).resolve().parents[2]
        entrypoint = (
            root
            / "skills"
            / "find-product-opportunities"
            / "scripts"
            / "opportunity_radar"
        )

        result = subprocess.run(
            [sys.executable, str(entrypoint), "--help"],
            capture_output=True,
            check=False,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("init", result.stdout)
        self.assertIn("score", result.stdout)
        self.assertIn("validate", result.stdout)

    def test_init_subcommand_creates_a_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "run"

            exit_code = main(["init", "--output", str(output)])

            self.assertEqual(exit_code, 0)
            self.assertTrue((output / "brief.json").is_file())

    def test_score_subcommand_updates_candidates_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            document = {
                "schema_version": 1,
                "decision": "recommendation",
                "candidates": [
                    {
                        "id": "candidate",
                        "name": "Candidate",
                        "scores": {dimension: 4 for dimension in SCORE_WEIGHTS},
                    }
                ],
            }
            (root / "candidates.json").write_text(json.dumps(document), encoding="utf-8")

            exit_code = main(["score", "--run", str(root)])

            updated = json.loads((root / "candidates.json").read_text(encoding="utf-8"))
            self.assertEqual(exit_code, 0)
            self.assertEqual(updated["candidates"][0]["weighted_score"], 80.0)

    def test_validate_subcommand_returns_machine_readable_issues(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output = io.StringIO()

            with redirect_stdout(output):
                exit_code = main(["validate", "--run", str(root), "--format", "json"])

            payload = json.loads(output.getvalue())
            self.assertEqual(exit_code, 1)
            self.assertTrue(any(issue["code"] == "missing-file" for issue in payload["issues"]))


if __name__ == "__main__":
    unittest.main()
