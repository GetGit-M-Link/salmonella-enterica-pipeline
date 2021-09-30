import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv('data/best_data.txt')

g = sns.catplot(data=df, kind="bar",
x="barcode", y="N50", 
ci="sd", palette="dark", alpha=.6, height=6
)
g.despine(left=True)
g.set_axis_labels("", "N50")
g.legend.set_title("k")
plt.savefig("plots/advanced/N50")
plt.clf()

g = sns.catplot(data=df, kind="bar",
x="barcode", y="assemblylength", 
ci="sd", palette="dark", alpha=.6, height=6
)
g.despine(left=True)
g.set_axis_labels("", "assemblylength")
g.legend.set_title("k")
plt.savefig("plots/advanced/assemblylength")
plt.clf()

g = sns.catplot(data=df, kind="bar",
x="barcode", y="numberofcontigs", 
ci="sd", palette="dark", alpha=.6, height=6
)
g.despine(left=True)
g.set_axis_labels("", "numberofcontigs")
g.legend.set_title("k")
plt.savefig("plots/advanced/numberofcontigs")
plt.clf()



