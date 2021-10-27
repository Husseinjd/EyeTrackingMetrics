########## PSYC 607 -- Homework #2 ##########

##### Preparation for Homework #2 #####
# Download PSYC607-Homework2.R script and rename it "FirstName-LastName-Homework2.R"
# Download bmi2.csv file
# Save both files in a folder you can access via R Studio

##### Instructions for Homework #2 #####
# Below each instruction, type your code and run it to make sure it works
# Where you see "RESPONSE:" simply type your response afterwards
# Make sure to save your script regularly
# Once you have finished, upload your R script to Canvas

# Question 1 - 4 points #

# Q1A: Set your working directory to where the bmi2.csv file is saved
setwd("/Downloads")

# Q1B: Load the bmi2.csv file as data frame named bmi2
bmi2 <- read.csv("bmi2.csv", header=TRUE)

# Q1C: Run a summary of the bmi2.csv file
summary(bmi2)

# Q1D: Run a summary of the bmi variable in the bmi2 data frame
summary(bmi2$bmi)

# Question 2 - 4 points #

# Q2A: Run a frequency table of the variable gender in bmi2
# and add the label "gender" to the table
# Then, save the table in a data frame with the name GenderFreq
GenderFreq<-as.data.frame(table(bmi2$gender, dnn='gender'))

# Q2B: Using the frequencies from the GenderFreq table above, 
# calculate a proportion table 
# and save it to the global environment as GenderProp
GenderProp<-prop.table(GenderFreq$Freq)
GenderProp

# Q2C: Using the proportion table above, 
# calculate a percentage table 
# and save it to the global environment as GenderPerc
GenderPerc<-GenderProp*100

# Q2D: Combine the frequency table, proportion table, and 
# percentage table (all from above) into a data frame 
# named GenderTab
# then make R print the data frame into the console
GenderTab<-cbind.data.frame(GenderFreq, proportion=GenderProp, percentage=GenderPerc)
GenderTab

# Question 3 - 4 points #

# Q3A: Run a frequency table of the variable height in bmi2 
# and add the label "height" to the table
# Then, sort the table (in decreasing order) 
# Then, save the table in a data frame with the name HeightFreq
HeightFreq<-as.data.frame(sort(table(bmi2$height, dnn='height'), decreasing=TRUE))

# Q3B: Using the frequencies from the HeightFreq table above, 
# calculate a proportion table (rounded to 3 decimal points)
# and save it to the global environment as HeightProp
HeightProp<-round(prop.table(HeightFreq$Freq),3)

# Q3C: Using the proportion table above, 
# calculate a percentage table 
# and save it to the global environment as HeightPerc
HeightPerc<-HeightProp*100

# Q3D: Combine the frequency table, proportion table, and 
# percentage table (all from above) into a data frame 
# named HeightTab
# then make R print the data frame into the console
HeightTab<-cbind.data.frame(HeightFreq, proportion=HeightProp, percentage=HeightPerc)
HeightTab

# Question 4 - 8 points total (2 points each) #

# Q4A: Calculate the mean of weight and save it in a variable
# named WeightMean
# then make R print the data frame into the console
WeightMean <- mean(bmi2$weight, na.rm=TRUE)
WeightMean

# Q4B: Calculate the median of weight and save it in a variable
# named WeightMedian
# then make R print the data frame into the console
WeightMedian<-median(bmi2$weight, na.rm=TRUE)
WeightMedian

# Q4C: Using the mean of weight, 
# calculate the deviations from the mean for each individual
# make R add the deviations to the bmi2 dataset 
# as a variable called WeightDev
# then view the updated bmi2 dataset
bmi2$WeightDev<-bmi2$weight-WeightMean
View(bmi2)

# Q4D: Using the median of weight, 
# calculate the squared deviations from the median for each individual
# make R add the squared deviations (rounded to 2 decimals)
# to the bmi2 dataset as a variable called WeightDevSq
# then view the updated bmi2 dataset
bmi2$WeightDevSq <- round(((bmi2$weight-WeightMedian)^2), 2)
View(bmi2)

# Question 5 - 10 points total (2 points each) #

# Q5A: Into GenderTab from Q2B, create a variable named
# PieLabel composed of the following put together:
# gender variable and in parentheses the percentage and "%"
GenderTab$PieLabel <- paste(GenderTab$gender, " (", GenderTab$percentage, "%)", sep="")
GenderTab

# Q5B: Create a pie chart based on the gender frequencies, 
# and use the PieLabel from above for the labels
pie(GenderTab$Freq, labels=GenderTab$PieLabel)


# Q5C: Add to the pie chart above three custom colors:
# nonbinary => pick your favorite green
# female => pick your favorite grey
# male => pick your favorite yellow
pie(GenderTab$Freq, labels=GenderTab$PieLabel, col=c("gray67", "yellow2", "green3"), main="Gender Pie Chart")

# Q5D: Before you make a 3D pie chart,
# you need to load the library required to make a 3D pie chart
library(plotrix)

# Q5E: Now turn the pie chart above in Q5C
# into a 3D pie chart with a title "Gender Pie Chart"
# Note: keep the colors and labels from Q5C
pie3D(GenderTab$Freq, labels=GenderTab$PieLabel, col=c("gray67", "yellow2", "green3"), main="Gender Pie Chart")

