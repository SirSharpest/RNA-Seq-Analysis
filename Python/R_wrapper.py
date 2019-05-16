from itertools import combinations as combos
from rpy2.robjects.conversion import localconverter
from os import chdir
from rpy2.robjects import pandas2ri
import rpy2.robjects as robjects
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import pandas as pd

chdir("/Users/hughesn/Transcripts/RNA-Seq/Analysis/R/")
r = robjects.r

r.source("./prep_data.R")
edgeR = importr('edgeR')
stringr = importr('stringr')
gProfileR = importr('gProfileR')
DESeq2 = importr('DESeq2')
pheatmap = importr('pheatmap')
apeglm = importr('apeglm')
base = importr('base')
dollar = base.__dict__["$"]

data_loc = "../../arabidopsis_thaliana/seedling_data/htseq-count_universal_removal"
dds_setup = r['get_DESeq2'](data_loc)
dds = r['DESeq'](dds_setup)
res = r['results'](dds)

treats = list(set(list(r['as.vector'](dollar(dds, 'treatmentID')))))

writer = pd.ExcelWriter(
    '../Data/significantly_different_expressions_no_adaptors.xlsx')

for i, j in combos(treats, 2):
    r_res = r.lfcShrink(dds, contrast=robjects.StrVector(
        ["treatmentID", i, j]))
    r_res = r['as.data.frame'](r_res)
    with localconverter(ro.default_converter + pandas2ri.converter):
        df = ro.conversion.rpy2py(r_res)
        df = df.sort_values(by=['padj'])
        conv = {k: str(k) for k in list(df.columns)}
        df = df.rename(index=str, columns=conv)
        df.to_excel(writer, sheet_name="{0} | {1}".format(i, j))

writer.save()
writer.close()
