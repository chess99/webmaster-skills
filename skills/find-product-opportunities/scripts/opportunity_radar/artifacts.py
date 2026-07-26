"""Create and load Opportunity Radar research artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


REPORT_TEMPLATE = (
    Path(__file__).resolve().parents[2]
    / "assets"
    / "report-template.md"
)


def initialize_run(output: Path, *, created_at: datetime | None = None) -> None:
    """Create an empty standard research run without overwriting user data."""

    output = Path(output)
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"output directory is not empty: {output}")
    output.mkdir(parents=True, exist_ok=True)

    timestamp = created_at or datetime.now(timezone.utc)
    brief = {
        "schema_version": 1,
        "goal": "",
        "market": "global-en",
        "product_types": [
            "micro-saas",
            "ai-tool",
            "browser-extension",
            "desktop-tool",
            "mobile-tool",
        ],
        "builder_profile": "technical-independent-developer",
        "mvp_window_weeks": [4, 6],
        "budget_class": "low",
        "exclusions": [],
        "depth": "standard",
        "created_at": timestamp.isoformat(),
    }
    (output / "brief.json").write_text(
        json.dumps(brief, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "evidence.jsonl").write_text("", encoding="utf-8")
    (output / "candidates.json").write_text(
        json.dumps({"schema_version": 1, "candidates": []}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    (output / "report.md").write_text(REPORT_TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")
