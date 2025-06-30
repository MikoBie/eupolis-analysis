import pytest
from eupolis.utils import (
    rmv_str_frm_lst,
    get_time_label,
    process_lst,
    share_replace,
    count_proportion,
    rescale_number,
    rename_columns,
    strip_string,
)
import pandas as pd
import numpy as np
import datetime
from eupolis.translation import WEARABLES_Q


@pytest.mark.parametrize(
    "srs",
    [
        pd.Series([1, 2, 3, "1"]),
        pd.Series(["1", "2"]),
        pd.Series([1, 2, 3]),
        pd.Series([None]),
        pd.Series([np.nan]),
    ],
)
def test_rmv_str_frm_lst(srs: pd.Series) -> None:
    result = rmv_str_frm_lst(srs)
    assert isinstance(result, pd.Series)
    if not result.empty:
        assert any(not isinstance(item, str) for item in srs)
        assert any(isinstance(item, int) for item in srs) or any(
            isinstance(item, float) for item in srs
        )
    else:
        assert (
            all(isinstance(item, str) for item in srs)
            or srs.empty
            or all(item == item for item in srs)
            or len(srs.dropna()) == 0
        )


@pytest.mark.parametrize(
    "tm",
    [
        (datetime.time(11, 59, 58), "Morning"),
        (datetime.time(17, 59, 58), "Afternoon"),
        (datetime.time(22, 59, 58), "Evening"),
    ],
)
def test_get_time_label(tm: datetime.time) -> None:
    tm, time = tm
    result = get_time_label(tm)
    assert isinstance(result, str)
    assert result == time


@pytest.mark.parametrize(
    "lst",
    [[pd.Series([1]), pd.Series([2, 2])], [pd.Series([])], [pd.Series([2])]],
)
def test_process_lst(lst: list) -> None:
    result = process_lst(lst, func=np.mean)
    assert isinstance(result, list)
    assert result == [np.mean(item) if not item.empty else 0 for item in lst]


@pytest.mark.parametrize(
    "flt",
    [
        (0.1, 1),
        (0.3, 2),
        (0.5, 3),
        (0.7, 4),
        (0.8, 5),
        (np.nan, np.nan),
    ],
)
def test_share_replace(flt: float) -> None:
    value, output = flt
    result = share_replace(value)
    if not np.isnan(result):
        assert isinstance(result, int)
        assert result > 0.9 and result < 5.1
        assert result == output
    else:
        assert result != output


@pytest.mark.parametrize(
    "tpl",
    [
        (pd.Series([np.nan]), 0),
        (pd.Series([np.nan, 1, 2, 3, 4]), np.mean([0, 0, 1, 1, 1])),
        (pd.Series([np.nan, 1, 2, 3, 1]), np.mean([0, 0, 1, 1, 0])),
    ],
)
def test_count_proportion(tpl: tuple) -> None:
    srs, output = tpl
    result = count_proportion(srs)
    assert isinstance(result, float)
    assert result == output


@pytest.mark.parametrize(
    "tpl",
    [(0, 1), (1, 5), (0.5, 3)],
)
def test_rescale_number(tpl: tuple) -> None:
    old, new = tpl
    result = rescale_number(
        value=old, original_min=0, original_max=1, new_min=1, new_max=5
    )
    assert isinstance(result, float)
    assert result == new


@pytest.mark.parametrize(
    "col",
    [
        (
            "12.    Βαθμολογήστε από το 1 έως το 7 τις παρακάτω δηλώσεις (όπου 1 διαφωνώ απόλυτα, και 7 συμφωνώ απόλυτα): [g) Η ευρεία χρήση τέτοιων wearables μπορεί να βελτιώσει τη δημόσια υγεία]",
            "12g)",
        ),
        ("timestamp", "timestamp"),
    ],
)
def test_rename_columns(col: tuple) -> None:
    colname, key = col
    result = rename_columns(colname, mapping=WEARABLES_Q)
    assert isinstance(result, str)
    assert result == (key + " " + WEARABLES_Q.get(key, "")).strip()


def test_strip_string():
    assert strip_string("  test  ") == "test"
    assert strip_string(123) == 123
    assert strip_string(None) is None
    assert strip_string(["test", "strip"]) == ["test", "strip"]
