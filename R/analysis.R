library(edgeR)
library(stringr)
library(gProfileR)
library(DESeq2)
library(pheatmap)
library(apeglm)

source('./prep_data.R')

## This is all just for data
data.loc <- "../../arabidopsis_thaliana/seedling_data/htseq-count_universal_removal"
dds.setup <- get_DESeq2(data.loc)

dds <- DESeq(dds.setup)
res <- results(dds)
