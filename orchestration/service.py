from functools import reduce
from operator import add
from typing import Dict, Iterator, Any

from observability.logger import InvalidDataLogger
from orchestration.pipeline import ProcessingPipeline
from processing.chunker import Chunker
from processing.operations import SumOperation

OPERATIONS = {
    "sum": SumOperation
}


class SumService:
    """Service for processing numeric streams and computing sums."""
    
    def __init__(self, operation: str = "sum", chunk_size: int = 100, log_path: str = "logs/invalid_records.log"):
        """
        Initialize the SumService.
        """
        if operation not in OPERATIONS:
            raise ValueError(f"Unknown operation: {operation}. Available: {list(OPERATIONS.keys())}")
        
        self.chunk_size = chunk_size
        self.logger = InvalidDataLogger(log_path)
        
        self.logger.clear() 
        
        self.operation = OPERATIONS[operation]()
        self.pipeline = ProcessingPipeline(self.logger, self.operation)
        self.log_path = log_path

    def execute(self, stream: Iterator[str]) -> Dict[str, Any]:
        """Execute the service on a stream of data."""

        partials = (
            self.pipeline.run(chunk)
            for chunk in Chunker.chunk(stream, self.chunk_size)
            if chunk
        )

        total = reduce(add, partials, 0)

        return {
            "total": total,
            "invalid_log_file": self.log_path
        }