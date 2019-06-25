hicks.law.data <- read.csv("data/combined.txt", sep="\t");

class(hicks.law.data$partiID)
hicks.law.data$partiID <- factor(hicks.law.data$partiID)
class(hicks.law.data$partiID)
mean(hicks.law.data$partiID)

plot(hicks.law.data$tEnd.ms.)

hicks.law.data <- 
  hicks.law.data[hicks.law.data$tEnd.ms.!=0,]

plot(hicks.law.data$tEnd.ms.)

hist(hicks.law.data$tEnd.ms.)
#hist(log(hicks.law.data$tEnd.ms.))

hicks.law.data$plot.group <- paste(hicks.law.data$fNmb,
              hicks.law.data$gesture, hicks.law.data$gestureSet);

library(lattice);
histogram(~ tEnd.ms. | partiID*plot.group, 
          nint=30, data = hicks.law.data)

hicks.law.data$log_time <- log(hicks.law.data$tEnd.ms.)

histogram(~log_time | partiID*plot.group,
          nint=30, data = hicks.law.data)

#install.packages("gplots")
library(gplots)

plotmeans(log_time~condiID, data=hicks.law.data)

interaction.plot(response = hicks.law.data$log_time,
                 x.factor = hicks.law.data$gestureSet,
                 trace.factor = paste(hicks.law.data$gesture,hicks.law.data$fNmb))

#Anova
# + partiID
fit <- aov(log_time ~ 
             gestureSet*gesture*fNmb, data = hicks.law.data)
drop1(fit,~.,test="F")


#two sided test to be more conservative
pairwise.t.test(hicks.law.data$log_time,
                paste(hicks.law.data$gestureSet,
                      hicks.law.data$gesture,
                      hicks.law.data$fNmb),
                alternative = "two.sided",
                p.adjust.method = "bonf")

#ggplot2 lib for butifull graphs