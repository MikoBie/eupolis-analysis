# %%
from eupolis import PROC, PNG
import pandas as pd
from eupolis.plots import plot_kids_barhplot, plot_kids_barplot
from eupolis.utils import prepare_kids_data

# %%
df = pd.read_excel(PROC / "kids_pireus.xlsx")
df[df.columns[1]] = df.loc[:, df.columns[1]].apply(
    lambda x: [item.strip() for item in x.split(";")]
)
df[df.columns[7]] = df.loc[:, df.columns[7]].apply(
    lambda x: [item.strip() for item in x.split(";")] if isinstance(x, str) else []
)
df[df.columns[8]] = df.loc[:, df.columns[8]].apply(
    lambda x: [item.strip() for item in x.split(";")] if isinstance(x, str) else []
)

# %%
df.value_counts("Sex")

# %%
## What are you usually doing while you are in the schoolyard?
df_1 = prepare_kids_data(df, 1).fillna(0)
fig = plot_kids_barhplot(df_1)

fig.legend(
    ncol=2, loc="center", bbox_to_anchor=(0.6, -0.03), fancybox=True, shadow=True
)
## fig.suptitle(
##     f"{df.columns[1].replace('1.', '').strip() + '?'}", fontsize=12, weight="bold"
## )
fig.tight_layout()
fig.savefig(PNG / "kids_1.png", dpi=200, bbox_inches="tight")
# %%
## What do you like about the schoolyard?
df_2 = prepare_kids_data(df, 7).fillna(0).query("names != ''")
fig = plot_kids_barhplot(df_2)


fig.legend(
    ncol=2, loc="center", bbox_to_anchor=(0.6, -0.03), fancybox=True, shadow=True
)
## fig.suptitle(f"{df.columns[7].replace('5.', '').strip()}", fontsize=12, weight="bold")
fig.tight_layout()
fig.savefig(PNG / "kids_2.png", dpi=200, bbox_inches="tight")

# %%
## What do you dislike about the schoolyard?
df_3 = prepare_kids_data(df, 8).fillna(0)
fig = plot_kids_barhplot(df_3)

fig.legend(
    ncol=2, loc="center", bbox_to_anchor=(0.6, -0.03), fancybox=True, shadow=True
)
## fig.suptitle(f"{df.columns[8].replace('6.', '').strip()}", fontsize=12, weight="bold")
fig.tight_layout()
fig.savefig(PNG / "kids_3.png", dpi=200, bbox_inches="tight")
# %%
## While you are in the schoolyard do you spend your time alone of with other kids?
df.iloc[:, 2].value_counts()

# %%
## Whould you like to have spend more or less time in the schoolyard during your day at school?
df.iloc[:, 3].value_counts()

# %%
## You can give stars to places listed below. Please give one star if you don’t like being there, three stars if it is OK, and five stars if you really like being there a lot

fig = plot_kids_barplot(df=df)

## fig.suptitle(
##     "How much do you like the following places (1-5)?", fontsize=12, weight="bold"
## )
fig.tight_layout()
fig.savefig(PNG / "kids_4.png", dpi=200, bbox_inches="tight")
# %%
