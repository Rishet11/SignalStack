#!/usr/bin/env python3
"""Lightweight smoke test for hackathon packaging and optional backend runtime checks."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "backend"
PRELOADED_DIR = BACKEND_ROOT / "data" / "preloaded"
ENV_EXAMPLE = REPO_ROOT / ".env.example"
SYMBOLS_FILE = BACKEND_ROOT / "data" / "nse_symbols.json"


def check(condition: bool, message: str) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {message}")
    if not condition:
        raise AssertionError(message)


def validate_json_file(path: Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    required_fields = {
        "ticker",
        "company_name",
        "confidence_score",
        "primary_signal_type",
        "direction",
        "thesis",
        "detailed_reasoning",
        "action_suggestion",
        "evidence_sources",
    }
    missing = sorted(required_fields - payload.keys())
    check(not missing, f"{path.name} includes required opportunity-card fields")
    check(isinstance(payload["evidence_sources"], list) and len(payload["evidence_sources"]) >= 1, f"{path.name} contains evidence sources")


def try_import_backend() -> None:
    try:
        sys.path.insert(0, str(BACKEND_ROOT))
        import app.main  # noqa: F401
    except ModuleNotFoundError as exc:
        print(f"[WARN] Backend import skipped: missing dependency '{exc.name}'. Install backend requirements to validate imports.")
    else:
        print("[PASS] Backend imports successfully")


def try_healthcheck() -> None:
    base_url = os.getenv("SIGNALSTACK_HEALTHCHECK_URL")
    if not base_url:
        print("[INFO] Skipping live health check. Set SIGNALSTACK_HEALTHCHECK_URL to test a running backend.")
        return

    try:
        with urllib.request.urlopen(base_url, timeout=5) as response:
            body = response.read().decode("utf-8")
            check(response.status == 200, f"Live health endpoint returned HTTP {response.status}")
            check('"status"' in body, "Live health endpoint returned a status payload")
    except (urllib.error.URLError, TimeoutError) as exc:
        raise AssertionError(f"Health check failed for {base_url}: {exc}") from exc


def main() -> int:
    try:
        check(ENV_EXAMPLE.exists(), "Root .env.example exists")
        check(SYMBOLS_FILE.exists(), "Ticker symbol data file exists")
        check(PRELOADED_DIR.exists(), "Preloaded opportunity-card directory exists")

        preloaded_files = sorted(PRELOADED_DIR.glob("*.json"))
        check(len(preloaded_files) >= 2, "At least two preloaded demo cards are present")
        for path in preloaded_files:
            validate_json_file(path)

        try_import_backend()
        try_healthcheck()
    except AssertionError as exc:
        print(f"[FAIL] Smoke test failed: {exc}")
        return 1

    print("[PASS] Smoke test completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
