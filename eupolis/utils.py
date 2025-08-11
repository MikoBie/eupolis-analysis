import pandas as pd
import datetime
from collections.abc import Callable
from collections import defaultdict
from eupolis.translation import WEARABLES_Q
import re
from collections import Counter


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


def prepare_data(
    df: pd.DataFrame,
    location: str,
    livability: dict,
    after: pd.Timestamp = pd.Timestamp(2020, 1, 1),
    comparison: bool = False,
) -> dict:
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
    group_by = ["time_day"]
    if comparison:
        df["comparison"] = df["date"].apply(
            lambda x: "before" if x < after else "after"
        )
        group_by += ["comparison"]
    df = df.query(f"location.str.contains('{location}')", engine="python")

    dt = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    for item in livability.keys():
        for _, dft in df.groupby(group_by):
            if comparison:
                dt[_[0]][_[1]][item] = dft[item].dropna()
            else:
                dt[_[0]]["before"][item] = dft[item].dropna()

    dt_ord = {}
    for key in ["Morning", "Afternoon", "Evening"]:
        if key in dt:
            dt_ord[key] = dt.pop(key)
    return dt_ord


def share_replace(share_value: float) -> float:
    """Rescale share_cars and share_nature to scale from 1 to 5.

    Parameters
    ----------
    share_value
        the value, it should be a float

    Returns
    -------
        a flaot from 1.0 to 5.0
    """
    dct = {1: 5, 0.7: 4, 0.5: 3, 0.3: 2, 0.1: 1}
    result = share_value
    for key, value in dct.items():
        if share_value <= key:
            result = value
    return result


def count_proportion(srs: pd.Series, cutoff: int = 1) -> float:
    """Compute the proportion of elements bigger than cutoff.

    Parameters
    ----------
    srs
        a series of numeric values
    cutoff, optional
        a value above each the element is counted as present, by default 1

    Returns
    -------
        a proportion of present elements
    """
    return pd.Series([1 if item > cutoff else 0 for item in srs]).mean()


def rescale_number(
    value: float, original_min: int, original_max: int, new_min: int, new_max: int
) -> float:
    """Rescales the variable for a given range.

    Parameters
    ----------
    value
        value to rescale
    original_min
        the minimum of the original scale
    original_max
        the maximum of the original scale
    new_min
        the new minimum
    new_max
        the new maximum

    Returns
    -------
        Rescaled value such as new_min is the minimum of the scale and new_max is the maximum.
    """
    return ((value - original_min) / (original_max - original_min)) * (
        new_max - new_min
    ) + new_min


def rename_columns(s: str, mapping: dict = WEARABLES_Q) -> str:
    """Rename columns based on a mapping dictionary.

    Parameters
    ----------
    s
        The string to be renamed.
    mapping
        A dictionary mapping old column names to new ones.

    Returns
    -------
        The renamed string based on the mapping.
    """
    rgxd = re.compile(r"\d+")
    rgxl = re.compile(r"[abcdefg]\)")
    key = ""
    if rgxd.search(s):
        key = rgxd.search(s).group()
    if rgxl.search(s):
        key += rgxl.search(s).group()
    return (key + " " + mapping.get(key, s)).strip()


def strip_string(x):
    """Returna strip string or the object.

    Parameters
    ----------
    x
        an python object

    Returns
    -------
        returns a stirpped string or a python object
    """
    return x.strip() if isinstance(x, str) else x


def prepare_kids_data(df: pd.DataFrame, column: int) -> pd.DataFrame:
    """Prepares data for plotting by counting occurences of items in a specified column.

    Parameters
    ----------
    df
        a data frame containing the data
    column
        a column index to count items in. The column should contain lists of items.

    Returns
    -------
        a data frame with item names and their counts divided by the sex.
    """
    lst = []
    for _, sex in df.groupby("Sex"):
        n = sex.shape[0]
        count = Counter(
            [el for item in sex[df.columns[column]].tolist() for el in item]
        )
        count = {key: value * 100 / n for key, value in count.items()}
        sex_df = pd.DataFrame({"names": count.keys(), _: count.values()})
        lst.append(sex_df.set_index("names"))
    return lst[0].join(lst[1:], how="outer").reset_index()
