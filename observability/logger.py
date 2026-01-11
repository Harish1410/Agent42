class InvalidDataLogger:
    
    def __init__(self, log_path: str):
        self.log_path = log_path

    def log_batch(self, values, reason: str):
        with open(self.log_path, "a", encoding="utf-8") as f:
            for val in values:
                f.write(f"{val} | {reason}\n")

    def clear(self):
        """Clear the log file."""
        with open(self.log_path, "w", encoding="utf-8") as f:
            pass  # File is truncated by opening in write mode
