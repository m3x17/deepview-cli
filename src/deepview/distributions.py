import warnings

import numpy as np
import pandas as pd
from scipy import stats

CANDIDATES = ["norm", "lognorm", "expon", "gamma", "weibull_min", "uniform", "t"]


def fit_distributions(values: pd.Series) -> pd.DataFrame:
    data = values.dropna().to_numpy(dtype=float)
    rows = []
    for name in CANDIDATES:
        dist = getattr(stats, name)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                params = dist.fit(data)
                log_likelihood = np.sum(dist.logpdf(data, *params))
                ks_stat = stats.kstest(data, name, args=params).statistic
        except Exception:
            continue
        if not np.isfinite(log_likelihood):
            continue
        aic = 2 * len(params) - 2 * log_likelihood
        rows.append({"distribution": name, "params": params, "aic": aic, "ks": ks_stat})
    if not rows:
        return pd.DataFrame(columns=["distribution", "params", "aic", "ks"])
    return pd.DataFrame(rows).sort_values("aic").reset_index(drop=True)