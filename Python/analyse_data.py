import pandas as pd
import seaborn as sns

data_file = pd.ExcelFile(
    "/Users/hughesn/Transcripts/RNA-Seq/Analysis/Data/diff_from_col0:False_onlyDiff:False.xlsx")
sheet_names = data_file.sheet_names

dfs = []
for s in sheet_names:
    d = data_file.parse(s)
    d['sample'] = s.split("|")[0].replace(" ", "")
    dfs.append(d)

df = pd.concat(dfs)

df = df.rename_axis('gene').sort_values(
    by=['gene', 'log2FoldChange'], ascending=[False, False])

bottom = df.iloc[:len(sheet_names)*20]


bottom = bottom.pivot(columns='sample', values='log2FoldChange')
# bottom['Control'] = 0
sns.clustermap(bottom, cmap='bwr', z_score=0)
plt.show()

# top = df.iloc[-20:-1]
