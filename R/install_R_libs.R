if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("apeglm")
BiocManager::install("gProfileR")
BiocManager::install("DESeq2")
BiocManager::install("edgeR")
BiocManager::install("org.At.tair.db")
