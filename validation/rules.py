import re
from typing import Any

import pandas as pd

# NOTE (For future scaling): This function is currently not used - validation uses try/except instead
NUMERIC_REGEX = re.compile(r"^[+-]?\d+$")

def is_numeric(series: pd.Series) -> Any:

    return series.str.match(NUMERIC_REGEX)
