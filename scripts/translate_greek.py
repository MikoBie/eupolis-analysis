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
    KIDS,
)
import re


# %%
def translate_wearables(df: pd.DataFrame, output_name: str = "wearables_pireus.xlsx"):
    """Translates the questions and answers of the wearables questionnaire.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to translate.
    output_name : str, optional
        The name of the output file, by default "wearables_pireus.xlsx".
    """
    df = df.rename(columns=lambda x: rename_columns(x)).map(
        lambda x: WEARABLES_A.get(strip_string(x), strip_string(x))
    )
    df.to_excel(PROC / output_name, index=False)


def translate_questionnaire(
    df: pd.DataFrame, output_name: str = "questionnaire_pireus.xlsx"
):
    """Translates the questions and answers of the Greek questionnaire.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to translate.
    output_name : str, optional
        The name of the output file, by default "questionnaire_pireus.xlsx".
    """
    rgx = re.compile(r",\s(?=[Α-Ω])")
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
    df.to_excel(PROC / output_name, index=False)


def process_kids():
    """Process the questionnaire from Rallion School."""
    df = pd.read_excel(RAW / "pireus" / "kids_questionnaire.xlsx")
    for n, dct in KIDS.items():
        df[df.iloc[:, n].name] = df[df.iloc[:, n].name].map(
            lambda x: "; ".join(
                dct.get(strip_string(item), strip_string(item))
                for item in str(x).split(";")
            )
        )
    df.to_excel(PROC / "kids_pireus.xlsx", index=False)


def main():
    df = pd.read_csv(RAW / "pireus" / "euPOLIS Piraeus Questionaire-Wearables.csv")
    translate_wearables(df=df)
    df_after = pd.read_csv(
        RAW / "pireus" / "euPOLIS Piraeus Questionaire-Wearables-Final 26-9-2025.csv"
    )
    translate_wearables(df=df_after, output_name="wearables_pireus_after.xlsx")
    df = pd.read_excel(RAW / "pireus" / "euPOLIS Piraeus Questionaire (Responses).xlsx")
    translate_questionnaire(df=df)
    df = pd.read_excel(
        RAW
        / "pireus"
        / "euPOLIS Piraeus Questionaire Sept 26 - After Interventions (Responses).xlsx"
    )
    translate_questionnaire(df=df, output_name="questionnaire_pireus_after.xlsx")
    process_kids()


# %%
if __name__ == "__main__":
    main()

# %%
