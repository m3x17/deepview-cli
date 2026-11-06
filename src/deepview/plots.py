from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def show_histogram(values: pd.Series, title: str, bins: int = 20, save: str | None = None) -> None:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(values.dropna(), bins=bins)
    ax.set_title(title)
    ax.set_xlabel("value")
    ax.set_ylabel("count")
    fig.tight_layout()
    if save:
        target = Path(save)
        target.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(target, dpi=150)
        plt.close(fig)
    else:
        plt.show()