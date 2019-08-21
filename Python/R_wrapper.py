from rpy2.robjects import Formula
from itertools import combinations as combos
from rpy2.robjects.conversion import localconverter
from os import chdir
from rpy2.robjects import pandas2ri
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import pandas as pd
from pairings import pairings_05hr, pairings_6hr, pairings_same_treat_05hr
from pairings import cross_time_pairings, stringlis_pairings
from pairings import pairings_same_treat_6hr, pairings_to_lym_05hr, pairings_to_lym_6hr


def write_all_compare_results(dds, treats, r, shrink=False, quiet=True, remove_pvals=False):
    writer = pd.ExcelWriter(
        '../Data/significantly_different_expressions_shrink:{0}_onlyDiff:{1}.xlsx'.format(shrink,
                                                                                          remove_pvals))

    for i, j in combos(treats, 2):
        if not quiet:
            print("Working on {0} | {1}".format(i, j))
        if shrink:
            r_res = r.lfcShrink(dds, contrast=ro.StrVector(
                ["treatmentID", i, j]))
        else:
            r_res = r.results(dds, contrast=ro.StrVector(
                ["treatmentID", i, j]))

        r_res = r['as.data.frame'](r_res)
        df = R_to_pandas(r_res, r)
        df = df.sort_values(by=['padj'])
        if remove_pvals:
            df = df[df['padj'] < 0.01]
        conv = {k: str(k) for k in list(df.columns)}
        df = df.rename(index=str, columns=conv)
        df.to_excel(writer, sheet_name="{0} | {1}".format(i, j))

    writer.save()
    writer.close()


def R_to_pandas(Robj, r):
    with localconverter(ro.default_converter + pandas2ri.converter):
        df = ro.conversion.rpy2py(r['as.data.frame'](Robj))
    return df


def write_compare_to_col0(dds, treats, r, shrink=False, quiet=True, remove_pvals=False):
    writer = pd.ExcelWriter(
        '../Data/diff_from_col0:{0}_onlyDiff:{1}.xlsx'.format(shrink,
                                                              remove_pvals))

    treats.remove("col_w_05h")
    ctrls = ["col_w_05h" for i in treats]

    for i, j in zip(treats, ctrls):
        if not quiet:
            print("Working on {0} | {1}".format(i, j))
        if shrink:
            r_res = r.lfcShrink(dds, contrast=ro.StrVector(
                ["treatmentID", i, j]))
        else:
            r_res = r.results(dds, contrast=ro.StrVector(
                ["treatmentID", i, j]))

        r_res = r['as.data.frame'](r_res)
        df = R_to_pandas(r_res)
        df = df.sort_values(by=['padj'])
        if remove_pvals:
            df = df[df['padj'] < 0.01]
        conv = {k: str(k) for k in list(df.columns)}
        df = df.rename(index=str, columns=conv)
        df.to_excel(writer, sheet_name="{0} | {1}".format(i, j))
    writer.save()
    writer.close()


def get_transformed_count_data(dds, r, vst=False):
    if vst:
        return r.vst(r.assay(dds), blind=False)
    else:
        return r.rlog(r.assay(dds), blind=False)


def make_one_compare(dds, r, treat1, treat2, shrink=False, remove_pvals=False, quiet=False):
    if not quiet:
        print("Working on {0} | {1}".format(treat1, treat2))
    if shrink:
        r_res = r.lfcShrink(dds, type='ashr', contrast=ro.StrVector(
            ["treatmentID", treat1, treat2]))
    else:
        r_res = r.results(dds, contrast=ro.StrVector(
            ["treatmentID", treat1, treat2]))

    r_res = r['as.data.frame'](r_res)
    df = R_to_pandas(r_res, r)
    df = df.sort_values(by=['padj'])
    if remove_pvals:
        df = df[df['padj'] < 0.01]
    conv = {k: str(k) for k in list(df.columns)}
    df = df.rename(index=str, columns=conv)
    return df


