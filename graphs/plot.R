library("ggplot2")
library("reshape2")

gaze <- read.csv("gazedata.csv", header=TRUE)
gaze
summary(gaze)
gaze<-t(gaze) # transpose the dataset

SGE<-data.frame(gaze[0:20,])
GTE<-data.frame(gaze[21:40,])

SGE$trialtype <- gl(2, 10, labels = c("normal", "attack"))
GTE$trialtype <- gl(2, 10, labels = c("normal", "attack"))

SGEmelt<-melt(SGE)
GTEmelt<-melt(GTE)

require(ggplot2)
jpeg("sge.jpg", width = 1920, height = 1080)
box<- ggplot(data=SGEmelt, aes(x=variable, y=value))+
	geom_boxplot(notch = FALSE, width=.4, aes(fill=trialtype))+
	labs(title="Gaze entropy",x = "Participants", y = "SGE")+
	geom_jitter(size = 1, alpha = 0.1, width = 0.2)+
	theme(axis.title = element_text(size = 32), 
        axis.text = element_text(size = 26),
        plot.title = element_text(size=32),
        legend.key.size = unit(3, 'cm'), #change legend key size
        legend.title = element_text(size=26), #change legend title font size
        legend.text = element_text(size=26)) #change legend text font size
box
dev.off() 

require(ggplot2)
jpeg("gte.jpg", width = 1920, height = 1080)
box<- ggplot(data=GTEmelt, aes(x=variable, y=value))+
	geom_boxplot(notch = FALSE, width=.4, aes(fill=trialtype))+
	labs(title="Gaze entropy",x = "Participants", y = "GTE")+
	geom_jitter(size = 1, alpha = 0.1, width = 0.2)+
	theme(axis.title = element_text(size = 32), 
        axis.text = element_text(size = 26),
        plot.title = element_text(size=32),
        legend.key.size = unit(3, 'cm'), #change legend key size
        legend.title = element_text(size=26), #change legend title font size
        legend.text = element_text(size=26)) #change legend text font size
box
dev.off() 

require(ggplot2)
jpeg("gte_avg.jpg", width = 1920, height = 1080)
box<- ggplot(data=GTEmelt, aes(x=trialtype, y=value))+
	geom_boxplot(notch = FALSE, width=.4)+
	labs(title="Gaze entropy",x = "Trials", y = "GTE")+
	geom_jitter(size = 1, alpha = 0.1, width = 0.2)+
	theme(axis.title = element_text(size = 32), 
        axis.text = element_text(size = 26),
        plot.title = element_text(size=32),
        legend.key.size = unit(3, 'cm'), #change legend key size
        legend.title = element_text(size=26), #change legend title font size
        legend.text = element_text(size=26)) #change legend text font size
box
dev.off() 

require(ggplot2)
jpeg("sge_avg.jpg", width = 1920, height = 1080)
box<- ggplot(data=SGEmelt, aes(x=trialtype, y=value))+
	geom_boxplot(notch = FALSE, width=.4)+
	labs(title="Gaze entropy",x = "Trials", y = "SGE")+
	geom_jitter(size = 1, alpha = 0.1, width = 0.2)+
	theme(axis.title = element_text(size = 32), 
        axis.text = element_text(size = 26),
        plot.title = element_text(size=32),
        legend.key.size = unit(3, 'cm'), #change legend key size
        legend.title = element_text(size=26), #change legend title font size
        legend.text = element_text(size=26)) #change legend text font size
box
dev.off() 



sge_normal <- subset(SGEmelt,  trialtype == "normal", value, drop=TRUE)
sge_attack <- subset(SGEmelt,  trialtype == "attack", value, drop=TRUE)


res <- t.test(sge_normal, sge_attack, paired = TRUE, alternative = "less")
res

# 	Paired t-test

# data:  sge_normal and sge_attack
# t = -3.9758, df = 119, p-value = 6.04e-05
# alternative hypothesis: true difference in means is less than 0
# 95 percent confidence interval:
#         -Inf -0.06105376
# sample estimates:
# mean of the differences 
#              -0.1047167 

gte_normal <- subset(GTEmelt,  trialtype == "normal", value, drop=TRUE)
gte_attack <- subset(GTEmelt,  trialtype == "attack", value, drop=TRUE)

res <- t.test(gte_normal, gte_attack, paired = TRUE, alternative = "greater")

# 	Paired t-test

# data:  gte_normal and gte_attack
# t = 3.0023, df = 119, p-value = 0.001633
# alternative hypothesis: true difference in means is greater than 0
# 95 percent confidence interval:
#  0.005623989         Inf
# sample estimates:
# mean of the differences 
#              0.01255833 


SGE$trialnumber <- 1:20

library("tidyverse")
df <- SGE %>%
  select(trialnumber, X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, X11, X12) %>%
  gather(key = "variable", value = "value", -trialnumber)
head(df)

jpeg("sge_trialwise.jpg", width = 1920, height = 1080)
# Visualization
ggplot(df, aes(x = trialnumber, y = value)) + 
  geom_line(aes(color = variable, linetype = variable)) +
  #  + scale_color_manual(values = c("darkred", "steelblue"))
  labs(title="Gaze entropy vs Trials",x = "Trials", y = "SGE") +
  theme(axis.title = element_text(size = 32), 
        axis.text = element_text(size = 26),
        plot.title = element_text(size=32),
        legend.key.size = unit(3, 'cm'), #change legend key size
        legend.title = element_text(size=26), #change legend title font size
        legend.text = element_text(size=26)) #change legend text font size
dev.off()


GTE$trialnumber <- 1:20

dfgte <- GTE %>%
  select(trialnumber, X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, X11, X12) %>%
  gather(key = "variable", value = "value", -trialnumber)
head(dfgte)

jpeg("gte_trialwise.jpg", width = 1920, height = 1080)
# Visualization
ggplot(dfgte, aes(x = trialnumber, y = value)) + 
  geom_line(aes(color = variable, linetype = variable))+
  labs(title="Gaze entropy vs Trials",x = "Trials", y = "SGE") +
  theme(axis.title = element_text(size = 32), 
        axis.text = element_text(size = 26),
        plot.title = element_text(size=32),
        legend.key.size = unit(3, 'cm'), #change legend key size
        legend.title = element_text(size=26), #change legend title font size
        legend.text = element_text(size=26)) #change legend text font size
dev.off()