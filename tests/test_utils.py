import pytest
from eupolis.utils import rmv_str_frm_lst, get_time_label, process_lst
import pandas as pd
import numpy as np
import datetime


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
