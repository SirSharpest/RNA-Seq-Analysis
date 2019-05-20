from rpy2.robjects import Formula
from itertools import combinations as combos
from rpy2.robjects.conversion import localconverter
from os import chdir
from rpy2.robjects import pandas2ri
import rpy2.robjects as robjects
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import pandas as pd


def write_all_compare_results(dds, treats, r, shrink=False, quiet=True, remove_pvals=False):
    writer = pd.ExcelWriter(
        '../Data/significantly_different_expressions_shrink:{0}_onlyDiff:{1}.xlsx'.format(shrink,
                                                                                          remove_pvals))

    for i, j in combos(treats, 2):
        if not quiet:
            print("Working on {0} | {1}".format(i, j))
        if shrink:
            r_res = r.lfcShrink(dds, contrast=robjects.StrVector(
                ["treatmentID", i, j]))
        else:
            r_res = r.results(dds, contrast=robjects.StrVector(
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
            r_res = r.lfcShrink(dds, contrast=robjects.StrVector(
                ["treatmentID", i, j]))
        else:
            r_res = r.results(dds, contrast=robjects.StrVector(
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


def do_suggested_analysis(dds, r, quiet=True, shrink=False, remove_pvals=False):
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

    for pair, pname in zip([pairings_05hr, pairings_6hr, pairings_to_lym_05hr,
                            pairings_to_lym_6hr, cross_time_pairings],
                           ['pairings_05hr', 'pairings_6hr', 'pairings_to_lym_05hr',
                            'pairings_to_lym_6hr', 'cross_time_pairings']):

        writer = pd.ExcelWriter(
            '../Data/{0}.xlsx'.format(pname))

        for i, j in pair:
            if not quiet:
                print("Working on {0} | {1}".format(i, j))
            if shrink:
                r_res = r.lfcShrink(dds, contrast=robjects.StrVector(
                    ["treatmentID", i, j]))
            else:
                r_res = r.results(dds, contrast=robjects.StrVector(
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


def main():
    chdir("/Users/hughesn/Transcripts/RNA-Seq/Analysis/R/")
    r = robjects.r
    r.source("./prep_data.R")
    libs = {im: importr(im)for im in ['stringr', 'DESeq2', 'base']}
    dollar = libs['base'].__dict__["$"]
    data_loc = "../../arabidopsis_thaliana/seedling_data/htseq-count_universal_removal"
    design = Formula("~ treatmentID")
    dds_setup = r['get_DESeq2'](data_loc, design)
    dds = r['DESeq'](dds_setup)
    do_suggested_analysis(dds, r, quiet=False)

    #treats = list(set(list(r['as.vector'](dollar(dds, 'treatmentID')))))
    # write_all_compare_results(dds, treats, r, quiet=False, remove_pvals=True)
    # write_compare_to_col0(dds, treats, r, quiet=False)
    # counts = R_to_pandas(get_transformed_count_data(dds, r, vst=True), r)


if __name__ == '__main__':
    main()
