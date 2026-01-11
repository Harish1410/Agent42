from typing import Any

from core.contracts import Operation
from processing.engine import NumericEngine
import pandas as pd


class SumOperation(Operation):
    """Operation that computes the sum of numeric data."""
    
    def execute(self, data: pd.Series) -> int:
        
        return NumericEngine.sum(data)
