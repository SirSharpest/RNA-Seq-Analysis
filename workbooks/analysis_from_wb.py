import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from gprofiler import GProfiler
import pandas as pd
import warnings
from scipy.spatial.distance import pdist, squareform
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


counts = pd.read_csv(
    "/Users/nathan/PHD/Transcripts/Data/norml_count_data.csv",
    index_col=0)

DE = read_xl()

counts.sample(20)[counts.columns[:4]]

DE.sample(20)


def get_gene_names(geneList):

    gp = GProfiler(return_dataframe=True)
    df = gp.convert(organism='athaliana',
                    query=geneList)[['incoming', 'name', 'description']]
    df['description'] = df.apply(lambda x: x['description'].split('[')[
                                 0].split(';')[0], axis=1)
    return df


get_gene_names(list(DE.sample(20).index))


fig, ax = plt.subplots(1, figsize=(10, 10))
tmp_counts = pd.DataFrame(counts.sum(), columns=['sum'])
tmp_counts['samples'] = tmp_counts.index.map(lambda x: str(x))
tmp_counts['groups'] = tmp_counts.index.map(lambda x: str(x)[:-4])
sns.barplot(data=tmp_counts, y='samples', x='sum', ax=ax, color="aqua")


def collapse_counts(counts):
    u_cols = list(set([l.rsplit("_", 1)[0] for l in list(counts.columns)]))
    cols = list(counts.columns)
    ss = []
    for uc in u_cols:
        cs = [c for c in cols if c.startswith(uc)]
        ss.append(counts[cs].sum(axis=1).rename(uc))
    dc = pd.concat(ss, axis=1)
    return dc


collapsed_counts = collapse_counts(counts)
lut = dict(zip(list(set([c[:3] for c in collapsed_counts.columns])), "rbg"))
row_colors = [lut[c[:3]] for c in collapsed_counts.columns]
# legend_TN = [mpatches.Patch(color=c, label=l) for (list(set([c[:3] for c in collapsed_counts.columns]))]

distances = pdist(collapsed_counts.T.values, metric='euclidean')
dist_matrix = squareform(distances)
dist_df = pd.DataFrame(
    dist_matrix, columns=collapsed_counts.columns, index=collapsed_counts.columns)
sns.clustermap(dist_df)

pairings_05hr = [['col_c_05h', 'col_w_05h'],
                 ['lym_c_05h', 'lym_w_05h'],
                 ['cer_c_05h', 'cer_w_05h']]

pairings_6hr = [['col_c_6h', 'col_w_6h'],
                ['lym_c_6h', 'lym_w_6h'],
                ['cer_c_6h', 'cer_w_6h']]

pairings_to_lym_05hr = [['col_c_05h', 'lym_w_05h'],
                        ['col_w_05h', 'lym_w_05h'],
                        ['cer_c_05h', 'lym_c_05h'],
                        ['cer_w_05h', 'lym_c_05h']]

pairings_to_lym_6hr = [['col_c_6h', 'lym_w_6h'],
                       ['col_w_6h', 'lym_w_6h'],
                       ['cer_c_6h', 'lym_c_6h'],
                       ['cer_w_6h', 'lym_c_6h']]

cross_time_pairings = [['col_w_05h', 'col_w_6h'],
                       ['lym_w_05h', 'lym_w_6h'],
                       ['cer_w_05h', 'cer_w_6h'],
                       ['col_c_05h', 'col_c_6h'],
                       ['lym_c_05h', 'lym_c_6h'],
                       ['cer_c_05h', 'cer_c_6h']]


DE_pairings_05hr = read_xl('./Data/pairings_05hr.xlsx')
DE_pairings_6hr = read_xl('./Data/pairings_6hr.xlsx')
DE_pairings_to_lym_05hr = read_xl('./Data/pairings_to_lym_05hr.xlsx')
DE_pairings_to_lym_6hr = read_xl('./Data/pairings_to_lym_6hr.xlsx')
DE_cross_time_pairings = read_xl('./Data/cross_time_pairings.xlsx')


def make_clustermap_df(DE, description='description', n=20):
    locs = DE[['log2FoldChange']].groupby(['gene']).sum().sort_values(by='log2FoldChange',
                                                                      ascending=False).head(n).index.values
    top = DE.loc[locs]
    top = top.pivot(columns='sample', values='log2FoldChange')

    locs = DE[['log2FoldChange']].groupby(['gene']).sum().sort_values(by='log2FoldChange',
                                                                      ascending=True).head(n).index.values
    bot = DE.loc[locs]
    bot = bot.pivot(columns='sample', values='log2FoldChange')

    both = pd.concat([top, bot])

    both['gene name'] = list(get_gene_names(
        list(both.index.values))[description])
    both = both.set_index('gene name')

    return both


