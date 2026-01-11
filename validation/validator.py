import pandas as pd
import gc
from core.config import NUMBER_WORDS

class NumericValidator:
    
    @staticmethod
    def validate(series: pd.Series):
        
        series = series.astype(object)
        valid, invalid = [], []

        for val in series:
            clean = str(val).strip()
            
            if not clean: 
                invalid.append((val, "Empty string"))
                continue
            
            try:
                valid.append(int(clean))
            except (ValueError, TypeError):
                words = clean.lower().split()
                
                if all(word in NUMBER_WORDS for word in words):
                    reason = "Number written in words"
                elif any(char.isdigit() for char in clean) and not clean.isdigit():
                    reason = "Contains digits mixed with invalid characters"
                else:
                    reason = "Not a valid number"
                
                invalid.append((val, reason))

        del series
        gc.collect()

        return pd.Series(valid, dtype=object), invalid