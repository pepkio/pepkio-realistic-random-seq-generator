import json
import sys
from typing import Optional

import click

from .client import PepkioClient
from .config import DEFAULT_API_BASE_URL
from .exceptions import PepkioError


@click.group()
@click.version_option()
def main():
    """CLI for Pepkio realistic-random-seq-generator tool."""
    pass


@main.command()
@click.option(
    "--base-url",
    default=None,
    help=f"API base URL (default: {DEFAULT_API_BASE_URL} or PEPKIO_API_BASE_URL env var)",
)
def manifest(base_url: Optional[str]):
    """Fetch and print the tool manifest."""
    try:
        client = PepkioClient(base_url=base_url)
        data = client.get_manifest()
        click.echo(json.dumps(data, indent=2))
    except PepkioError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--example",
    help=(
        "Run using an example name from the tool manifest "
        "(e.g. dna_demo, rna_orf, protein_uniprot)"
    ),
)
@click.option(
    "--input-json",
    help="JSON string containing tool input parameters",
)
@click.option(
    "--sequence-type",
    type=click.Choice(["dna", "rna", "protein"]),
    help="Sequence type (dna, rna, protein)",
)
@click.option(
    "--length",
    type=int,
    help="Sequence length (10-50,000)",
)
@click.option(
    "--count",
    type=int,
    help="Number of sequences (1-100)",
)
@click.option(
    "--gc-percent",
    type=float,
    help="Target GC percentage (0-100)",
)
@click.option(
    "--seed",
    type=int,
    help="PRNG seed for reproducibility",
)
@click.option(
    "--base-url",
    default=None,
    help=f"API base URL (default: {DEFAULT_API_BASE_URL} or PEPKIO_API_BASE_URL env var)",
)
@click.option(
    "--api-key",
    default=None,
    help="Pepkio API key (default: PEPKIO_API_KEY env var)",
)
@click.option(
    "--output-fasta",
    is_flag=True,
    help="Output FASTA content directly instead of JSON response",
)
def run(
    example: Optional[str],
    input_json: Optional[str],
    sequence_type: Optional[str],
    length: Optional[int],
    count: Optional[int],
    gc_percent: Optional[float],
    seed: Optional[int],
    base_url: Optional[str],
    api_key: Optional[str],
    output_fasta: bool,
):
    """Run the realistic-random-seq-generator tool."""
    try:
        client = PepkioClient(api_key=api_key, base_url=base_url)

        input_data = {}

        if example:
            manifest_data = client.get_manifest()
            examples = manifest_data.get("examples", [])
            matched = next((ex for ex in examples if ex.get("name") == example), None)
            if not matched:
                names = [ex.get("name") for ex in examples if "name" in ex]
                click.echo(
                    f"Error: Example '{example}' not found. Available examples: {', '.join(names)}",
                    err=True,
                )
                sys.exit(1)
            input_data = matched.get("input", {})
        elif input_json:
            try:
                input_data = json.loads(input_json)
            except json.JSONDecodeError as e:
                click.echo(f"Error: Invalid --input-json JSON: {e}", err=True)
                sys.exit(1)
        else:
            if sequence_type is None or length is None or count is None:
                click.echo(
                    "Error: Must specify either --example, --input-json, or "
                    "all required parameters (--sequence-type, --length, --count)",
                    err=True,
                )
                sys.exit(1)
            input_data = {
                "sequence_type": sequence_type,
                "length": length,
                "count": count,
            }
            if gc_percent is not None:
                input_data["gc_percent"] = gc_percent
            if seed is not None:
                input_data["seed"] = seed

        result = client.run(input_data)

        if output_fasta and result.result and "fasta" in result.result:
            click.echo(result.result["fasta"])
        else:
            click.echo(json.dumps(result.model_dump(exclude_none=True), indent=2))

    except PepkioError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("run_id")
@click.option(
    "--base-url",
    default=None,
    help=f"API base URL (default: {DEFAULT_API_BASE_URL} or PEPKIO_API_BASE_URL env var)",
)
@click.option(
    "--api-key",
    default=None,
    help="Pepkio API key (default: PEPKIO_API_KEY env var)",
)
def get(run_id: str, base_url: Optional[str], api_key: Optional[str]):
    """Fetch status and result of a run by ID."""
    try:
        client = PepkioClient(api_key=api_key, base_url=base_url)
        result = client.get_run(run_id)
        click.echo(json.dumps(result.model_dump(exclude_none=True), indent=2))
    except PepkioError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
