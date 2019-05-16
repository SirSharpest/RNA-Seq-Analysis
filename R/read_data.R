library(tools)
## Small helper function
read_tsv_filename <- function(filename){
    tbl <- read.table(filename, header=FALSE, sep="\t", row.names = 1)
    names(tbl) <- file_path_sans_ext(basename(filename))
    return(tbl)
}

get_counts_data <- function(path){
    ## Loads in count data files
    files <- list.files(path = path, full.names = TRUE)
    df  <- do.call(cbind,lapply(files,function(fn)read_tsv_filename(fn)))
    colnames(df)<-sub("_1_htseq-count", "", colnames(df))
    return(df)
}
