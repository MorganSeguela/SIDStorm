##=============================================================
## Package
##=============================================================

library(dplyr)

##=============================================================

##=============================================================

vfiles <- list.files("data_meteo", "train", full.names = TRUE)

clean_file <- function(file){
    trainDf <- read.csv2(
        file,
        sep = ";",
        dec = ",",
        stringsAsFactors = FALSE
    )
    trainDf$insee <- formatC(trainDf$insee, width = 8, flag = "0")
    trainDf$ech <- formatC(trainDf$ech, width = 2, flag = "0")
    
    trainDf$ddH10_rose4 <- as.factor(as.numeric(trainDf$ddH10_rose4))
    trainDf$flvis1SOL0 <- as.numeric(trainDf$flvis1SOL0)
    
    w1 <- which(grepl("[0-9]+/[0-9]+/[0-9]+", trainDf$date))
    if(length(w1)){
        split_ls <- strsplit(trainDf$date[w1], "/")
        trainDf$date[w1] <- sapply(split_ls, function(x){
            paste(x[3], x[2], x[1], sep = "-")
        })
    }
    return(trainDf)
}

##=============================================================

##=============================================================
dfTrain <- dplyr::bind_rows(lapply(vfiles, clean_file))

w1 <- which(grepl("[0-9]+/[0-9]+/[0-9]+", dfTrain$date))
w2 <- which(grepl("[0-9]+-[0-9]+-[0-9]+", dfTrain$date))


datals_insee <- split.data.frame(dfTrain, dfTrain$insee)
for(insee in names(datals_insee)){
    iDf <- datals_insee[[insee]]
    iDf$insee <- as.numeric(iDf$insee)
    iDf$ech <- as.numeric(iDf$ech)
    prefix <- substr(insee, 1, 2)
    write.csv2(iDf, paste0("data_cleaned/data_train_", insee, ".csv"),
               row.names = FALSE,
               na = "")
}

datals_ech <- split.data.frame(dfTrain, dfTrain$ech)
for(ech in names(datals_ech)){
    iDf <- datals_ech[[ech]]
    iDf$insee <- as.numeric(iDf$insee)
    iDf$ech <- as.numeric(iDf$ech)
    prefix <- substr(insee, 1, 2)
    write.csv2(iDf,
               paste0("data_cleaned/data_train_ech_", ech, ".csv"),
               row.names = FALSE,
               na = "")
}

##=============================================================

##=============================================================

dfTest <- read.csv2(
    "data_meteo/test.csv",
    sep = ";",
    dec = ",",
    stringsAsFactors = FALSE
) %>%
    dplyr::mutate(
        ddH10_rose4 = as.factor(as.numeric(ddH10_rose4)),
        flvis1SOL0 = as.numeric(gsub(",", ".", flvis1SOL0))
    )

w1 <- which(grepl("[0-9]+/[0-9]+/[0-9]+", dfTest$date))
if(length(w1)){
    split_ls <- strsplit(dfTest$date[w1], "/")
    dfTest$date[w1] <- sapply(split_ls, function(x){
        paste(x[3], x[2], x[1], sep = "-")
    })
}

write.csv2(dfTest,
           paste0("data_cleaned/data_test.csv"),
           row.names = FALSE,
           na = "")




