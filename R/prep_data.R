library(edgeR)
library(DESeq2)
library(org.At.tair.db)
source('./read_data.R')


read_raw_data <- function(data_location, replace_names=FALSE){
    data <- get_counts_data(data_location)
    data <- head(data,-5) # summaries are stripped from bottom
    ## Remove the columns which have no transcripts detected
    bad_data <- (colSums(data) != 0)
    data <- data[, bad_data] # all the non-zero columns
    return(data)
}


get_data_and_normalise_edgeR <- function(data_location){
    groups <- colnames(data)
    dgel <- DGEList(count=data, group=groups)
    ## Here we remove those which are <3 in counts per million reads
    s0 <- dim(dgel)[1]
    #dgel <- dgel[rowSums(cpm(dgel)) >= 3,]
    sprintf('%d genes dropped of %d', s0-dim(dgel)[1], s0)
    ## Recalculate sample numbers for normalisation
    dgel$samples$lib.size <- colSums(dgel$counts)
    ## Normalise
    dgel <- calcNormFactors(dgel)
    return(dgel)
}


get_DESeq2 <- function(data_location, design){
    data <- read_raw_data(data_location)
    treats <- get_exp_table(data)
    data <- data[rowSums(cpm(data)) >= 5,]
    dds <- DESeqDataSetFromMatrix(data, treats,
                                  design = design)
    return(dds)
}


get_exp_table <- function(data){
    res <- lapply(colnames(data), function(n) unlist(strsplit(n, "_")))
    mat <- do.call(rbind, res)
    genos <- mat[,1]
    treat <- mat[,2]
    time <- mat[,3]
    rep_id <- mat[,4]
    treatments <- data.frame(geno=genos, treatment=treat,
                             time=time, repID=rep_id)
    rownames(treatments) <- apply( treatments , 1 , paste , collapse = "_" )
    treatments['treatmentID'] <- apply( treatments[1:3] , 1 , paste , collapse = "_" )
    return(treatments)
}



get_gene_names <- function(symbols){
    ids <- mapIds(org.At.tair.db, symbols, 'SYMBOL', 'TAIR')
    for(n in names(ids)){
        if (is.na(ids[n])){
            ids[n] <- n
        }
    }
    return(ids)
}

add_gene_names_to_df <- function(df){
    genes <- rownames(df)
    gnames <- get_gene_names(genes)
    df['name'] <- unlist(lapply(rownames(df), function(x) gnames[x]))
    return(df)
}
