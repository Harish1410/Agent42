import numpy as np
import pandas as pd


class NumericEngine:
    """Engine for numeric computations."""
    
    @staticmethod
    def sum(series: pd.Series) -> int:
        
        return int(np.sum(series.dropna().astype(object)))
