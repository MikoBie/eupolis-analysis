# %%
from eupolis import PROC
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from eupolis.config import COLORS

# %%
df = pd.read_excel(PROC / "kids_pireus.xlsx")
df[df.columns[1]] = df.loc[:, df.columns[1]].apply(lambda x: x.split(";"))

# %%
df.value_counts("Sex")

# %%
lst = []
for _, sex in df.groupby("Sex"):
    n = sex.shape[0]
    count = Counter([el for item in sex[df.columns[1]].tolist() for el in item])
    count = {key: value * 100 / n for key, value in count.items()}
    sex_df = pd.DataFrame({"names": count.keys(), _: count.values()})
    lst.append(sex_df.set_index("names"))
sex = lst[0].join(lst[1], how="outer").reset_index()
# %%
fig, axs = plt.subplots(figsize=(6, 4), nrows=1, ncols=2)
rect = axs[0].barh(
    sex["names"], sex["Male"], color=COLORS["blue"], label="Male (n = 6)"
)
axs[0].bar_label(rect, padding=1, fmt=lambda x: f"{int(round(x, 0))}%")
rect = axs[1].barh(
    sex["names"], sex["Female"], color=COLORS["green"], label="Female (n = 10)"
)
axs[1].bar_label(rect, padding=1, fmt=lambda x: f"{int(round(x, 0))}%")
axs[1].set_yticks([])
for ax in axs:
    for spin in ax.spines:
        if spin != "bottom" and spin != "left":
            ax.spines[spin].set_visible(False)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())

fig.legend(
    ncol=2, loc="center", bbox_to_anchor=(0.6, -0.03), fancybox=True, shadow=True
)
fig.suptitle(
    f"{df.columns[1].replace('1.', '').strip() + '?'}", fontsize=12, weight="bold"
)
fig.tight_layout()
# %%
