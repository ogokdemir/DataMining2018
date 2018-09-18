library(tidyverse)
library(dplyr)
library(readr)

data <- read_csv("C:\\Users\\Ozan Gokdemir\\Desktop\\movies.csv")
attach(data)
sorted <- data[order(user_id),]

