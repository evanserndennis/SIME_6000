import numpy as np
import pandas as pd
from scipy import stats

_F_THRESHOLD = 0.2
_ALPHA = 0.01


def f_test(a_statistics: list, b_statistics: list) -> np.ndarray:
    a_var, a_n = a_statistics
    b_var, b_n = b_statistics

    f_stat = a_var / b_var

    a_dof = a_n - 1
    b_dof = b_n - 1

    cdf = stats.f.cdf(f_stat, a_dof, b_dof)

    p_value = 2 * np.minimum(cdf, 1 - cdf)

    return p_value > _F_THRESHOLD


def t_test(
        a_statistics: pd.DataFrame, b_statistics: pd.DataFrame) -> np.ndarray:
    a_mean, a_var, a_n = (
        a_statistics[c].to_numpy() for c in ('mean', 'var', 'count'))
    b_mean, b_var, b_n = (
        b_statistics[c].to_numpy() for c in ('mean', 'var', 'count'))


    equal_variances = f_test(
        a_statistics=[a_var, a_n], b_statistics=[b_var, b_n])

    p_equal = stats.ttest_ind_from_stats(
        a_mean, np.sqrt(a_var), a_n,
        b_mean, np.sqrt(b_var), b_n,
        equal_var=True).pvalue

    p_unequal = stats.ttest_ind_from_stats(
        a_mean, np.sqrt(a_var), a_n,
        b_mean, np.sqrt(b_var), b_n,
        equal_var=False).pvalue

    p_value = np.where(equal_variances, p_equal, p_unequal)

    return p_value < _ALPHA
