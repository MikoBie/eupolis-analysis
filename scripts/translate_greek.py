# %%
from eupolis import RAW, PROC
import pandas as pd
from eupolis.utils import rename_columns, strip_string
from eupolis.translation import WEARABLES_A


# %%
def translate_wearables():
    df = pd.read_csv(RAW / "pireus" / "euPOLIS Piraeus Questionaire-Wearables.csv")
    df = df.rename(columns=lambda x: rename_columns(x)).map(
        lambda x: WEARABLES_A.get(strip_string(x), strip_string(x))
    )
    df.to_excel(PROC / "wearables_pireus.xlsx", index=False)


# %%
if __name__ == "__main__":
    translate_wearables()
