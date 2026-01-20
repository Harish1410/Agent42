import os
import time
import tracemalloc
import gc
import psutil
from typing import Dict, List, Any

from core.config import CHUNK_SIZE
from ingestion.generator import generate
from ingestion.reader import stream_lines
from orchestration.service import SumService

def count_lines(file_path: str) -> int:
    """Helper to count lines in a file safely."""
    try:
        if not os.path.exists(file_path):
            return 0
        with open(file_path, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0

class SumPipeline:
    """Orchestrates multiple pipeline runs and tracks performance metrics."""

    def __init__(self, chunk_size: int):
        self.chunk_size = chunk_size
        self.results = {}
        self.process = psutil.Process(os.getpid())
        os.makedirs("data", exist_ok=True)
        os.makedirs("logs", exist_ok=True)

    def run_sizes(self, sizes: List[int], generator_func) -> Dict[int, Dict[str, Any]]:
        """Run pipeline for multiple input sizes and benchmark each."""
        for size in sizes:
            # 1. Setup paths
            input_path = f"data/input_{size}.txt"
            # We will move the default log to this unique path after each run
            final_log_path = f"logs/invalid_{size}.log"
            
            # 2. Generate Data
            generator_func(input_path, size)

            # 3. Initialize Service (One service per run ensures a clean log start for each size)
            service = SumService(chunk_size=self.chunk_size, log_path="logs/temp_invalid.log")

            # 4. Start Tracking
            gc.collect() 
            tracemalloc.start()
            start_time = time.time()

            # 5. Execute
            result = service.execute(stream_lines(input_path))

            # 6. End Tracking
            end_time = time.time()
            _, peak_bytes = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            memory_used_mb = self.process.memory_info().rss / (1024 * 1024)

            # 7. Move/Rename the log file for this specific size
            if os.path.exists(result["invalid_log_file"]):
                os.replace(result["invalid_log_file"], final_log_path)

            # 8. Calculate Stats
            total_records = count_lines(input_path)
            invalid_records = count_lines(final_log_path)
            valid_records = total_records - invalid_records

            # 9. Store metrics
            self.results[size] = {
                "sum_result": result["total"],
                "total_records": total_records,
                "valid_records": valid_records,
                "invalid_records": invalid_records,
                "time_taken_sec": round(end_time - start_time, 4),
                "algorithm_peak_mb": round(peak_bytes / (1024 * 1024), 4),
                "process_rss_mb": round(memory_used_mb, 4),
                "input_path": input_path,
                "invalid_log_file": final_log_path,
            }
        
        return self.results

if __name__ == "__main__":
    input_sizes = [500, 1000, 10000]
    pipeline = SumPipeline(chunk_size=CHUNK_SIZE)
    all_results = pipeline.run_sizes(input_sizes, generate)

    for size, metrics in all_results.items():
        print(f"\n========== INPUT SIZE: {size} ==========")
        print(f"SUM RESULT        : {metrics['sum_result']}")
        print(f"Total records     : {metrics['total_records']}")
        print(f"Valid records     : {metrics['valid_records']}")
        print(f"Invalid records   : {metrics['invalid_records']}")
        print("----------------------------------------")
        print(f"Time taken        : {metrics['time_taken_sec']} seconds")
        print(f"Process RSS       : {metrics['process_rss_mb']} MB")
        print(f"Algorithm peak    : {metrics['algorithm_peak_mb']} MB")
        print(f"Input file        : {metrics['input_path']}")
        print(f"Invalid log file  : {metrics['invalid_log_file']}")
        print("========================================")