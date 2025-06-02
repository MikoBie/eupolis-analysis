import pandas as pd
import datetime
from collections.abc import Callable


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


def process_lst(lst: list, func: Callable[[], float] = lambda x: min) -> list[float]:
    """Applies the func to each element of the list. It returns a list of values.

    Parameters
    ----------
    lst : list
        a list-like object containing sublists of numerical values.
    func: Callable
        a function that takes as an argument a list and returns a float.

    Returns
    -------
    list[float]
        a list of values that are the result of applying the func to the element.
    """
    return [func(sublist) if not sublist.empty else 0 for sublist in lst]
