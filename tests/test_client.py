"""Unit tests for PepkioClient with mocked HTTP."""

from __future__ import annotations

import httpx
import pytest

from pepkio_oligo_qc_bench.client import PepkioClient
from pepkio_oligo_qc_bench.config import resolve_api_key, resolve_base_url
from pepkio_oligo_qc_bench.exceptions import PepkioAPIError


def test_resolve_base_url_default():
    assert resolve_base_url() == "https://tools.pepkio.com"
    assert resolve_base_url("https://tools.localtest.me/") == "https://tools.localtest.me"


def test_resolve_api_key(monkeypatch):
    monkeypatch.setenv("PEPKIO_API_KEY", "prod_key_123")
    monkeypatch.setenv("LOCAL_PEPKIO_API_KEY", "local_key_123")

    assert resolve_api_key(base_url="https://tools.pepkio.com") == "prod_key_123"
    assert resolve_api_key(base_url="https://tools.localtest.me") == "local_key_123"
    assert resolve_api_key("override_key") == "override_key"


def test_client_missing_api_key(monkeypatch):
    monkeypatch.delenv("PEPKIO_API_KEY", raising=False)
    monkeypatch.delenv("LOCAL_PEPKIO_API_KEY", raising=False)
    client = PepkioClient(api_key=None, base_url="https://tools.pepkio.com")
    with pytest.raises(ValueError, match="API key required"):
        client.run({"mode": "single", "sequence": "ATGC", "preset_id": "standard_pcr"})


def test_get_manifest_success(mock_manifest):
    def handle_request(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/tools/oligo-qc-bench/manifest"
        return httpx.Response(200, json=mock_manifest)

    transport = httpx.MockTransport(handle_request)
    with PepkioClient(api_key="test_key", base_url="https://tools.pepkio.com") as client:
        client._http = httpx.Client(base_url=client.base_url, transport=transport)
        manifest = client.get_manifest()
        assert manifest["tool_id"] == "oligo-qc-bench"
        assert len(client.list_examples()) == 2
        assert "single_standard_pcr" in client.list_examples()

        ex_input = client.get_example_input("single_standard_pcr")
        assert ex_input["mode"] == "single"
        assert ex_input["sequence"] == "GAAGGTGAAGGTCGGAGTC"


def test_run_success(mock_run_response):
    def handle_request(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/tools/oligo-qc-bench/run"
        assert request.headers.get("Authorization") == "Bearer test_key"
        return httpx.Response(200, json=mock_run_response)

    transport = httpx.MockTransport(handle_request)
    with PepkioClient(api_key="test_key", base_url="https://tools.pepkio.com") as client:
        client._http = httpx.Client(
            base_url=client.base_url,
            headers={"Authorization": "Bearer test_key"},
            transport=transport,
        )
        result = client.run(
            {"mode": "single", "sequence": "GAAGGTGAAGGTCGGAGTC", "preset_id": "standard_pcr"},
            label="test-run",
        )
        assert result.status == "completed"
        assert result.run_id == "run_test123"
        assert result.result["mode"] == "single"


def test_get_run_success(mock_run_response):
    def handle_request(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/runs/run_test123"
        return httpx.Response(200, json=mock_run_response)

    transport = httpx.MockTransport(handle_request)
    with PepkioClient(api_key="test_key", base_url="https://tools.pepkio.com") as client:
        client._http = httpx.Client(
            base_url=client.base_url,
            headers={"Authorization": "Bearer test_key"},
            transport=transport,
        )
        result = client.get_run("run_test123")
        assert result.status == "completed"
        assert result.run_id == "run_test123"


def test_api_error_response():
    def handle_request(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            400,
            json={"error": {"message": "Invalid sequence", "code": "INVALID_INPUT"}},
        )

    transport = httpx.MockTransport(handle_request)
    with PepkioClient(api_key="test_key", base_url="https://tools.pepkio.com") as client:
        client._http = httpx.Client(
            base_url=client.base_url,
            headers={"Authorization": "Bearer test_key"},
            transport=transport,
        )
        with pytest.raises(PepkioAPIError) as exc_info:
            client.run({"mode": "single", "sequence": "INVALID", "preset_id": "standard_pcr"})
        assert exc_info.value.status_code == 400
        assert "Invalid sequence" in str(exc_info.value)
