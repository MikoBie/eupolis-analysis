import pandas as pd
import datetime
from collections.abc import Callable
from collections import defaultdict


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


def prepare_data(df: pd.DataFrame, location: str, livability: dict) -> dict:
    """Prepare data for plotting radar plots. It returns a dictionary where keys are time of the day and values lists of the results.

    Parameters
    ----------
    df
        data frame with Spatial Audits
    location
        the name of the city or place. It uses contains so it does not have to be the whole name
    livability, optional
        dictionary with livability dimmensions as keys. The values are the names of specific columns, by default LIVABILITY

    Returns
    -------
        A dictionary where keys are times of the day and values lists of the results.
    """
    df = df.query(f"location.str.contains('{location}')", engine="python")
    dt = defaultdict(lambda: defaultdict(float))
    for item in livability.keys():
        for _, dft in df.groupby("time_day"):
            dt[_][item] = dft[item].dropna()
    dt_ord = {}
    for key in ["Morning", "Afternoon", "Evening"]:
        if key in dt:
            dt_ord[key] = dt.pop(key)
    return dt_ord
