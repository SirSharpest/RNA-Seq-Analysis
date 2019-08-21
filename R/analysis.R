###
### if you need to install libs use the install_R_libs.R file
# source('install_R_libs.R')
###


library(edgeR)
library(stringr)
library(gProfileR)
library(DESeq2)
library(apeglm)



## NB set working directory to where this file is! 
## and also will need to change data.loc location 

source('./prep_data.R')

## This is all just for data
data.loc <- "/Users/hughesn/Transcripts/RNA-seq/arabidopsis_thaliana/backup_data/htseq-count_universal_removal"
dds.setup <- get_DESeq2(data.loc, ~ treatmentID)
dds <- DESeq(dds.setup)


## E.G.
col_results <- results(dds, contrast = c('treatmentID', 'col_c_05h', 'col_w_05h'))
col_results.dataframe <- as.data.frame(col_results)