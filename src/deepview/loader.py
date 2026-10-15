from pathlib import Path

import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    file = Path(path)
    if not file.exists():
        raise FileNotFoundError(f"File not found: {path}")
    suffix = file.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(file)
    if suffix == ".json":
        return pd.read_json(file)
    raise ValueError(f"Unsupported file type: {suffix}")