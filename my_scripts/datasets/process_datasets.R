 # define Class attribute in all dataset 
rm(list=ls())
setwd("backup")
files_list = list.files(pattern="*.csv")
files_list
#files = lapply(files_list, function(x) read.csv(x, header = FALSE, sep=",", stringsAsFactors=FALSE))
#files
files = as.data.frame(read.csv(files_list[[15]], header = FALSE, sep=","))
files_factor <- as.data.frame(lapply(files, factor))
num_files_factor <- lapply(files_factor, nlevels)
class_idx <-ncol(files)
nlevels(files_factor[, class_idx ])
names(files)[1] <- "Class"
setwd("..")
write.csv(files, file = files_list[[15]], row.names = FALSE)