def do_suggested_analysis(dds, r, quiet=True, shrink=False, remove_pvals=False, stringlis=False):

    def do_pair(pair, writer, quiet):
        for i, j in pair:
            if not quiet:
                print("Working on {0} | {1}".format(i, j))
            if shrink:
                r_res = r.lfcShrink(dds, type='ashr', contrast=ro.StrVector(
                    ["treatmentID", i, j]))
            else:
                r_res = r.results(dds, contrast=ro.StrVector(
                    ["treatmentID", i, j]))

            r_res = r['as.data.frame'](r_res)
            df = R_to_pandas(r_res, r)
            df = df.sort_values(by=['padj'])
            if remove_pvals:
                df = df[df['padj'] < 0.01]
            conv = {k: str(k) for k in list(df.columns)}
            df = df.rename(index=str, columns=conv)
            df.to_excel(writer, sheet_name="{0} | {1}".format(i, j))

    if stringlis:
        for pair, pname in zip([stringlis_pairings], ['stringlis']):
            writer = pd.ExcelWriter(
                '../Data/{0}_{1}.xlsx'.format(pname, shrink))
            do_pair(pair, writer, quiet)
        writer.save()
        writer.close()
    else:
        for pair, pname in zip([pairings_same_treat_05hr, pairings_same_treat_6hr,
                                pairings_05hr, pairings_6hr, pairings_to_lym_05hr,
                                pairings_to_lym_6hr, cross_time_pairings],
                               ['pairings_same_treat_05hr', 'pairings_same_treat_6hr',
                                'pairings_05hr', 'pairings_6hr', 'pairings_to_lym_05hr',
                                'pairings_to_lym_6hr', 'cross_time_pairings']):
            writer = pd.ExcelWriter(

                '../Data/{0}.xlsx'.format(pname))
            do_pair(pair, writer, quiet)

            writer.save()
            writer.close()


def go_seq_prep(dds, r, counts):
    """
    As per MIL recomendations:

    "In order to perform a GO analysis of your RNA-seq data, goseq only requires a simple named vector,
    which contains two pieces of information.
    1. Measured genes: all genes for which RNA-seq data was gathered for your experiment.
       Each element of your vector should be named by a unique gene identifier.

    2. Differentially expressed genes: each element of your vector should be either a 1 or a 0,
        where 1 indicates that the gene is differentially expressed and 0 that it is not.
    "

    So this can be obtained with:
    """
    rowsum_threshold = 1  # user chosen
    fdr_threshold = 0.1  # user chosen
    rs = r.rowSums(r.counts(dds))
    # use count threshold instead of IF
    res = r.results(dds, independentFiltering=False)
    assayed_genes = r.rownames(res)
    # de_genes = r.rownames(res)[which(res$padj < fdr.threshold)]


def main():
    chdir("/Users/hughesn/Transcripts/RNA-Seq/Analysis/R/")
    r = ro.r
    r.source("./prep_data.R")
    libs = {im: importr(im)for im in ['stringr', 'DESeq2', 'base']}
    dollar = libs['base'].__dict__["$"]
    # Original data
    data_loc = "/Users/hughesn/Transcripts/RNA-seq/arabidopsis_thaliana/backup_data/htseq-count_universal_removal"
    # Stringlis
    # data_loc = "/Volumes/HPC-Home/Stringlis/HTSEQ"

    design = Formula("~ treatmentID")
    dds_setup = r['get_DESeq2'](data_loc, design)
    dds = r['DESeq'](dds_setup)

    #do_suggested_analysis(dds, r, quiet=False, shrink=False, stringlis=True)
    #do_suggested_analysis(dds, r, quiet=False, shrink=True, stringlis=True)
    do_suggested_analysis(dds, r, quiet=False, shrink=True)
    counts = R_to_pandas(get_transformed_count_data(dds, r, vst=True), r)
    counts.to_csv('../Data/stringlis_counts_nonCPM.csv')


if __name__ == '__main__':
    main()
