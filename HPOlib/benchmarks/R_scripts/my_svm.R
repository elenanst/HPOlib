rm(list=ls())
# Training an SVM RBF model 
library(caret)
library(dplyr)         # Used by caret
library(kernlab)       # support vector machine 
options(warn=-1)
set.seed(15)

sink("my_svm.R")
# load data
myArgs <- commandArgs(trailingOnly = TRUE)
#myArgs <- c(2000 ,5, '/home/elena/R_ws/automl/ADS_workspace/datasets_repo/test/ad.csv')
dataset_position <- lapply(myArgs, function(x)  grepl('datasets_repo', x))
dataset_position <- which(unlist(dataset_position))
dataset_path <- myArgs[dataset_position]
dataset <- read.csv(dataset_path,
                    header = TRUE, sep=",", stringsAsFactors=FALSE)

#remove instances with nas
dataset <- dataset[complete.cases(dataset),]
if ("date" %in% names(dataset) )
 {
   dataset$date <- as.Date(dataset$date)
}
#variables <- names(dataset[sapply(dataset,class) == "character"])

#dataset[, (names(dataset) %in% variables)]<- lapply(dataset[, (names(dataset) %in% variables)], as.factor)

#pick class as first two-level categorical attribute(remember, we are dealing with binary classifi
#cation problems)
dataset$Class <- factor(dataset$Class)
trainIndex <- createDataPartition(dataset$Class, p=.8, list=FALSE)
trainData <- dataset[trainIndex,]
testData  <- dataset[-trainIndex,]
testClass <- testData[, "Class"]
testData$Class <- NULL


# train with specified arguments
optParameters <- expand.grid( C = c(as.numeric(myArgs[1])) ,
                              sigma = c(as.numeric(myArgs[2]))
)

# train model
result = tryCatch( {
  trained_model <- train(Class ~ ., data = trainData,
                         method = "svmRadial", # SVM with RBF
                         tuneGrid = optParameters,
                         preProcess=c("center","scale"),
                         trControl=trainControl(method="none")
  )
  
  # calculate error(as 1-accuracy)
  predictions <- predict(trained_model, testData)
  cm <- confusionMatrix(predictions, testClass)
  accuracy <- as.numeric(cm$overall['Accuracy'])
  error_metric <- 1-accuracy
  error_metric
  },error = function(err) {
  1 
}
)
sink()

cat(result)



