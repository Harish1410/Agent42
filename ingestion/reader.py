from typing import Iterator

def stream_lines(path: str) -> Iterator[str]:
    """Stream non-empty stripped lines from a file using a generator expression."""
    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        yield from (stripped for line in file if (stripped := line.strip()))