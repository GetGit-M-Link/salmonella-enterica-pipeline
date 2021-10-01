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
plt.xticks(rotation=45,ha='right')
plt.tight_layout()
plt.savefig("plots/advanced/N50")
plt.clf()

g = sns.catplot(data=df, kind="bar",
x="barcode", y="assemblylength", 
ci="sd", palette="dark", alpha=.6, height=6
)
g.despine(left=True)
g.set_axis_labels("", "assemblylength")
plt.xticks(rotation=45,ha='right')
plt.tight_layout()
plt.savefig("plots/advanced/assemblylength")
plt.clf()

g = sns.catplot(data=df, kind="bar",
x="barcode", y="numberofcontigs", 
ci="sd", palette="dark", alpha=.6, height=6
)
g.despine(left=True)
g.set_axis_labels("", "numberofcontigs")
plt.xticks(rotation=45,ha='right')
plt.tight_layout()
plt.savefig("plots/advanced/numberofcontigs")
plt.clf()

with open("data/Analysis.md",'r') as original: analysis = original.read()
with open("data/Analysis.md",'w') as advanced: 
    advanced.write(f"""## Analysis
#### comparison of the best assemblies
|N50 comparison|assembly length comparison|number of contigs
|---|---|---|
|<img src="../plots/advanced/N50.png" width="400">|<img src="../plots/advanced/assemblylength.png" width="400">|<img src="../plots/advanced/numberofcontigs.png" width="400">|  
  

#### analysis for all assemblies  
  
  """ + analysis)

