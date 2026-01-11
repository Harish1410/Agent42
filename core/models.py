from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class NumericRecord:
    """Data model for numeric records with validation status."""
    raw: str
    value: Optional[int]
    error: Optional[str]
