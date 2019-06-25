#
# FIT R Bootcamp
# Follow-along script
#
# Author: Oliver Schneider oliver.schneider@hpi.de
#

###########################
#
# PART 1 - Data Wrangling
#
###########################


#
# import data
#

# read in data
hicks.law.data <- read.table("data/combined.txt", sep="\t", header=T);

# help
help(hicks.law.data)

# calculate mean
mean(hicks.law.data$partiID)

# confirm type
class(hicks.law.data$partiID)
hicks.law.data$partiID <- factor(hicks.law.data$partiID);
class(hicks.law.data$partiID)
mean(hicks.law.data$partiID)



#
# plot data
#

# plot raw data
plot(hicks.law.data$tEnd.ms.)


#
# transform data
#

# remove time=0
hicks.law.data <- hicks.law.data[hicks.law.data$tEnd.ms.!=0,]
plot(hicks.law.data$tEnd.ms.)

# plot histogram
hist(hicks.law.data$tEnd.ms.)

# group for plotting
hicks.law.data$plot.group <- paste(hicks.law.data$fNmb,
                                   hicks.law.data$gesture,
                                   hicks.law.data$gestureSet);


# plot histogram by group
library(lattice);
histogram(~tEnd.ms. | partiID*plot.group,
          nint=30, data = hicks.law.data)


# log transform and normality plots
hicks.law.data$log_time <- log(hicks.law.data$tEnd.ms.);
histogram(~log_time | partiID*plot.group,
          nint=30, data = hicks.law.data)






###########################
#
# PART 2 - Analysis
#
###########################



#
# plot results
#

#plot means and standard error
# install.packages("gplots");
library(gplots);
plotmeans(log_time~condiID, data=hicks.law.data,
          xlab="Condition ID",
          ylab="Logarithm of Response Time",
          main="Mean Plot\nwith 95% CI");


#
# anova
#

# fit anova (analysis of variance = aov)
fit <- aov(	log_time ~ gestureSet*gesture*fNmb + partiID,
            data = hicks.law.data);

#use Type III SS and F Tests
drop1(fit, ~., test="F")



#
# post-hoc analysis
#

# Bonferroni corrected multiple comparison
pairwise.t.test(
  hicks.law.data$log_time,                 
  paste(hicks.law.data$gestureSet,
        hicks.law.data$gesture,
        hicks.law.data$fNmb),
  alternative="two.sided",
  p.adjust.method = "bonf")


# interaction plots
interaction.plot(	response=hicks.law.data$log_time,
                  x.factor=hicks.law.data$gestureSet,
                  trace.factor=paste(hicks.law.data$gesture,
                                     hicks.law.data$fNmb),
                  ylab="Logarithm of Response Time",
                  xlab="Gesture Set",
                  main="Interaction Plots");


