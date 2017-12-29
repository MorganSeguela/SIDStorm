
library(dplyr)
library(tidyr)
library(tibble)
library(ggplot2)


rm(list = ls())
load("rdata/train.RData")
load("rdata/test.RData")

source("functions/multiplot.R")

data_train$file <- "train"
data_test$file <- "test"
data_train <- dplyr::bind_rows(data_train, data_test) %>%
    dplyr::mutate(file = factor(file, levels = c("train", "test")))


dfTrain_gth <- data_train %>%
    dplyr::select(-mois) %>%
    tidyr::gather(
        "features", "values",
        -c(file, date, insee, ech, tH2_obs, dtH2, ddH10_rose4)
    ) %>%
    dplyr::mutate(features = as.factor(features))

## List Density
list_density <- list()
box_density <- list()
scatter_ls <- list()
## Boucle
for(i in levels(dfTrain_gth$features)){
    ## filtte
    iDf <- dfTrain_gth %>%
        dplyr::filter(features == i)
    
    ## dtH2
    scatter_ls[[i]] <- ggplot(data = iDf) +
        facet_grid(~insee) +
        geom_point(
            mapping = aes(values, tH2_obs, col = insee),
            alpha = 0.5,
            na.rm = TRUE
        ) +
        guides(col = FALSE) +
        xlab(i) +
        ggtitle(i)
    
    ## plot density
    list_density[[i]] <- ggplot(data = iDf) +
        facet_grid(file~insee) +
        geom_density(
            mapping = aes(values, fill = insee),
            alpha = 0.5,
            na.rm = TRUE
        ) +
        ggtitle(i)
    ## boxplot
    box_density[[i]] <- ggplot(data = iDf) +
        facet_wrap(~file) +
        geom_boxplot(
            mapping = aes(insee, values, fill = insee),
            alpha = 0.5,
            na.rm = TRUE
        ) +
        ggtitle(i)
}


for(ilvl in levels(dfTrain_gth$features)){
    print(ilvl)
    png(paste('pictures/', ilvl, '.png'), width = 800, height = 650)
    multiplot(
        scatter_ls[[i]],
        list_density[[ilvl]],
        box_density[[ilvl]],
        ncol = 1,
        mainTitle = ilvl
    )
    dev.off()
}



ggplot(data = data_train) +
    geom_histogram(
        mapping = aes(x = iwcSOL0, y = ..density.., fill = insee),
        bins = 10,
        na.rm = TRUE
    ) +
    facet_wrap(~insee)


## Plot Density
plot_density <- ggplot(data = dfTrain_gth) +
    geom_density(
        mapping = aes(values, fill = insee),
        alpha = 0.5,
        na.rm = TRUE
    ) +
        facet_wrap(~features, scales = "free") +
        ggtitle(i)

plot_density


## Plot Density
plot_density_dtH2 <- ggplot(data = data_train) +
    geom_density(
        mapping = aes(dtH2, fill = insee),
        alpha = 0.5,
        na.rm = TRUE
    ) +
    ggtitle("dtH2")
plot_density_dtH2


plot_density_tH2obs <- ggplot(data = data_train) +
    geom_density(
        mapping = aes(tH2_obs, fill = insee),
        alpha = 0.5,
        na.rm = TRUE
    ) +
    ggtitle("tH2_obs")

plot_density_tH2obs






shaptest <- with(data_train, {
    tapply(tH2_obs, list(insee, ech), function(x){
        shapiro.test(x)$p.value
    })
})


list_aov <- sapply(levels(dfTrain_gth$features)[1:10], function(feat){
    print(feat)
    iDf <- dfTrain_gth %>%
        dplyr::filter(features == feat)
    iLm <- lm(tH2_obs ~ values + insee + ech, data = iDf)
    iAov <- aov(tH2_obs ~ values + insee + ech, data = iDf)
    iSumma <- summary(iLm)
    pval <- iSumma$coefficients[2, 4]
    return(iAov)
})

aov_ls <- list()
for(feat in levels(dfTrain_gth$features)){
    iFormula <- paste("tH2_obs ~", feat, "* insee")
    iAov <- aov(as.formula(iFormula), data = data_train)
    aov_ls[[feat]] <- summary(iAov)
    print(summary(iAov))
}



dfTH2 <- data_train %>%
    dplyr::select(insee, contains('tH2_'), -tH2_obs) %>%
    tidyr::gather("features", "values", -insee) %>%
    dplyr::mutate(features = as.factor(features))

list_tH2 <- list()
for(i in levels(dfTH2$features)){
    iDf <- dfTH2 %>% dplyr::filter(features == i)
    list_tH2[[i]] <- ggplot(data = iDf) +
        facet_wrap(~insee) +
        geom_density(
            mapping = aes(values, fill = insee),
            alpha = 0.5,
            na.rm = TRUE
        ) +
        ggtitle(i)
}







