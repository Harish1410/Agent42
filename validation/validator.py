import pandas as pd
import numpy as np
from core.config import NUMBER_WORDS

class NumericValidator:
    """
    Engineered validator using vectorized decision matrices for classification.
    Optimized for high-throughput data streams and arbitrary-precision math.
    """
    
    # Precompile word set for O(1) lookup performance
    _WORD_SET = frozenset(NUMBER_WORDS)
    
    @staticmethod
    def validate(series: pd.Series):
        """
        Validate numeric data using vectorized operations.
        Returns (valid_data, invalid_generator).
        """
        # Vectorized cleanup
        clean_s = series.astype(str).str.strip()
        
        # Fast-path: Convert to numeric using C-engine
        # Coerce handles scientific notation (1e10) and identifies garbage as NaN
        numeric_map = pd.to_numeric(clean_s, errors='coerce')
        is_valid = numeric_map.notna() & np.isfinite(numeric_map)
        
        # Extract Valid Data: Convert to object to support Python's arbitrary-precision ints
        valid_data = numeric_map[is_valid].apply(int).astype(object)
        
        # Prepare slices for the Invalid Decision Matrix
        inv_orig = series[~is_valid]
        inv_cln = clean_s[~is_valid]

        def invalid_generator():
            """Lazy generator that classifies invalid data using vector mapping."""
            if inv_cln.empty:
                return

            # Decision Matrix: Priority is determined by column order (left to right)
            matrix = pd.DataFrame({
                "Empty string": inv_cln == '',
                "Infinity representation": inv_cln.str.lower().isin(['inf', '-inf', 'infinity', '+inf']),
                "Number written in words": inv_cln.apply(
                    lambda v: bool(v) and all(w in NumericValidator._WORD_SET for w in v.lower().split())
                ),
                "Contains digits mixed with invalid characters": inv_cln.str.contains(r'\d', na=False)
            }, index=inv_cln.index)

            # Vectorized Dispatching: Find the first True column name for every row
            reasons = matrix.idxmax(axis=1).where(matrix.any(axis=1), "Not a valid number")

            # Yield from a zip-stream to minimize memory overhead
            yield from zip(inv_orig, reasons)

        return valid_data, invalid_generator()