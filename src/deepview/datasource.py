from pathlib import Path

import pandas as pd

from deepview.loader import load_data
from deepview.storage import load_stored, stored_names


def load_source(source: str) -> pd.DataFrame:
    if Path(source).exists():
        return load_data(source)
    if source in stored_names():
        return load_stored(source)
    raise FileNotFoundError(f"No file or stored dataset named: {source}")