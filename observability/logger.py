from typing import Iterator, Tuple
from collections import deque


class InvalidDataLogger:
    """Optimized logger with batched I/O operations."""
    
    def __init__(self, log_path: str, buffer_size: int = 1000):
        self.log_path = log_path
        self.buffer_size = buffer_size
        self._buffer = deque()

    def log_stream(self, invalid_stream: Iterator[Tuple[str, str]]):
        
        with open(self.log_path, "a", encoding="utf-8") as f:
            # Process stream: append to buffer and flush only when condition met
            [(self._buffer.append(f"{v} | {r}\n"), 
            len(self._buffer) >= self.buffer_size and (f.writelines(self._buffer), self._buffer.clear())) 
            for v, r in invalid_stream]
            
            # Final flush using a single-line conditional
            self._buffer and (f.writelines(self._buffer), self._buffer.clear())

    def log_batch(self, values, reason: str):
        
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.writelines([f"{val} | {reason}\n" for val in values])

    def clear(self):
        """Atomic clear."""
        open(self.log_path, "w", encoding="utf-8").close()