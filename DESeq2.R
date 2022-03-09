library(limma)
library(DESeq2)

#' Run DESeq2
#'
#' Perform differential expression analysis using DESeq2. DESeq2 sample-normalizes gene expression, then
#' builds a negative binomial glm for each gene. Here we use the likelihood ratio test of the test variable against
#' any other covariates you specify.
#'
#' @param input_counts Path to a text file containing raw RNAseq counts, formatted s.t. genes are rows and samples are columns.
#' @param sample_info_path Path to a text file containing sample metadata, formatted s.t. samples are rows and metadata are columns.
#' @param on Perform DE analysis w.r.t. this variable. Must be a column header of sample_info_path.
#' @param control Regress out these variables. Must be column headers of sample_info_path
#' @param comparisons Pairwise comparisons. Must be values in param on. List of list.
#' @param output_dir DESeq2 output tables are written here. Defaults to current directory.
#' @param qvalue.threshold FDR threshold. Default 0.05.
#'
#' @return Returns the DESeq2 object.
#'
#' @references
#' DESeq2 tutorial vignette:
#' http://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html
#'
#' @importFrom roxygen2 roxygenise
#' @export
#'
#' @md
DESeq2 = function(
  input_counts,
  sample_info_path,
  on,
  control,
  comparisons,
  output_dir='.',
  qvalue.threshold=0.05
){
    # read input files
    cts <- read.table(input_counts, sep='\t', header=TRUE, row.names = 1)
    coldata <- read.table(sample_info_path, sep='\t', header=TRUE, row.names = 1)
    cts <- round(cts)
    
    # subset of the samples for which we have RNAseq and metadata
    samples <- intersect(rownames(coldata), colnames(cts))
    cts <- cts[samples]
    cts.rownames <- rownames(cts)
    cts <- as.data.frame(cts)
    rownames(cts) <- cts.rownames
    coldata <- coldata[samples,]
    
    # Set up DE variable.
    classes <- as.character(coldata[[on]])
    coldata$group <- as.factor(classes)
    for (x in control){
        coldata[[x]] <- as.factor(coldata[[x]])
    }
    design <- as.formula(paste('~ 0', 'group',control, sep=' + '))
    
    message(paste("Number of genes:",dim(cts)[[1]]))
    message(paste("Number of samples:",dim(cts)[[2]]))

    ## DESeq2
    dds <- DESeqDataSetFromMatrix(countData = cts,
                              colData = coldata,
                              design = design)
    keep <- rowSums(counts(dds)) >= 10
    dds <- dds[keep,]
    
    # DE analysis
    message('Fitting GLM...')
    reduced<-as.formula(paste('~ 0',control,sep=' + '))
    dds <- DESeq(dds, test='LRT', reduced=reduced, parallel=TRUE)
    summary(dds)
    for (comp in comparisons){
        name = paste0(comp[1],'_vs_',comp[2])
        message('performing LRT test for ',name)
        
        # Generate each contrast using make_contrast
        levels <- resultsNames(dds)
        #cc <- comparison_as_vectors(comp)
        contrast <- make_contrast(as.character(comp[1]),as.character(comp[2]),levels)
        res <- results(dds,contrast=contrast,name=name, alpha = qvalue.threshold, parallel = TRUE)
        res <- res[order(res$pvalue),]
        summary(res)
        
        ## Write
        # Make directory
        dir <- file.path(output_dir,'DESeq2')
        dir.create(dir, showWarnings = FALSE)
        
        write.table(as.data.frame(res), file = file.path(dir,paste0(name,'.txt')),quote=FALSE)
    }
    return(dds)
}

# prepends 'group' to every element of a vector if it doesnt already have it.
make_contrasts_helper2 <- function(str_vector){
    if (! startsWith(str_vector[1],'group')){
        str_vector = paste0('group',str_vector)
    }
    return(str_vector)
}

# Converts eg 'G3a_G4' into '(groupG3a+groupG4)/4'
make_contrasts_helper <- function(ingroup,outgroup,levels){
    if (ingroup[1] == 'grouprest'){
        ingroup = levels[!(levels %in% outgroup)]
    }
    n = length(ingroup)
    contrast = paste(ingroup,collapse='+')
    contrast=paste0('(',contrast,')/',n)
    return(contrast)
}

make_contrast <- function(c1, c2, levels){
    c1 = make_contrasts_helper2(c1)
    c2 = make_contrasts_helper2(c2)
    levels = make_contrasts_helper2(levels)
    con1 = make_contrasts_helper(c1,c2,levels)
    con2 = make_contrasts_helper(c2,c1,levels)
    contrast = paste0(con1,'-',con2)
    n1 = paste(c1,collapse='_')
    n2 = paste(c2,collapse='_')
    name = paste0(n1,'_vs_',n2)
    return (limma::makeContrasts(contrasts=contrast,levels=levels))
}