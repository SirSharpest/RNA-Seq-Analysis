library(edgeR)
source('./read_data.R')


read_raw_data <- function(data_location){
    data <- get_counts_data(data_location)
    data <- head(data,-5) # summaries are stripped from bottom
    ## Remove the columns which have no transcripts detected
    bad_data <- (colSums(data) != 0)
    data <- data[, bad_data] # all the non-zero columns
    return(data)
}

get_data_and_normalise <- function(data_location){
    data = read_raw_data(data_location)
    groups <- colnames(data)
    dgel <- DGEList(count=data, group=groups)
    ## Here we remove those which are <3 in counts per million reads
    s0 <- dim(dgel)[1]
    dgel <- dgel[rowSums(cpm(dgel)) >= 3,]
    sprintf('%d genes dropped of %d', s0-dim(dgel)[1], s0)
    ## Recalculate sample numbers for normalisation
    dgel$samples$lib.size <- colSums(dgel$counts)
    ## Normalise
    dgel <- calcNormFactors(dgel)
    return(dgel)
}


get_DESeq2 <- function(data_location){
    data = read_raw_data(data_location)
    symbols <- rownames(data$counts)

}

get_gene_names <- function(symbols){
    return (gconvert(symbols, organism = "athaliana", target = "ENSG",
                     region_query = F, numeric_ns = "", mthreshold = Inf,
                     filter_na = T, df = T))
}
