import pandas as pd

def summarize(df: pd.DataFrame) -> pd.DataFrame:
    numeric = df.select_dtypes(include="number")
    stats = numeric.describe().T
    stats["missing"] = numeric.isna().sum()
    return stats.reset_index().rename(columns={"index": "column"})