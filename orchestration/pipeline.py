import gc
from typing import Any, List

import pandas as pd

from core.contracts import Operation
from observability.logger import InvalidDataLogger
from validation.validator import NumericValidator


class ProcessingPipeline:
    """Pipeline for processing data chunks."""
    
    def __init__(self, logger: InvalidDataLogger, operation: Operation):
        
        self.logger = logger
        self.operation = operation

    def run(self, chunk: List[str]) -> Any:
        
        series = pd.Series(chunk, dtype=object)
        valid, invalid = NumericValidator.validate(series)

        for val, reason in invalid:
            self.logger.log_batch([val], reason)

        result = self.operation.execute(valid)

        del series, valid, invalid
        gc.collect()

        return result
