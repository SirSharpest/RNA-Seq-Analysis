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




## Check if the controls have any differences
#results(dds, contrast = c("repID", "a1", "b2"))

## res_control_c_v_w <- results(dds, contrast = c("treatmentID", "col_w_05h", "col_c_05h"))
## res_control_c_v_w <- res_control_c_v_w[order(res_control_c_v_w$pvalue),]


## res_col_0_T<- results(dds, contrast = c("treatmentID", "col_w_05h", "col_c_6h"))
## res_col_0_T <- res_col_0_T[order(res_col_0_T$pvalue),]
