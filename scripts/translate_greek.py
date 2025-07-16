# %%
from eupolis import RAW, PROC
import pandas as pd
from eupolis.utils import rename_columns, strip_string
from eupolis.translation import (
    WEARABLES_A,
    QUESTIONNAIRE_Q,
    QUESTIONNAIRE_A,
    QUALITY_A,
    DEPRESION_A,
    PEACE_A,
    CRIME_A,
    ENCOURAGEMENT_A,
    MAINTENANCE_A,
    OTHER_A,
)
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
        lambda x: "; ".join(QUESTIONNAIRE_A.get(item, item) for item in rgx.split(x))
        if isinstance(x, str)
        else x
    )
    df.iloc[:, 35:42] = df.iloc[:, 35:42].map(lambda x: QUALITY_A.get(x, x))
    df.iloc[:, 42:63] = df.iloc[:, 42:63].map(lambda x: DEPRESION_A.get(x, x))
    df.iloc[:, 63:66] = df.iloc[:, 63:66].map(lambda x: PEACE_A.get(x, x))
    df.iloc[:, 66:68] = df.iloc[:, 66:68].map(lambda x: CRIME_A.get(x, x))
    df.iloc[:, 68:73] = df.iloc[:, 68:73].map(lambda x: ENCOURAGEMENT_A.get(x, x))
    df.iloc[:, 73:84] = df.iloc[:, 73:84].map(lambda x: MAINTENANCE_A.get(x, x))
    df.iloc[:, 84:] = df.iloc[:, 84:].map(lambda x: OTHER_A.get(x, x))
    df.to_excel(PROC / "questionnaire_pireus.xlsx", index=False)


def main():
    translate_wearables()
    translate_questionnaire()


# %%
if __name__ == "__main__":
    main()

# %%
