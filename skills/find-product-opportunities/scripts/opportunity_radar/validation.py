"""Structural validation for evidence-backed Opportunity Radar runs."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .scoring import score_candidates


EVIDENCE_FIELDS = {
    "id",
    "source_url",
    "source_title",
    "collected_at",
    "source_type",
    "signal_family",
    "direction",
    "claim",
    "excerpt",
    "reliability",
    "limitations",
}
CANDIDATE_FIELDS = {
    "id",
    "name",
    "target_user",
    "problem",
    "scores",
    "evidence_ids",
    "confidence",
    "status",
}
CITATION_PATTERN = re.compile(r"\[(E\d{3,})\]")
REPORT_PLACEHOLDER_PATTERN = re.compile(
    r"待评分脚本写回|待补充|\b(?:TBD|TODO)\b|RECOMMENDATION\s*/\s*NO-GO",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str


def _issue(issues: list[ValidationIssue], code: str, message: str) -> None:
    issues.append(ValidationIssue(code, message))


def _load_evidence(path: Path, issues: list[ValidationIssue]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        _issue(issues, "missing-file", "evidence.jsonl is missing")
        return rows

    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            _issue(issues, "invalid-evidence-json", f"line {line_number}: {error.msg}")
            continue
        if not isinstance(row, dict):
            _issue(issues, "invalid-evidence-record", f"line {line_number} is not an object")
            continue
        missing = sorted(EVIDENCE_FIELDS - set(row))
        if missing:
            _issue(
                issues,
                "missing-evidence-field",
                f"line {line_number} is missing: {', '.join(missing)}",
            )
        if row.get("direction") not in {"support", "counter", "context"}:
            _issue(issues, "invalid-evidence-direction", f"line {line_number} has invalid direction")
        rows.append(row)
    return rows


def _load_json(path: Path, issues: list[ValidationIssue]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        _issue(issues, "missing-file", f"{path.name} is missing")
        return {}
    except json.JSONDecodeError as error:
        _issue(issues, "invalid-json", f"{path.name}: {error.msg}")
        return {}
    if not isinstance(value, dict):
        _issue(issues, "invalid-json-root", f"{path.name} must contain an object")
        return {}
    return value


def validate_run(run_path: Path) -> list[ValidationIssue]:
    """Return all structural and traceability issues in a saved research run."""

    root = Path(run_path)
    issues: list[ValidationIssue] = []
    _load_json(root / "brief.json", issues)
    rows = _load_evidence(root / "evidence.jsonl", issues)
    document = _load_json(root / "candidates.json", issues)
    try:
        report = (root / "report.md").read_text(encoding="utf-8")
    except FileNotFoundError:
        _issue(issues, "missing-file", "report.md is missing")
        report = ""

    placeholder = REPORT_PLACEHOLDER_PATTERN.search(report)
    if placeholder:
        _issue(
            issues,
            "unresolved-report-placeholder",
            f"report contains unresolved placeholder: {placeholder.group(0)}",
        )

    evidence_by_id: dict[str, dict[str, Any]] = {}
    for row in rows:
        evidence_id = row.get("id")
        if not isinstance(evidence_id, str) or not re.fullmatch(r"E\d{3,}", evidence_id):
            _issue(issues, "invalid-evidence-id", f"invalid evidence id: {evidence_id!r}")
            continue
        if evidence_id in evidence_by_id:
            _issue(issues, "duplicate-evidence-id", f"duplicate evidence id: {evidence_id}")
        else:
            evidence_by_id[evidence_id] = row

    candidates = document.get("candidates", [])
    if not isinstance(candidates, list):
        _issue(issues, "invalid-candidates", "candidates must be a list")
        candidates = []

    try:
        expected_document = score_candidates(document)
    except ValueError as error:
        _issue(issues, "invalid-candidate-score", str(error))
        expected_document = {"candidates": []}
    expected_by_id = {
        candidate.get("id"): candidate
        for candidate in expected_document.get("candidates", [])
        if isinstance(candidate, dict)
    }

    finalists: list[dict[str, Any]] = []
    recommended: list[dict[str, Any]] = []
    for candidate in candidates:
        if not isinstance(candidate, dict):
            _issue(issues, "invalid-candidate", "candidate must be an object")
            continue
        candidate_id = candidate.get("id", "<unknown>")
        expected = expected_by_id.get(candidate_id)
        if expected is not None and any(
            candidate.get(field) != expected.get(field)
            for field in ("weighted_score", "base_rank", "final_rank")
        ):
            _issue(
                issues,
                "stale-candidate-score",
                f"candidate {candidate_id} must be processed by the score command",
            )
        missing = sorted(CANDIDATE_FIELDS - set(candidate))
        if missing:
            _issue(
                issues,
                "missing-candidate-field",
                f"candidate {candidate_id} is missing: {', '.join(missing)}",
            )
        evidence_ids = candidate.get("evidence_ids", [])
        if not isinstance(evidence_ids, list):
            _issue(
                issues,
                "invalid-evidence-references",
                f"candidate {candidate_id} evidence_ids must be a list",
            )
            evidence_ids = []
        referenced_rows = []
        for evidence_id in evidence_ids:
            row = evidence_by_id.get(evidence_id)
            if row is None:
                _issue(
                    issues,
                    "broken-candidate-reference",
                    f"candidate {candidate_id} references missing {evidence_id}",
                )
            else:
                referenced_rows.append(row)

        if candidate.get("status") == "finalist":
            finalists.append(candidate)
            families = {
                row.get("signal_family")
                for row in referenced_rows
                if row.get("signal_family")
            }
            if len(families) < 3:
                _issue(
                    issues,
                    "finalist-signal-diversity",
                    f"finalist {candidate_id} has {len(families)} independent signal families",
                )
            checks = candidate.get("counterevidence_checks")
            if not isinstance(checks, list) or not checks:
                _issue(
                    issues,
                    "missing-counterevidence-check",
                    f"finalist {candidate_id} has no recorded counterevidence check",
                )
            if candidate.get("confidence") == "high" and any(
                row.get("direction") == "counter" for row in referenced_rows
            ):
                _issue(
                    issues,
                    "confidence-conflict",
                    f"finalist {candidate_id} cannot be high confidence with counter evidence",
                )
            if candidate.get("recommended") is True:
                recommended.append(candidate)

    report_ids = set(CITATION_PATTERN.findall(report))
    for evidence_id in report_ids:
        if evidence_id not in evidence_by_id:
            _issue(issues, "broken-report-reference", f"report references missing {evidence_id}")
    for candidate in finalists:
        for evidence_id in candidate.get("evidence_ids", []):
            if evidence_id in evidence_by_id and evidence_id not in report_ids:
                _issue(
                    issues,
                    "missing-report-citation",
                    f"report does not cite {evidence_id} used by finalist {candidate.get('id')}",
                )

    decision = document.get("decision")
    if decision == "recommendation":
        if len(finalists) != 3:
            _issue(
                issues,
                "finalist-count",
                f"recommendation requires 3 finalists, found {len(finalists)}",
            )
        if len(recommended) != 1:
            _issue(
                issues,
                "recommendation-count",
                f"recommendation requires 1 primary choice, found {len(recommended)}",
            )
    elif decision == "no-go":
        if recommended:
            _issue(issues, "no-go-recommendation", "no-go runs cannot contain a primary recommendation")
        if "NO-GO" not in report.upper():
            _issue(issues, "missing-no-go-marker", "no-go report must state NO-GO")
    else:
        _issue(issues, "invalid-decision", "decision must be recommendation or no-go")

    return issues
