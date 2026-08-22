# pepkio-realistic-random-seq-generator

Python client and CLI for the Pepkio **Realistic Random Sequence Generator** tool.

Generate composition-realistic DNA, RNA, or protein sequences with GC control, dinucleotide-preserving Markov sampling, ORF framing, motifs, homopolymer limits, and reproducible seeded FASTA export.

## Installation

```bash
pip install pepkio-realistic-random-seq-generator
```

Or using `uv`:

```bash
uv add pepkio-realistic-random-seq-generator
```

## Quick Start

### Environment Setup

Set your Pepkio API key:

```bash
export PEPKIO_API_KEY="your_api_key_here"
```

Optionally override the base URL (defaults to `https://tools.pepkio.com`):

```bash
export PEPKIO_API_BASE_URL="https://tools.pepkio.com"
```

### Python API

```python
from pepkio_realistic_random_seq_generator import PepkioClient, SequenceInput

# Initialize client
client = PepkioClient()

# Get manifest
manifest = client.get_manifest()
print("Tool Title:", manifest["title"])

# Run tool with dict or SequenceInput
result = client.run({
    "sequence_type": "dna",
    "length": 200,
    "count": 5,
    "gc_percent": 50.0,
    "seed": 42
})

print(f"Status: {result.status}")
parsed = result.get_parsed_result()
print(f"Generated {parsed.count} sequences")
print("FASTA Preview:")
print(parsed.fasta[:200])
```

### Command-Line Interface (CLI)

```bash
# Fetch manifest
pepkio-realistic-random-seq-generator manifest

# Run using preset manifest example
pepkio-realistic-random-seq-generator run --example dna_demo

# Run with explicit parameters
pepkio-realistic-random-seq-generator run --sequence-type rna --length 100 --count 3 --gc-percent 45.0 --seed 99

# Run with custom JSON input
pepkio-realistic-random-seq-generator run --input-json '{"sequence_type": "protein", "length": 100, "count": 2, "aa_frequency_preset": "uniprot_average", "seed": 7}'

# Output raw FASTA directly
pepkio-realistic-random-seq-generator run --example dna_demo --output-fasta
```

## License

MIT
