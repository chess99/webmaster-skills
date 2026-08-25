import csv
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "link-ops" / "scripts" / "link_ops.py"
SPEC = importlib.util.spec_from_file_location("link_ops_script", SCRIPT)
assert SPEC and SPEC.loader
link_ops = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(link_ops)


class LinkOpsTests(unittest.TestCase):
    def test_cli_help_lists_core_commands(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--help"],
            capture_output=True,
            check=False,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("init", result.stdout)
        self.assertIn("import", result.stdout)
        self.assertIn("score", result.stdout)
        self.assertIn("validate", result.stdout)

    def test_init_creates_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run = Path(temp_dir) / "run"
            link_ops.init_workspace(run, site="https://example.com", name="Example")

            self.assertTrue((run / "brief.json").is_file())
            self.assertTrue((run / "prospects.csv").is_file())
            self.assertTrue((run / "channels.csv").is_file())
            self.assertTrue((run / "outreach.csv").is_file())
            self.assertEqual(link_ops.validate_workspace(run), [])

    def test_import_normalizes_common_export_headers_and_deduplicates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run = root / "run"
            link_ops.init_workspace(run)
            export = root / "ahrefs.csv"
            export.write_text(
                "Referring page URL,Target URL,Anchor,Domain Rating\n"
                "https://blog.example/post,https://competitor.test/tool,Example Tool,61\n"
                "https://blog.example/post,https://competitor.test/tool,Example Tool,61\n",
                encoding="utf-8",
            )

            added, skipped = link_ops.import_csv(
                run,
                export,
                import_source="ahrefs",
                competitor="competitor.test",
            )

            self.assertEqual((added, skipped), (1, 1))
            rows = link_ops.read_csv(run / "prospects.csv")
            self.assertEqual(rows[0]["source_domain"], "blog.example")
            self.assertEqual(rows[0]["anchor_text"], "Example Tool")
            self.assertEqual(rows[0]["authority_metric"], "61")
            self.assertEqual(rows[0]["import_source"], "ahrefs")
            self.assertEqual(rows[0]["competitor"], "competitor.test")

    def test_score_applies_weighted_score_and_risk_penalty(self) -> None:
        row = link_ops.blank_row(link_ops.PROSPECT_FIELDS)
        row["source_url"] = "https://example.com/resource"
        for field in link_ops.SCORE_WEIGHTS:
            row[field] = "4"
        row["spam_risk"] = "3"

        scored = link_ops.score_row(row)

        self.assertEqual(scored["opportunity_score"], "55.0")
        self.assertEqual(scored["score_status"], "complete")
        self.assertEqual(scored["recommended_action"], "consider")

    def test_high_spam_risk_is_rejected_even_with_strong_base_score(self) -> None:
        row = link_ops.blank_row(link_ops.PROSPECT_FIELDS)
        row["source_url"] = "https://example.com/resource"
        for field in link_ops.SCORE_WEIGHTS:
            row[field] = "5"
        row["spam_risk"] = "4"

        scored = link_ops.score_row(row)

        self.assertEqual(scored["opportunity_score"], "50.0")
        self.assertEqual(scored["recommended_action"], "reject")

    def test_validate_reports_bad_urls_scores_and_duplicates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run = Path(temp_dir) / "run"
            link_ops.init_workspace(run)
            rows = []
            for _ in range(2):
                row = link_ops.blank_row(link_ops.PROSPECT_FIELDS)
                row["source_url"] = "not-a-url"
                row["target_url"] = "https://target.example/page"
                row["competitor"] = "target.example"
                row["topic_relevance"] = "9"
                rows.append(row)
            link_ops.write_csv(run / "prospects.csv", link_ops.PROSPECT_FIELDS, rows)

            issues = link_ops.validate_workspace(run)
            codes = [issue["code"] for issue in issues]

            self.assertIn("invalid-url", codes)
            self.assertIn("invalid-score", codes)
            self.assertIn("duplicate-prospect", codes)


if __name__ == "__main__":
    unittest.main()
