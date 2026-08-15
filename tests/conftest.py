"""Pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load monorepo .env for local integration runs (never log keys).
_monorepo_env = Path(__file__).resolve().parents[3] / ".env"
if _monorepo_env.is_file():
    load_dotenv(_monorepo_env)

_package_env = Path(__file__).resolve().parents[1] / ".env"
if _package_env.is_file():
    load_dotenv(_package_env)


@pytest.fixture
def mock_manifest() -> dict:
    return {
        "tool_id": "oligo-qc-bench",
        "title": "Oligo QC Bench",
        "execution_mode": "sync",
        "examples": [
            {
                "name": "single_standard_pcr",
                "input": {
                    "mode": "single",
                    "sequence": "GAAGGTGAAGGTCGGAGTC",
                    "partner_sequence": "GAAGATGGTGATGGGATTTC",
                    "preset_id": "standard_pcr",
                },
                "output": {"single": {"risk_level": "low"}},
            },
            {
                "name": "batch_two_oligos",
                "input": {
                    "mode": "batch",
                    "preset_id": "high_fidelity",
                    "batch_text": "ATGCGTACGTACGTACGTACG\nGAAGGTGAAGGTCGGAGTCAAC\n",
                },
                "output": {"batch": [{"risk_level": "low"}]},
            },
        ],
    }


@pytest.fixture
def mock_run_response() -> dict:
    return {
        "run_id": "run_test123",
        "status": "completed",
        "result": {
            "mode": "single",
            "preset_id": "standard_pcr",
            "single": {
                "sequence": "GAAGGTGAAGGTCGGAGTC",
                "risk_level": "low",
            },
        },
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_test123",
        "permalink": "https://tools.pepkio.com/r/run_test123",
    }
