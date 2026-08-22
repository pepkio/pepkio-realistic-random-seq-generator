from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field


class SequenceItem(BaseModel):
    id: int
    sequence: str


class SequenceInput(BaseModel):
    sequence_type: Literal["dna", "rna", "protein"] = Field(
        ..., description="Sequence type (dna, rna, or protein)"
    )
    length: int = Field(..., ge=10, le=50000, description="Sequence length in bp or aa")
    count: int = Field(..., ge=1, le=100, description="Number of sequences to generate")
    tab: Optional[str] = Field(default="generator", description="UI tab (generator | history)")
    gc_percent: Optional[float] = Field(
        default=None, ge=0, le=100, description="Target GC% for DNA/RNA (0-100)"
    )
    homopolymer_max: Optional[int] = Field(
        default=None, description="Maximum homopolymer run length"
    )
    seed: Optional[int] = Field(
        default=None, description="PRNG seed for reproducibility"
    )
    enforce_orf: Optional[bool] = Field(
        default=None, description="Coding ORF with start codon, no internal stops, terminal stop"
    )
    poly_a_tail: Optional[int] = Field(
        default=None, description="Poly(A) tail length appended to RNA 3' end"
    )
    motif: Optional[str] = Field(default=None, description="Fixed motif sequence to embed")
    motif_position: Optional[Literal["start", "end", "random"]] = Field(
        default=None, description="Motif insertion position"
    )
    aa_frequency_preset: Optional[Literal["uniform", "uniprot_average", "custom"]] = Field(
        default=None, description="Amino acid frequency preset"
    )
    custom_aa_frequencies: Optional[Dict[str, float]] = Field(
        default=None, description="Custom AA frequency map (percent)"
    )
    header_prefix: Optional[str] = Field(
        default=None, description="FASTA header prefix (default: seq)"
    )
    line_wrap: Optional[Union[int, str]] = Field(
        default=None, description="FASTA line wrap length (60, 80, or none)"
    )


class RunOptions(BaseModel):
    idempotency_key: Optional[str] = Field(default=None, description="Optional idempotency key")
    label: Optional[str] = Field(default=None, description="Optional label for the run")
    share: Optional[str] = Field(default=None, description="Optional sharing setting")


class ToolResultData(BaseModel):
    tab: Optional[str] = None
    sequence_type: Optional[str] = None
    sequences: Optional[List[SequenceItem]] = None
    fasta: Optional[str] = None
    download_filename: Optional[str] = None
    seed: Optional[int] = None
    gc_target: Optional[float] = None
    gc_actual_percent: Optional[float] = None
    length: Optional[int] = None
    count: Optional[int] = None
    generation_time_ms: Optional[int] = None
    warnings: Optional[List[str]] = None
    error: Optional[str] = None


class RunResult(BaseModel):
    run_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[Any] = None
    result_url: Optional[str] = None
    permalink: Optional[str] = None

    def get_parsed_result(self) -> Optional[ToolResultData]:
        """Convenience method to return the result parsed as ToolResultData."""
        if self.result:
            return ToolResultData(**self.result)
        return None
