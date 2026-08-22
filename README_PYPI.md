# Pepkio Realistic Random Sequence Generator

A Python client and command-line package for programmatically generating biologically constrained synthetic DNA, RNA, and protein sequences with exact GC ratios, capped homopolymer lengths, frameshift-free ORFs, and reproducible seeds.

# What It Does

The **Pepkio Realistic Random Sequence Generator** creates statistically realistic biological sequences for bioinformatics, genomics, and synthetic biology applications. Unlike unconstrained uniform random string generation, this package synthesizes DNA, RNA, and peptide sequences under explicit biological rules—such as host-specific GC ratios, homopolymer repeat limits, open reading frames (ORFs) free of premature stop codons, custom motif placements, and UniProtKB amino acid distributions.

# Features

* **Multi-Molecule Generation**: Synthesize DNA, RNA, or protein sequences from 10 to 50,000 residues.
* **GC Content Control**: Specify exact target GC percentages (0.0% to 100.0%) for DNA and RNA.
* **Homopolymer Suppression**: Cap consecutive identical base or amino acid repeats to avoid sequencing artifacts.
* **ORF Framing**: Enforce canonical start codons (`ATG`/`AUG`), eliminate premature stop codons, and terminate with valid stops.
* **Motif & Tail Embedding**: Insert custom nucleotide or peptide motifs (5', 3', or internal) and append customizable RNA poly(A) tails.
* **Empirical Proteomics Models**: Select between uniform amino acid frequencies or empirical UniProtKB average distributions.
* **Deterministic PRNG Seeding**: Pass integer seeds for bit-for-bit reproducible sequence generation.
* **FASTA Export**: Format headers and line-wrapping options (60-char, 80-char, or unwrapped).

# Installation

Install the package via `pip`:

```bash
pip install pepkio-realistic-random-seq-generator
```

Or using `uv`:

```bash
uv add pepkio-realistic-random-seq-generator
```

# Quick Example

Set your environment variable (if using API endpoints) and generate GC-matched synthetic DNA:

```python
from pepkio_realistic_random_seq_generator import PepkioClient, SequenceInput

# Initialize client
client = PepkioClient()

# Generate 3 synthetic DNA sequences matching a 42% target GC content
params = SequenceInput(
    sequence_type="dna",
    length=300,
    count=3,
    gc_percent=42.0,
    homopolymer_max=3,
    seed=12345,
    header_prefix="ctrl_dna"
)

response = client.run(params)
result = response.get_parsed_result()

print(f"Generated {result.count} sequences (actual average GC: {result.gc_actual_percent:.1f}%)")
print(result.fasta)
```

For command-line usage:

```bash
pepkio-realistic-random-seq-generator run --sequence-type dna --length 300 --count 3 --gc-percent 42.0 --seed 12345
```

# Typical Use Cases

* **qPCR & PCR Controls**: Synthesize complex, non-reactive background DNA to test primer cross-reactivity and probe specificity.
* **Motif Discovery Null Models**: Produce GC-matched background sequence sets for HOMER and MEME motif enrichment evaluation.
* **Mass Spectrometry Decoy Databases**: Generate decoy peptide libraries reflecting UniProtKB frequencies to calculate false discovery rates (FDR) in proteomics.
* **Synthetic mRNA Design**: Build in vitro transcription (IVT) construct templates with defined start/stop codons and 3' poly(A) tails.
* **NGS Benchmarking**: Create synthetic reference FASTA sets with controlled GC gradients and homopolymer limits to benchmark mappers and variant callers.

# Scientific Background

* **Nucleotide Thermodynamics & GC Content**: GC pairs contribute 3 hydrogen bonds versus 2 for AT pairs. GC fraction directly influences duplex melting temperature (\(T_m\)) and secondary structure stability:
  \[
  \text{GC\%} = \frac{N_G + N_C}{N_A + N_T + N_G + N_C} \times 100
  \]
* **ORF Stop Codon Probability**: In uniform random DNA (\(P(A)=P(C)=P(G)=P(T)=0.25\)), any triplet has a stop codon probability of \(P(\text{Stop}) = 3/64 \approx 4.69\%\), yielding an expected random ORF length of only ~21 codons. Enforcing ORF constraints removes internal premature stops (`TAA`, `TAG`, `TGA`).
* **Proteomic Residue Frequencies**: Natural proteins deviate significantly from uniform 5.0% amino acid frequencies (e.g., Leucine ~9.65% vs. Tryptophan ~1.08%). Using empirical UniProtKB frequencies produces realistic mass-to-charge (\(m/z\)) distributions for decoy databases.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/realistic-random-seq-generator

The web application allows users to interactively set GC content sliders, configure homopolymer thresholds, visualize sequences in real time, and export FASTA files without writing code.

# Documentation and Resources

GitHub Repository: https://github.com/pepkio/pepkio-realistic-random-seq-generator

Web Application: https://www.pepkio.com/tools/realistic-random-seq-generator

Source and issues: https://github.com/pepkio/pepkio-realistic-random-seq-generator

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

# Keywords

* random DNA sequence generator
* synthetic RNA generator
* random protein sequence generator
* GC content control
* bioinformatics sequence generator
* FASTA generator
* open reading frame generator
* mock sequence generator
* null model background sequence
* decoy peptide generator
* target decoy database proteomics
* random peptide generator
* homopolymer suppression
* seed based sequence generator
* qPCR negative control generator
* motif discovery background sequence
* NGS aligner benchmark
* RNA poly A tail generator
* synthetic mRNA design
* custom amino acid frequency
* UniProt amino acid distribution
* reproducible sequence generation
* molecular biology sequence simulator
* nucleotide composition matching
* biological sequence generator CLI
* Python sequence generator library
* Pepkio bioinformatics tool
* GC matched background generator
* synthetic sequence FASTA generator
* how to generate random DNA with specific GC content
* generate random RNA with poly A tail for IVT controls
* background sequence model generator for HOMER motif search
* MEME motif discovery null control sequence generator
* Proteomics decoy peptide database generator UniProt frequency
* synthetic DNA background matrix for multiplex qPCR assays
* prevent premature stop codons in synthetic DNA sequence
* seed reproducible pseudo random sequence generator Python
* homopolymer limit nucleotide sequence generator for long reads
* realistic random peptide generator mass spectrometry decoy
* command line tool for generating mock FASTA files
* Python API for realistic synthetic nucleotide generation
* generate non target control sequences for primer binding assays
* synthetic ORF generator with start ATG and stop codons
* calculate actual vs target GC percentage in random DNA
