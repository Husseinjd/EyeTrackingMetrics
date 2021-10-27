#---------------------------------------------------------------------------------------------------------
#R Code for Chapter 3 of:
#
#Field, A. P., Miles, J. N. V., & Field, Z. C. (2012). Discovering Statistics Using R: and Sex and Drugs and Rock 'N' Roll. #London Sage
#
#(c) 2011 Andy P. Field, Jeremy N. V. Miles & Zoe C. Field
#-----------------------------------------------------------------------------------------------------------


#-----------Metallica Data---------------------------------------------------------------------------

metallica<-c("lars", "james", "Jason", "Kirk")
metallica 
metallica<-metallica[metallica != "Jason"]  # remove jason
metallica
metallica<-c(metallica, "Rob") # append rob
metallica
metallicaNames<-c("Lars", "James", "Kirk", "Rob")
metallicaAges<-c(47, 47, 48, 46)

# metallica<-list(metallicaNames, metallicaAges)
# metallica<-cbind(metallicaNames, metallicaAges)

metallica<-data.frame(Name = metallicaNames, Age = metallicaAges)
metallica$childAge<-c(12, 12, 4, 6)
metallica$fatherhoodAge<-metallica$Age-metallica$childAge

#-----------Lecturer Data---------------------------------------------------------------------------

name<-c("Ben", "Martin","Andy","Paul", "Graham","Carina","Karina","Doug","Mark", "Zoe")

#Default date format is yyyy-mm-dd
birth_date<-as.Date(c("1977-07-03", "1969-05-24", "1973-06-21", "1970-07-16", "1949-10-10", "1983-11-05", "1987-10-08", "1989-09-16", "1973-05-20", "1984-11-12"))

job<-c(1,1,1,1,1,2,2,2,2,2) # line below does the same thing
# job<-c(rep(1, 5),rep(2, 5))

job<-factor(job, levels = c(1:2), labels = c("Lecturer", "Student")) # line below does the same thing
# job<-gl(2, 5, labels = c("Lecturer", "Student"))

friends<-c(5,2,0,4,1,10,12,15,12, 17)
alcohol<-c(10,15,20,5,30,25,20,16,17,18)
income<-c(20000,40000,35000,22000,50000,5000,100,3000,10000,10)
neurotic<-c(10,17,14,13,21,7,13,9,14,13)

lecturerData<-data.frame(name, birth_date, job, friends, alcohol,income, neurotic)
# lecturerData$job<-factor(lecturerData$job, levels = c(1:2), labels = c("Lecturer", "Student")) # same as line 38

#--------Selecting Data-----------

lecturerPersonality <- lecturerData[, c("friends", "alcohol", "neurotic")]
lecturerPersonality
lecturerOnly <- lecturerData[job=="Lecturer",]
lecturerOnly
alcoholPersonality <- lecturerData[alcohol > 10, c("friends", "alcohol", "neurotic")]
alcoholPersonality
alcoholPersonalityMatrix <- as.matrix(alcoholPersonality)
alcoholPersonalityMatrix

alcoholPersonalityMatrix <- as.matrix(lecturerData[alcohol > 10, c("friends", "alcohol", "neurotic")])


#--------Subset-----------

lecturerOnly <- subset(lecturerData, job=="Lecturer")
alcoholPersonality <- subset(lecturerData, alcohol > 10, select = c("friends", "alcohol", "neurotic"))

