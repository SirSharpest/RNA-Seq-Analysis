import pandas as pd
from glob import glob
from os.path import basename


def make_dataframe(dloc="/Users/hughesn/Transcripts/RNA-Seq/arabidopsis_thaliana/seedling_data/htseq-count/"):
    # Read data
    files = glob("{0}/*".format(dloc))
    dfs = [pd.read_csv(f, sep="\t", skipfooter=5, engine='python',
                       names=['gene', basename(f)]) for f in files]
    data = dfs[0]
    for df in dfs[1:]:
        n = df.columns[1]
        data[n] = df[n]
    data = data.set_index('gene')
    data = data.T
    return data


def add_experimental_details(df):

    new_cols = df.apply(get_experimental_details, axis=1)
    new_cols.columns = ['genotype', 'treatment', 'time', 'uid']
    ndf = df.join(new_cols)
    return (ndf, new_cols)


def get_experimental_details(row):
    n = row.name
    r = n.replace('_1_htseq-count.txt', '')
    s = r.split('_')
    x = pd.Series(s)
    return x


def drop_low_counts(df, n=10, quiet=False):
    b = len(df)
    ndf = df.loc[(df > n).any(axis=1)]
    a = len(ndf)
    if not quiet:
        print("Genes dropped: {0}".format(b-a))
        print(a, b)
    return ndf


def adjust_for_count_differences(df):
    factors = (1+(1-(df.sum()/max(df.sum())))).values
    return df * factors


def drop_non_diff_exp(df):
    def l(x): return x.sum()
    df.loc[(ttest)]
