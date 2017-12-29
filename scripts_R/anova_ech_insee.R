
rm(list = ls())
load("rdata/train.RData")

data_train$ech

isnum <- sapply(data_train, is.numeric)

varnum <- names(which(isnum))

for(i in varnum){
    print(i)
    ianova <- aov(as.formula(paste(i, "~ ech * insee" )), data = data_train)
    print(summary(ianova))
    print("\n")
}