import json

import httpx
import pytest

from pepkio_realistic_random_seq_generator import (
    DEFAULT_API_BASE_URL,
    PepkioAPIError,
    PepkioAuthError,
    PepkioClient,
    PepkioHTTPError,
    RunResult,
    SequenceInput,
)


def test_client_init_defaults(monkeypatch):
    monkeypatch.delenv("PEPKIO_API_KEY", raising=False)
    monkeypatch.delenv("PEPKIO_API_BASE_URL", raising=False)
    client = PepkioClient()
    assert client.base_url == DEFAULT_API_BASE_URL
    assert client.api_key is None


def test_client_init_override():
    client = PepkioClient(api_key="test_key", base_url="https://custom.pepkio.com/")
    assert client.base_url == "https://custom.pepkio.com"
    assert client.api_key == "test_key"


def test_get_manifest_success():
    mock_manifest = {
        "tool_id": "realistic-random-seq-generator",
        "title": "Realistic Random Sequence Generator",
        "examples": [{"name": "dna_demo", "input": {"sequence_type": "dna"}}],
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/tools/realistic-random-seq-generator/manifest"
        assert request.method == "GET"
        return httpx.Response(200, json=mock_manifest)

    transport = httpx.MockTransport(handler)
    httpx_client = httpx.Client(transport=transport)
    client = PepkioClient(httpx_client=httpx_client)

    manifest = client.get_manifest()
    assert manifest["tool_id"] == "realistic-random-seq-generator"
    assert manifest["title"] == "Realistic Random Sequence Generator"


def test_run_missing_api_key(monkeypatch):
    monkeypatch.delenv("PEPKIO_API_KEY", raising=False)
    client = PepkioClient(base_url="https://tools.pepkio.com")
    with pytest.raises(PepkioAuthError, match="PEPKIO_API_KEY is required"):
        client.run({"sequence_type": "dna", "length": 100, "count": 1})


def test_run_success():
    mock_response = {
        "run_id": "run-12345",
        "status": "completed",
        "result": {
            "sequence_type": "dna",
            "count": 1,
            "length": 100,
            "sequences": [{"id": 1, "sequence": "ATCG"}],
            "fasta": ">seq_1\nATCG\n",
        },
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run-12345",
        "permalink": "https://tools.pepkio.com/r/run-12345",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/tools/realistic-random-seq-generator/run"
        assert request.headers["Authorization"] == "Bearer test_key"
        body = json.loads(request.content)
        assert body["input"]["sequence_type"] == "dna"
        assert body["input"]["length"] == 100
        return httpx.Response(200, json=mock_response)

    transport = httpx.MockTransport(handler)
    httpx_client = httpx.Client(transport=transport)
    client = PepkioClient(api_key="test_key", httpx_client=httpx_client)

    input_data = SequenceInput(sequence_type="dna", length=100, count=1)
    res = client.run(input_data)

    assert isinstance(res, RunResult)
    assert res.run_id == "run-12345"
    assert res.status == "completed"
    parsed = res.get_parsed_result()
    assert parsed.count == 1
    assert parsed.fasta == ">seq_1\nATCG\n"


def test_run_http_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="Internal Server Error")

    transport = httpx.MockTransport(handler)
    httpx_client = httpx.Client(transport=transport)
    client = PepkioClient(api_key="test_key", httpx_client=httpx_client)

    with pytest.raises(PepkioHTTPError) as exc_info:
        client.run({"sequence_type": "dna", "length": 100, "count": 1})
    assert exc_info.value.status_code == 500


def test_run_body_error():
    mock_response = {
        "run_id": "run-err",
        "status": "failed",
        "result": None,
        "error": "Invalid motif sequence",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=mock_response)

    transport = httpx.MockTransport(handler)
    httpx_client = httpx.Client(transport=transport)
    client = PepkioClient(api_key="test_key", httpx_client=httpx_client)

    with pytest.raises(PepkioAPIError, match="Invalid motif sequence"):
        client.run({"sequence_type": "dna", "length": 100, "count": 1, "motif": "INVALID"})


def test_get_run_success():
    mock_response = {
        "run_id": "run-999",
        "status": "completed",
        "result": {"count": 2},
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/runs/run-999"
        return httpx.Response(200, json=mock_response)

    transport = httpx.MockTransport(handler)
    httpx_client = httpx.Client(transport=transport)
    client = PepkioClient(api_key="test_key", httpx_client=httpx_client)

    res = client.get_run("run-999")
    assert res.run_id == "run-999"
    assert res.status == "completed"
