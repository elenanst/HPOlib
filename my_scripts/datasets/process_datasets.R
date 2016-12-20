 # define Class attribute in all dataset 
rm(list=ls())
setwd("/home/elena/R_ws/automl/ADS_workspace/datasets_repo/configured")
files_list = list.files(pattern="*.csv")
files_list
#files = lapply(files_list, function(x) read.csv(x, header = FALSE, sep=",", stringsAsFactors=FALSE))
#files
files = as.data.frame(read.csv(files_list[[45]], header = TRUE, sep=",", stringsAsFactors=FALSE))
files<- as.data.frame(lapply(files, function(x) as.numeric(gsub("?",NA,x, fixed = TRUE))))
files[files == "*"] <-0
files_factor <- as.data.frame(lapply(files, factor))
num_files_factor <- lapply(files_factor, nlevels)
class_idx <-ncol(files)
nlevels(files_factor[, class_idx ])
names(files)[1] <- "Class"
write.csv(files, file = files_list[[1]], row.names = FALSE)