def get_locs(DE, n, include_large=True, include_small=True):
    samples = DE['sample'].unique()
    locs = []
    for idx, s in enumerate(samples):

        if include_large:
            l1 = DE[DE['sample'] == s][['log2FoldChange']].groupby(['gene']).sum().sort_values(by='log2FoldChange',
                                                                                               ascending=False).head(n).index.values
            locs.extend(l1)
        if include_small:
            l2 = DE[DE['sample'] == s][['log2FoldChange']].groupby(['gene']).sum().sort_values(by='log2FoldChange',
                                                                                               ascending=True).head(n).index.values
            locs.extend(l2)

    locs = np.array(locs)
    return locs


def make_clustermap_df_n_samples(DE, description='description', n=20):
    locs = get_locs(DE, n)
    top = DE.loc[locs]
    top = top.groupby(['sample', 'gene']).mean(
    ).reset_index().set_index('gene')
    top = top.pivot(columns='sample', values='log2FoldChange')
    top['gene name'] = list(get_gene_names(
        list(top.index.values))[description])
    top = top.set_index('gene name')
    return top


df = make_clustermap_df_n_samples(DE_pairings_05hr)
sns.clustermap(df, cmap='bwr', vmin=-10, vmax=10)


fig, ax = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(15, 5))
top = DE_pairings_05hr.groupby(
    ['sample', 'gene']).mean().reset_index().set_index('gene')
top_extracted = top.loc[get_locs(top, 50, include_small=False)]
sns.boxplot(data=top_extracted, x='sample', y='log2FoldChange', ax=ax[0])


bot = DE_pairings_05hr.groupby(
    ['sample', 'gene']).mean().reset_index().set_index('gene')
bot_extracted = bot.loc[get_locs(bot, 50, include_large=False)]
sns.boxplot(data=bot_extracted, x='sample', y='log2FoldChange', ax=ax[1])


df = make_clustermap_df_n_samples(DE_pairings_6hr)

sns.clustermap(df, cmap='bwr', vmin=-10, vmax=10)


fig, ax = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(15, 5))
top = DE_pairings_6hr.groupby(
    ['sample', 'gene']).mean().reset_index().set_index('gene')
top_extracted = top.loc[get_locs(top, 50, include_small=False)]
sns.boxplot(data=top_extracted, x='sample', y='log2FoldChange', ax=ax[0])


bot = DE_pairings_6hr.groupby(
    ['sample', 'gene']).mean().reset_index().set_index('gene')
bot_extracted = bot.loc[get_locs(bot, 50, include_large=False)]
sns.boxplot(data=bot_extracted, x='sample', y='log2FoldChange', ax=ax[1])


df = make_clustermap_df_n_samples(DE_pairings_to_lym_05hr)

sns.clustermap(df, cmap='bwr', vmin=-10, vmax=10)


fig, ax = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(15, 5))
top = DE_pairings_to_lym_05hr.groupby(
    ['sample', 'gene']).mean().reset_index().set_index('gene')
top_extracted = top.loc[get_locs(top, 50, include_small=False)]
sns.boxplot(data=top_extracted, x='sample', y='log2FoldChange', ax=ax[0])


bot = DE_pairings_to_lym_05hr.groupby(
    ['sample', 'gene']).mean().reset_index().set_index('gene')
bot_extracted = bot.loc[get_locs(bot, 50, include_large=False)]
sns.boxplot(data=bot_extracted, x='sample', y='log2FoldChange', ax=ax[1])


df = make_clustermap_df_n_samples(DE_pairings_to_lym_6hr)

sns.clustermap(df, cmap='bwr', vmin=-10, vmax=10)


fig, ax = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(15, 5))
top = DE_pairings_6hr.groupby(
    ['sample', 'gene']).mean().reset_index().set_index('gene')
top_extracted = top.loc[get_locs(top, 50, include_small=False)]
sns.boxplot(data=top_extracted, x='sample', y='log2FoldChange', ax=ax[0])


bot = DE_pairings_6hr.groupby(
    ['sample', 'gene']).mean().reset_index().set_index('gene')
bot_extracted = bot.loc[get_locs(bot, 50, include_large=False)]
sns.boxplot(data=bot_extracted, x='sample', y='log2FoldChange', ax=ax[1])


df = make_clustermap_df_n_samples(DE_cross_time_pairings)

sns.clustermap(df, cmap='bwr', vmin=-10, vmax=10)


fig, ax = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(15, 5))
top = DE_cross_time_pairings.groupby(
    ['sample', 'gene']).mean().reset_index().set_index('gene')
top_extracted = top.loc[get_locs(top, 50, include_small=False)]
sns.boxplot(data=top_extracted, x='sample', y='log2FoldChange', ax=ax[0])


bot = DE_cross_time_pairings.groupby(
    ['sample', 'gene']).mean().reset_index().set_index('gene')
bot_extracted = bot.loc[get_locs(bot, 50, include_large=False)]
sns.boxplot(data=bot_extracted, x='sample', y='log2FoldChange', ax=ax[1])
