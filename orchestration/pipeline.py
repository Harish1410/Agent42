from typing import Any, List

import pandas as pd

from core.contracts import Operation
from observability.logger import InvalidDataLogger
from validation.validator import NumericValidator


class ProcessingPipeline:
    """Optimized pipeline with streaming invalid record processing."""
    
    def __init__(self, logger: InvalidDataLogger, operation: Operation):
        self.logger = logger
        self.operation = operation

    def run(self, chunk: List[str]) -> Any:
        """
        Process a chunk with streaming invalid record handling.
        Memory-efficient: invalid records are logged via generator, not materialized.
        """
        series = pd.Series(chunk, dtype=object)
        
        # Get valid data and invalid generator (lazy evaluation)
        valid, invalid_stream = NumericValidator.validate(series)
        
        # Stream invalid records to logger without materializing full list
        self.logger.log_stream(invalid_stream)
        
        # Execute operation on valid data
        result = self.operation.execute(valid)
        
        # Explicit cleanup (series is small per-chunk, but be thorough)
        del series, valid
        
        return result
