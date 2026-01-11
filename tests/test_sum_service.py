import pytest

from ingestion.generator import generate
from ingestion.reader import stream_lines
from orchestration.service import SumService


def run_case(tmp_path, count, chunk):
    path = tmp_path / f"input_{count}.txt"
    generate(str(path), count)

    service = SumService(chunk_size=chunk)
    result = service.execute(stream_lines(path))

    assert isinstance(result, dict)
    assert "total" in result
    assert "invalid_log_file" in result

    assert isinstance(result["total"], int)
    assert result["invalid_log_file"].endswith(".log")

    return result


@pytest.mark.parametrize(
    "count,chunk",
    [
        (10, 2),
        (50, 10),
        (500, 100),
        (1000, 200),
        (10000, 1000),
    ]
)
def test_sum_service_for_any_input_size(tmp_path, count, chunk):
    run_case(tmp_path, count, chunk)
