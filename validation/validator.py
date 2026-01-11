import pandas as pd
import gc
from core.config import NUMBER_WORDS

class NumericValidator:
    
    @staticmethod
    def validate(series: pd.Series):
        clean_series = series.astype(str).str.strip()

        def get_invalid_reason(val: str) -> str:
            if not val:
                return "Empty string"
            
            words = val.lower().split()
            if all(word in NUMBER_WORDS for word in words):
                return "Number written in words"
            
            if any(char.isdigit() for char in val):
                return "Contains digits mixed with invalid characters"
            
            return "Not a valid number"

        # 1. Identify which are actually valid integers
        # errors='coerce' turns invalid ones into NaN
        numeric_conversion = pd.to_numeric(clean_series, errors='coerce')
        is_valid = numeric_conversion.notnull()

        # 2. Extract valid data (cast to object for large int support)
        valid_data = numeric_conversion[is_valid].astype(object)

        # 3. Extract invalid data and map the reason without an explicit for loop
        # We pair the original value with the reason string
        invalid_entries = [
            (orig, get_invalid_reason(clean))
            for orig, clean in zip(series[~is_valid], clean_series[~is_valid])
        ]

        # Explicit cleanup
        del clean_series, numeric_conversion
        gc.collect()

        return valid_data, invalid_entries