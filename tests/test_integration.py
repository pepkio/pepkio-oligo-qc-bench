"""Integration tests against live Pepkio Tools API."""

from __future__ import annotations

import os

import pytest

from pepkio_oligo_qc_bench.client import PepkioClient

# Local first, then production (param order).
ENVIRONMENTS = [
    ("local", "https://tools.localtest.me"),
    ("production", "https://tools.pepkio.com"),
]


def _api_key_for(base_url: str) -> str | None:
    if "localtest.me" in base_url:
        return os.getenv("LOCAL_PEPKIO_API_KEY")
    return os.getenv("PEPKIO_API_KEY")


@pytest.fixture(params=ENVIRONMENTS, ids=["local", "production"])
def live_client(request):
    env_name, base_url = request.param
    api_key = _api_key_for(base_url)
    if not api_key:
        pytest.skip(f"No API key for {env_name} (set LOCAL_PEPKIO_API_KEY or PEPKIO_API_KEY)")
    try:
        with PepkioClient(api_key=api_key, base_url=base_url) as client:
            client.get_manifest()
            yield client
    except Exception as exc:
        pytest.skip(f"Environment {env_name} ({base_url}) unreachable: {exc}")


def test_get_manifest(live_client: PepkioClient):
    manifest = live_client.get_manifest(refresh=True)
    assert manifest["tool_id"] == "oligo-qc-bench"
    names = live_client.list_examples()
    assert "single_standard_pcr" in names


def test_run_single_standard_pcr_example(live_client: PepkioClient):
    inp = live_client.get_example_input("single_standard_pcr")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.run_id
    assert result.permalink
    assert result.result is not None
    assert result.result.get("mode") == "single"
    assert "single" in result.result
    assert result.result["single"].get("risk_level") == "low"


def test_run_batch_two_oligos_example(live_client: PepkioClient):
    inp = live_client.get_example_input("batch_two_oligos")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("mode") == "batch"
    assert "batch" in result.result
    assert isinstance(result.result["batch"], list)
