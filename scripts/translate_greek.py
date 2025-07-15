# %%
from eupolis import RAW, PROC
import pandas as pd
from eupolis.utils import rename_columns, strip_string
from eupolis.translation import WEARABLES_A, QUESTIONNAIRE_Q, QUESTIONNAIRE_A
import re

# %%


# %%
def translate_wearables():
    df = pd.read_csv(RAW / "pireus" / "euPOLIS Piraeus Questionaire-Wearables.csv")
    df = df.rename(columns=lambda x: rename_columns(x)).map(
        lambda x: WEARABLES_A.get(strip_string(x), strip_string(x))
    )
    df.to_excel(PROC / "wearables_pireus.xlsx", index=False)


def translate_questionnaire():
    rgx = re.compile(r",\s(?=[Α-Ω])")
    df = pd.read_excel(RAW / "pireus" / "euPOLIS Piraeus Questionaire (Responses).xlsx")
    df = df.rename(columns=lambda x: QUESTIONNAIRE_Q.get(x, x)).map(
        lambda x: "; ".join(
            QUESTIONNAIRE_A.get(strip_string(item), strip_string(item))
            for item in rgx.split(x)
        )
        if isinstance(x, str)
        else x
    )
    df.to_excel(PROC / "questionnaire_pireus.xlsx", index=False)


def main():
    translate_wearables()
    translate_questionnaire()


# %%
if __name__ == "__main__":
    main()

# %%
