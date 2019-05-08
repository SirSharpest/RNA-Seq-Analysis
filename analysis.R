library(edgeR)
library(stringr)
library(gProfileR)
source('./prep_data.R')



## This is all just for SRA data
data <- get_data_and_normalise("../../arabidopsis_thaliana/SRA_Data/seq_counts/")
data.times <-lapply(colnames(data), function(a) str_sub(a,-2,-1))
data.treat <-lapply(colnames(data), function(a) str_sub(a,4,5))
data.treat_time <- mapply(function(a,b) paste(a,b), data.treat, data.times)


plotMDS(data, labels=data.treat_time)
