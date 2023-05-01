#Libs
library(reshape2)
library(stringr)
library(ggplot2)

#Reference: https://www.r-bloggers.com/2016/03/computing-classification-evaluation-metrics-in-r/

#func
calcMetrics <- function(filename, feat, degrade) {
  #Load data
  df <- read.csv(filename, sep="\t", header = FALSE)
  df$clade <- str_split_fixed(df$V1,"\\|",4)[,3]
  table <- dcast(df, clade ~ V2, fun.aggregate = length, value.var = "clade")
  rownames(table) <- table$clade
  table$clade <- NULL
  
  #Check name diffs
  missingName <- setdiff(rownames(table),colnames(table))
  if (typeof(missingName) == "character") {
    table[missingName] <- 0
    table <- table[ , order(names(table))]
  }
  
  #Precalcs
  n = sum(table) # number of instances
  nc = nrow(table) # number of classes
  diag = diag(as.matrix(table)) # number of correctly classified instances per class 
  rowsums = apply(table, 1, sum) # number of instances per class
  colsums = apply(table, 2, sum) # number of predictions per class
  
  if(colnames(table)[length(colnames(table))] == "unknown") {
    colsums = colsums[1:length(colsums) -1]
  }
  
  p = rowsums / n # distribution of instances over the actual classes
  q = colsums / n # distribution of instances over the predicted classes
  
  #raw accuracy
  accuracy = sum(diag) / n 
  accuracy 
  
  #Per class P-R-F
  precision = diag / colsums 
  recall = diag / rowsums 
  #Replace NaN w/ zero
  precision[is.nan(precision)] <- 0
  recall[is.nan(recall)] <- 0
  f1 = 2 * precision * recall / (precision + recall) 
  f1[is.nan(f1)] <- 0
  data.frame(precision, recall, f1) 
  
  #Macro calcs
  macroPrecision = mean(precision)
  macroRecall = mean(recall)
  macroF1 = mean(f1)
  return(data.frame(accuracy,macroPrecision, macroRecall, macroF1, feat, degrade))
}

#degrade 0
scoreDf <- calcMetrics("p0.5_0.csv",0.5,0)
scoreDf <- rbind(scoreDf, calcMetrics("p1_0.csv",1,0))
scoreDf <- rbind(scoreDf, calcMetrics("p5_0.csv",5,0))
scoreDf <- rbind(scoreDf, calcMetrics("p10_0.csv",10,0))
scoreDf <- rbind(scoreDf, calcMetrics("p20_0.csv",20,0))
scoreDf <- rbind(scoreDf, calcMetrics("p100_0.csv",100,0))

#degrade 10
scoreDf <- rbind(scoreDf, calcMetrics("p0.5_10.csv",0.5,10))
scoreDf <- rbind(scoreDf, calcMetrics("p1_10.csv",1,10))
scoreDf <- rbind(scoreDf, calcMetrics("p5_10.csv",5,10))
scoreDf <- rbind(scoreDf, calcMetrics("p10_10.csv",10,10))
scoreDf <- rbind(scoreDf, calcMetrics("p20_10.csv",20,10))
scoreDf <- rbind(scoreDf, calcMetrics("p100_10.csv",100,10))

#degrade 20
scoreDf <- rbind(scoreDf, calcMetrics("p0.5_20.csv",0.5,20))
scoreDf <- rbind(scoreDf, calcMetrics("p1_20.csv",1,20))
scoreDf <- rbind(scoreDf, calcMetrics("p5_20.csv",5,20))
scoreDf <- rbind(scoreDf, calcMetrics("p10_20.csv",10,20))
scoreDf <- rbind(scoreDf, calcMetrics("p20_20.csv",20,20))
scoreDf <- rbind(scoreDf, calcMetrics("p100_20.csv",100,20))

#degrade 30
scoreDf <- rbind(scoreDf, calcMetrics("p0.5_30.csv",0.5,30))
scoreDf <- rbind(scoreDf, calcMetrics("p1_30.csv",1,30))
scoreDf <- rbind(scoreDf, calcMetrics("p5_30.csv",5,30))
scoreDf <- rbind(scoreDf, calcMetrics("p10_30.csv",10,30))
scoreDf <- rbind(scoreDf, calcMetrics("p20_30.csv",20,30))
scoreDf <- rbind(scoreDf, calcMetrics("p100_30.csv",100,30))

#degrade 40
scoreDf <- rbind(scoreDf, calcMetrics("p0.5_40.csv",0.5,40))
scoreDf <- rbind(scoreDf, calcMetrics("p1_40.csv",1,40))
scoreDf <- rbind(scoreDf, calcMetrics("p5_40.csv",5,40))
scoreDf <- rbind(scoreDf, calcMetrics("p10_40.csv",10,40))
scoreDf <- rbind(scoreDf, calcMetrics("p20_40.csv",20,40))
scoreDf <- rbind(scoreDf, calcMetrics("p100_40.csv",100,40))


#Melt for plotting
meltDf <- melt(scoreDf, id = c("feat","degrade"))

#Test
ggplot(meltDf, aes(degrade, as.factor(feat), fill=value)) + 
  geom_tile(color="white") +
  coord_fixed(10) +
  geom_text(aes(label = round(value, 2))) +
  scale_fill_gradient2(midpoint = 0.7, low = "#648FFF", mid = "#DC267F", high = "#FFFF00") +
  theme_minimal() +
  labs(fill="Value", x="Sequence Degredation %", y="% Features") +
  facet_wrap(~ variable, nrow = 2) +
  theme(
    strip.text.x = element_text(size = 18),
    axis.text = element_text(size = 12),
    axis.title = element_text(size = 18)
  )





#ACCURACY (geom_raster(interpolate=TRUE))
ggplot(scoreDf, aes(degrade, as.factor(feat), fill=accuracy)) + 
  geom_tile() +
  coord_fixed(10) +
  geom_text(aes(label = round(accuracy, 2))) +
  scale_fill_gradient2(midpoint = 0.75, low = "#648FFF", mid = "#DC267F", high = "#FFFF00") +
  theme_minimal()

ggplot(scoreDf, aes(degrade, as.factor(feat), fill=macroPrecision)) + 
  geom_tile() +
  geom_text(aes(label = round(accuracy, 2))) +
  scale_fill_gradient2(midpoint = 0.75, low = "#648FFF", mid = "#DC267F", high = "#FFFF00") +
  theme_minimal()

ggplot(scoreDf, aes(degrade, as.factor(feat), fill=macroRecall)) + 
  geom_tile() +
  geom_text(aes(label = round(accuracy, 2))) +
  scale_fill_gradient2(midpoint = 0.75, low = "#648FFF", mid = "#DC267F", high = "#FFFF00") +
  theme_minimal()

ggplot(scoreDf, aes(degrade, as.factor(feat), fill=macroF1)) + 
  geom_tile() +
  geom_text(aes(label = round(accuracy, 2))) +
  scale_fill_gradient2(midpoint = 0.75, low = "#648FFF", mid = "#DC267F", high = "#FFFF00") +
  theme_minimal()