# Question 6 - 10 points total (2 points each) #

# Q6A: Using GenderTab again, create a basic bar chart
# using the gender variable for the x-axis
barplot(GenderTab$Freq)

# Q6B: Building on the bar plot from above,
# add a main title "Gender Bar Chart",
# add an x-axis label "Gender", 
# and add a y-axis label "Frequency (n)"
barplot(GenderTab$Freq, main="Gender Bar Chart", xlab="Gender", ylab="Frequency (n)", names.arg=c("Female", "Male","Non-binary"))

# Q6C: Load the ggplot library
# Create a ggplot called GenderBar
# using the GenderTab, with gender on the x-axis,
# frequency on the y-axis, and gender as the color
# Note: the graph should be blank
library(ggplot2)
GenderBar <- ggplot(data=GenderTab, aes(x=gender, y=Freq, color=gender))

# Q6D: STRETCH -- Building on the bar plot from above,
# add a geom_bar() using an identity as the statistic,
# set the color of the outlines to black and set the fill as:
# nonbinary => pick your favorite green
# female => pick your favorite grey
# male => pick your favorite yellow
GenderBar <- ggplot(data=GenderTab, aes(x=gender, y=Freq, fill=gender))+
	geom_bar(stat="identity", width=0.6, colour="black")+
	scale_fill_manual(values = c("gray67", "yellow2", "green3"))

# Q6E: Again, building on the bar plot from above,
# add a title "Frequency Bar Chart",
# add an x-axis "Gender", and
# add a y-axis "Frequency (n)"
GenderBar <- ggplot(data=GenderTab, aes(x=gender, y=Freq, fill=gender))+
	geom_bar(stat="identity", width=0.6, colour="black")+
	scale_fill_manual(values = c("gray67", "yellow2", "green3"))+
	labs(title="Frequency Bar Chart", 
       x="Gender", y="Frequency (n)")

# Question 7 - 10 points total (2 points each) #

# Q7A: Create a basic histogram of the bmi variable
# from the bmi2 data table
bmiHist <- ggplot(data=bmi2, aes(x=bmi))+ 
  geom_histogram(position="identity", 
                 alpha=0.8, col="white")

# Q7B: To the histogram above,
# add a title "Histogram of BMI",
# add an x-axis of "BMI", and
# add a y-axis of "Frequency (n)"
bmiHist <- ggplot(data=bmi2, aes(x=bmi))+ 
  geom_histogram(position="identity", 
                 alpha=0.8, col="white")+
  labs(title="Histogram of BMI", 
       x="BMI", y="Frequency (n)")

# Q7C: Create a ggplot called GenderHist
# with BMI on the x-axis,
# and using the identity position within geom_histogram
genderHist <- ggplot(data=bmi2, aes(x=bmi))+ 
  geom_histogram(position="identity")

# Q7D: Building off the histogram above, 
# add a classic theme and a binwidth of 2.5
genderHist <- ggplot(data=bmi2, aes(x=bmi))+ 
  geom_histogram(position="identity", binwidth=2.5)+
  theme_classic()

# Q7E: Building off the histogram above, 
# add a title, x-axis label, and y-axis label (your choice of wording)
genderHist <- ggplot(data=bmi2, aes(x=bmi))+ 
  geom_histogram(position="identity", binwidth=2.5)+
  theme_classic()+
  labs(title="BMI distribution", 
       x="BMI", y="n")

# Question 8 - 10 points total (2 points each) #

# Q8A: Using bmi in the bmi2 dataset,
# create a ggplot called BMIbox
# with BMI on the y-axis and with the x-axis blank
# NOTE: the graph should be blank
BMIbox<- ggplot(data=bmi2, aes(x = "", y=bmi))

# Q8B: Building off of the previous plot,
# add a geom_boxplot without notches and a width of .4
BMIbox<- ggplot(data=bmi2, aes(x = "", y=bmi))+
	geom_boxplot(notch = FALSE, width=.4)

# Q8C: Building off of the previous plot,
# add a main title and a y-axis label, 
# but make the x-axis label blank
BMIbox<- ggplot(data=bmi2, aes(x = "", y=bmi))+
	geom_boxplot(notch = FALSE, width=.4)+
	labs(title="BMI boxplot",x = "", y = "BMI")

# Q8D: Building off of the previous plot,
# add jitter of size 1, alpha .1, width of .2, and color blue
BMIbox<- ggplot(data=bmi2, aes(x = "", y=bmi))+
	geom_boxplot(notch = FALSE, width=.4)+
	labs(title="BMI boxplot",x = "", y = "BMI")+
	geom_jitter(size = 1, alpha = 0.1, width = 0.2) 

# Q8E: Building off of the previous plot,
# make the plot title size 20,
# make the axis text size 14, 
# and make the axis title size 18
BMIbox<- ggplot(data=bmi2, aes(x = "", y=bmi))+
	geom_boxplot(notch = FALSE, width=.4)+
	labs(title="BMI boxplot",x = "", y = "BMI")+
	geom_jitter(size = 1, alpha = 0.1, width = 0.2)+
	theme(axis.title = element_text(size = 20), 
        axis.text = element_text(size = 14),
        plot.title = element_text(size=18))