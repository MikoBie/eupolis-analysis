import pandas as pd
import datetime


def rmv_str_frm_lst(srs: pd.Series) -> pd.Series:
    """Remove strings from a list.

    Parameters
    ----------
    lst
        list from which to remove strings.
    """
    return pd.Series([item for item in srs.dropna() if not isinstance(item, str)])


def get_time_label(tm: datetime.time) -> str:
    """Get the label for a given time.

    Parameters
    ----------
    time : datetime.time
        Time to get the label for.

    Returns
    -------
    str
        Label for the time.
    """
    times = {
        datetime.time(12, 0, 0): "Morning",
        datetime.time(18, 0, 0): "Afternoon",
        datetime.time(23, 59, 59): "Evening",
    }
    for time, label in times.items():
        if tm <= time:
            return label


def mean_lst(lst: list) -> list[float]:
    """Computes the mean of nested lists. It returns a list of means for each sublist.

    Parameters
    ----------
    lst : list
        a list-like object containing sublists of numerical values.

    Returns
    -------
    list[float]
        a list of means for each sublist in the input list.
    """
    return [sum(sublist) / len(sublist) if not sublist.empty else 0 for sublist in lst]


def max_lst(lst: list) -> list[float]:
    """Computes the max values of nested lists. It returns a list of max values for each sublist.

    Parameters
    ----------
    lst : list
        a list-like object containing sublists of numerical values.

    Returns
    -------
    list[float]
        a list of max values for each sublist in the input list.
    """
    return [max(sublist) if not sublist.empty else 0 for sublist in lst]


def min_lst(lst: list) -> list[float]:
    """Computes the min values of nested lists. It returns a list of max values for each sublist.

    Parameters
    ----------
    lst : list
        a list-like object containing sublists of numerical values.

    Returns
    -------
    list[float]
        a list of min values for each sublist in the input list.
    """
    return [min(sublist) if not sublist.empty else 0 for sublist in lst]
