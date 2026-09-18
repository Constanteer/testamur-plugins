from __future__ import annotations

import json
from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[1]


def test_submission_assets_are_complete() -> None:
    assert (PLUGIN / "README.md").is_file()
    assert (PLUGIN / "SUBMISSION.md").is_file()
    provider_manifest = PLUGIN / "testamur-monitor-providers.json"
    assert provider_manifest.is_file()
    providers = json.loads(provider_manifest.read_text(encoding="utf-8"))
    assert providers["schema"] == "testamur.monitor-providers.v1"
    assert any(item["name"] == "github_branch" for item in providers["providers"])
    payload = json.loads((PLUGIN / "submission-tests.json").read_text(encoding="utf-8"))
    assert payload["schema"] == "testamur.openai-plugin-submission-cases.v1"
    assert len(payload["starter_prompts"]) >= 4
    assert len(payload["positive"]) >= 5
    assert len(payload["negative"]) >= 3


def test_submission_cases_preserve_testamur_firewall() -> None:
    payload = json.loads((PLUGIN / "submission-tests.json").read_text(encoding="utf-8"))
    text = json.dumps(payload, sort_keys=True).lower()
    assert "hidden chain-of-thought" in text
    assert "fetched/exposed != relied" in text
    assert "changed with invalid" in text or "change" in text
