from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE, RFECV
from gprofiler import GProfiler
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


def read_xl(fn="/Users/nathan/PHD/Transcripts/Data/diff_from_col0:False_onlyDiff:False.xlsx"):
    xl = pd.ExcelFile(fn)
    sheet_names = xl.sheet_names
    dfs = []
    for s in sheet_names:
        d = xl.parse(s)
        d['sample'] = s.split("|")[0].replace(" ", "")
        dfs.append(d)

    DE = pd.concat(dfs)
    DE = DE.rename_axis('gene').sort_values(by=['gene', 'log2FoldChange'],
                                            ascending=[False, False])
    return DE


def get_gene_names(geneList):
    gp = GProfiler(return_dataframe=True)
    df = gp.convert(organism='athaliana',
                    query=geneList)[['incoming', 'name', 'description']]
    df['description'] = df.apply(lambda x: x['description'].split('[')[
        0].split(';')[0], axis=1)
    return df


counts = pd.read_csv(
    "/Users/hughesn/PHD/Transcripts/Data/norml_count_data.csv", index_col=0)
counts[[c for c in counts.columns if 'cer_c' in c]].head(5)


# load data
DE_pairings_05hr = read_xl('./Data/pairings_05hr.xlsx')
sig = DE_pairings_05hr[DE_pairings_05hr['padj'] < 1]
sig = sig['log2FoldChange'].sort_values()
locs = sig.index
df = counts.loc[locs][[c for c in counts.columns if (
    '05h' in c and ('col' in c or 'lym' in c or 'cer' in c))]].T
df = df.loc[:, ~df.columns.duplicated()]
df = df[[c for c in set(df.columns.values)]]

# Feature Extraction with RFE
X = df.values
y = [y.rsplit('_', 1)[0] for y in df.reset_index()['index']]
# feature extraction
model = LogisticRegression()
rfe = RFE(model, n_features_to_select=25)
fit = rfe.fit(X, y)
print("Num Features: {0}".format(fit.n_features_))
print("Selected Features: {0}".format(fit.support_))
print("Feature Ranking: {0}".format(fit.ranking_))


genes = []
for r, f in zip(fit.ranking_, df.columns.values):
    if r == 1:
        genes.append(f)
        get_gene_names(genes)


rfe_forest = counts.loc[genes][[c for c in counts.columns if (
    '05h' in c and ('col' in c or 'lym' in c))]].T
rfe_forest = rfe_forest.loc[:, ~rfe_forest.columns.duplicated()]
rfe_forest = rfe_forest[[c for c in set(rfe_forest.columns.values)]]

feat_labels = rfe_forest.columns.values
y = [d.rsplit('_', 1)[0] for d in rfe_forest.index.values]

X_train, X_test, y_train, y_test = train_test_split(
    rfe_forest.values, y, test_size=1, random_state=42)
forest = RandomForestClassifier(n_estimators=20000, random_state=1, n_jobs=-1)
forest.fit(X_train, y_train)
res = {k: v for k, v in sorted(
    zip(feat_labels, forest.feature_importances_), key=lambda x: x[1], reverse=True)}
res_df = pd.DataFrame(list(res.items()), columns=[
                      'gene', 'importance']).set_index('gene')
names = get_gene_names(list(res_df.index))
res_df = pd.merge(res_df, names, left_index=True, right_on='incoming').rename(
    columns={'incoming': 'gene'}).set_index('gene').sort_values('importance', ascending=False)


res_df.to_csv('results.csv')
joblib.dump(forest, 'saved_model.pkl')
