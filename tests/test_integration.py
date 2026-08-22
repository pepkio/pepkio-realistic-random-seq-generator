import os

import pytest
from dotenv import load_dotenv

from pepkio_realistic_random_seq_generator import (
    DEFAULT_API_BASE_URL,
    PepkioClient,
    RunResult,
)

# Load environment variables from .env if present
load_dotenv()


def get_target_config():
    """Determine base_url and api_key from environment."""
    base_url = os.getenv("PEPKIO_API_BASE_URL")
    api_key = os.getenv("PEPKIO_API_KEY")

    if not base_url:
        base_url = DEFAULT_API_BASE_URL

    if not api_key and "localtest.me" in base_url:
        api_key = os.getenv("LOCAL_PEPKIO_API_KEY")

    return base_url, api_key


def test_integration_manifest():
    base_url, _ = get_target_config()
    client = PepkioClient(base_url=base_url)
    manifest = client.get_manifest()

    assert manifest["tool_id"] == "realistic-random-seq-generator"
    assert "title" in manifest
    assert "input" in manifest
    assert "examples" in manifest
    assert len(manifest["examples"]) > 0


def test_integration_run_dna_demo():
    base_url, api_key = get_target_config()
    if not api_key:
        pytest.skip(
            f"No API key provided for {base_url}. Set PEPKIO_API_KEY or LOCAL_PEPKIO_API_KEY."
        )

    client = PepkioClient(api_key=api_key, base_url=base_url)
    manifest = client.get_manifest()
    examples = manifest.get("examples", [])
    dna_example = next((ex for ex in examples if ex.get("name") == "dna_demo"), None)
    assert dna_example is not None, "dna_demo example missing in manifest"

    input_payload = dna_example["input"]
    res = client.run(input_payload)

    assert isinstance(res, RunResult)
    assert res.status == "completed"
    assert res.run_id is not None
    assert res.result is not None

    parsed = res.get_parsed_result()
    assert parsed is not None
    assert parsed.count == 5
    assert parsed.seed == 42
    assert parsed.fasta is not None
    assert len(parsed.sequences) == 5


def test_integration_run_rna_orf():
    base_url, api_key = get_target_config()
    if not api_key:
        pytest.skip(
            f"No API key provided for {base_url}. Set PEPKIO_API_KEY or LOCAL_PEPKIO_API_KEY."
        )

    client = PepkioClient(api_key=api_key, base_url=base_url)
    manifest = client.get_manifest()
    examples = manifest.get("examples", [])
    rna_example = next((ex for ex in examples if ex.get("name") == "rna_orf"), None)
    assert rna_example is not None, "rna_orf example missing in manifest"

    input_payload = rna_example["input"]
    res = client.run(input_payload)

    assert isinstance(res, RunResult)
    assert res.status == "completed"
    assert res.result is not None

    parsed = res.get_parsed_result()
    assert parsed is not None
    assert parsed.count == 2
    assert parsed.fasta is not None


def test_integration_run_protein_uniprot():
    base_url, api_key = get_target_config()
    if not api_key:
        pytest.skip(
            f"No API key provided for {base_url}. Set PEPKIO_API_KEY or LOCAL_PEPKIO_API_KEY."
        )

    client = PepkioClient(api_key=api_key, base_url=base_url)
    manifest = client.get_manifest()
    examples = manifest.get("examples", [])
    prot_example = next((ex for ex in examples if ex.get("name") == "protein_uniprot"), None)
    assert prot_example is not None, "protein_uniprot example missing in manifest"

    input_payload = prot_example["input"]
    res = client.run(input_payload)

    assert isinstance(res, RunResult)
    assert res.status == "completed"
    assert res.result is not None

    parsed = res.get_parsed_result()
    assert parsed is not None
    assert parsed.count == 3


def test_integration_get_run():
    base_url, api_key = get_target_config()
    if not api_key:
        pytest.skip(
            f"No API key provided for {base_url}. Set PEPKIO_API_KEY or LOCAL_PEPKIO_API_KEY."
        )

    client = PepkioClient(api_key=api_key, base_url=base_url)
    run_res = client.run(
        {"sequence_type": "dna", "length": 50, "count": 1, "seed": 123}
    )
    assert run_res.run_id is not None

    fetched = client.get_run(run_res.run_id)
    assert fetched.run_id == run_res.run_id
    assert fetched.status == "completed"
