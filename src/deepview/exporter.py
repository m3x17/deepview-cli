from pathlib import Path

import pandas as pd


def export_data(df: pd.DataFrame, output: str) -> None:
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    suffix = target.suffix.lower()
    if suffix == ".csv":
        df.to_csv(target, index=False)
    elif suffix == ".json":
        df.to_json(target, orient="records", indent=2)
    else:
        raise ValueError(f"Unsupported output type: {suffix}")