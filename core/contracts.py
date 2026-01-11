from abc import ABC, abstractmethod
from typing import Any

import pandas as pd


class Operation(ABC):
    """Abstract base class for data processing operations."""
    
    @abstractmethod
    def execute(self, data: pd.Series) -> Any:
        pass
