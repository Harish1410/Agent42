from typing import Any

from core.contracts import Operation
from processing.engine import NumericEngine
import pandas as pd


class SumOperation(Operation):
    """Optimized sum operation with overflow protection."""
    
    def execute(self, data: pd.Series) -> int:
        """
        Execute sum with edge case handling.
        - Empty series returns 0
        - Overflow protection via Python arbitrary precision int
        """
        return NumericEngine.sum(data)
