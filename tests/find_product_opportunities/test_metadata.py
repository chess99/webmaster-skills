import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "find-product-opportunities"


class MetadataTests(unittest.TestCase):
    def test_codex_manifest_declares_skill_only_plugin(self) -> None:
        manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))

        self.assertEqual(manifest["name"], "webmaster-skills")
        self.assertEqual(manifest["version"], "1.1.0")
        self.assertEqual(manifest["author"]["name"], "chess99")
        self.assertEqual(manifest["repository"], "https://github.com/chess99/webmaster-skills")
        self.assertEqual(manifest["license"], "MIT")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertFalse({"apps", "mcpServers", "hooks"} & set(manifest))

    def test_claude_manifest_matches_plugin_identity(self) -> None:
        codex = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        claude = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))

        self.assertEqual(claude["name"], codex["name"])
        self.assertEqual(claude["version"], codex["version"])
        self.assertEqual(claude["skills"], "./skills/")

    def test_skill_has_concrete_trigger_description_and_no_placeholders(self) -> None:
        content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = content.split("---", 2)[1]

        self.assertIn("name: find-product-opportunities", frontmatter)
        self.assertRegex(frontmatter, r"description: .*(产品机会|product opportunit)")
        self.assertNotRegex(content, r"\b(TODO|TBD)\b|\[TODO:")
        self.assertIn("最多三个", content)
        self.assertIn("NO-GO", content)
        self.assertIn("Google Trends", content)

    def test_skill_resources_are_complete_and_one_level_deep(self) -> None:
        expected = {
            "evidence.md",
            "report.md",
            "scoring.md",
            "source-strategy.md",
        }
        references = SKILL / "references"

        self.assertEqual({path.name for path in references.glob("*.md")}, expected)
        self.assertTrue((SKILL / "assets" / "report-template.md").is_file())
        self.assertTrue((SKILL / "scripts" / "opportunity_radar" / "__main__.py").is_file())

    def test_repository_docs_state_agent_first_boundary(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

        self.assertIn("不提供网页", readme)
        self.assertIn("Top 3", readme)
        self.assertIn("Agent 主导", agents)
        self.assertIn("不得", agents)

    def test_eval_cases_cover_positive_negative_and_failure_paths(self) -> None:
        evals = json.loads((SKILL / "evals" / "evals.json").read_text(encoding="utf-8"))
        labels = {case["label"] for case in evals["cases"]}

        self.assertTrue({"trigger", "non-trigger", "no-go", "source-failure"} <= labels)
        self.assertGreaterEqual(len(evals["cases"]), 6)

    def test_marketplace_descriptions_do_not_hardcode_skill_counts(self) -> None:
        marketplace = (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")

        self.assertNotRegex(marketplace, r"\b\d+ first-party skills?\b")


if __name__ == "__main__":
    unittest.main()
