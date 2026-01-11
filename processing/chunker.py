from itertools import islice
from typing import Iterator, TypeVar, List

T = TypeVar('T')

class Chunker:
    
    @staticmethod
    def chunk(iterable: Iterator[T], size: int) -> Iterator[List[T]]:
        """Yield successive chunks from an iterable."""
        
        it = iter(iterable)
        return iter(lambda: list(islice(it, size)), [])
