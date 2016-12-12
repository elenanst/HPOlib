rm(list=ls())
# Training an SVM RBF model 
library(caret)
library(dplyr)         # Used by caret
library(kernlab)       # support vector machine 

set.seed(15)

# load data
#myArgs <- commandArgs(trailingOnly = TRUE)
myArgs <- c(10,44, '/home/elena/R_ws/automl/ADS_workspace/datasets_repo/student/student-mat.csv')
dataset_position <- lapply(myArgs, function(x)  grepl('datasets_repo', x))
dataset_position <- which(unlist(dataset_position))
dataset_path <- myArgs[dataset_position]
dataset <- read.csv(dataset_path,
                         header = TRUE, sep=";", stringsAsFactors=FALSE)

#pick class as first two-level categorical attribute(remember, we are dealing with binary classifi
#cation problems)
variables <- names(dataset[sapply(dataset,class) == "character"])
dataset[, (names(dataset) %in% variables)] <- lapply(dataset[, (names(dataset) %in% variables)], as.factor)
binary_categorical <- sapply(dataset, function(x) nlevels(x) == 2)
positions <- which(binary_categorical)
dataset$Class <- dataset[, positions[1]]
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
trained_model <- train(Class ~ ., data = trainData,
                       method = "svmRadial", # SVM with RBF
                       tuneGrid = optParameters,
                       trControl=trainControl(method="none")
)

# calculate error(as 1-accuracy)
predictions <- predict(trained_model, testData)
cm <- confusionMatrix(predictions, testClass)
accuracy <- as.numeric(cm$overall['Accuracy'])
error_metric <- 1-accuracy
cat(error_metric)



