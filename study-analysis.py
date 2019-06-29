# -*- coding: utf-8 -*-
# %% [markdown]
# # Hick's Law Study

# %% [markdown]
# ## Imports

# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
#use a costum stylesheet
#https://matplotlib.org/3.1.0/gallery/style_sheets/style_sheets_reference.html
plt.style.use("ggplot")
#plt.rcParams["figure.figsize"] = [16,9]
plt.rcParams.update({'font.size': 22,"figure.figsize":[16,9]})
# %%
DATA_PATH = "data"

# %%
from os import listdir
listdir(DATA_PATH)


# %% [markdown]
# ## Data Import

# %% [markdown]
# Let's see if we can load the data correctly and show the top rows of the loaded dataframe.

# %%
def read_data_from_participant(participant_id):
    return pd.read_csv(f"{DATA_PATH}/{participant_id}.txt",sep="\t")


# %%
hicks_law_data = read_data_from_participant("combined2")

# %%
mapping_file_path = f"{DATA_PATH}/participant_mapping.csv"
participant_mapping = {}
with open(mapping_file_path) as f:
    for line in f:
        content = line.replace("\n", "").split(";")
        participant_mapping[content[0]] = content[1]

# %%
participant_mapping

# %% [markdown]
# ## Data Visualization

# %%
var_name = "tEnd(ms)"


# %% [markdown]
# subplots nach subjekten geteilt
# combiniert mit gleicher part id
# If we plot `tEnd(ms)` as a scatter plot, we get the following image:

# %%

import seaborn as sns
plt.rcParams.update({'font.size': 22,"figure.figsize":[16,9]})
for s in hicks_law_data.groupby("partiID"):
    fig, ax = plt.subplots(1, 1)
    dat = pd.DataFrame(s[1])
    participant_names = []
    for i in dat.groupby("filename"):
        p = pd.DataFrame(i[1])
        filename = list(p["filename"])[0]
        ax.plot(p[var_name], marker="o", linestyle = 'None', label=participant_mapping[filename])
#         participant_names.append(participant_mapping[p["filename", 0]])
#         plt.plot(np.arange(0,len(p)),z_transform(p[var_name]),marker="o",linestyle = 'None')
    #sns.lmplot(x = "index", y=var_name, data=dat, fit_reg=False
    #       #  , hue='filename', legend=False, palette="Set2", height=9,aspect=19/9)
    plt.title(f"plot of raw data (set order {s[0]})")
    
    # Move the legend to an empty part of the plot
#     fig.legend([x.split(".")[0] for x in dat["filename"]], loc='upper right')
#     fig.show()
    ax.set_xticklabels([""])
    ax.set_xlabel('trials')
    ax.set_ylabel('time for gesture completion [ms]')

    fig.legend(loc='upper right')
    fig.savefig(f"raw_plot{s[0]}")


# %% [markdown]
# Next, well have a look at the distribution. Therefore we'll create a histogram.

# %%
plt.hist(hicks_law_data[var_name],30)
plt.title("overall distribution of reaction time")
plt.xlabel("reaction time [ms]")
plt.savefig("img/fig2.svg", dpi = 300)
plt.show()


# %% [markdown]
# As expected, this looks somewhat like a normal distribution. We can remove all incorrect trials, to make it "prettier".
#

# %% [markdown]
# ## Compare error rates

# %%
def better_legend(lbl):
    return f"{lbl[0]} finger – {lbl[1].lower()}"
gesture_set_types = ["Half", "Combined"]
legend =[]
means = []
for x in hicks_law_data.groupby(["fNmb","gesture"]):
    print(x[0])
    legend.append(x[0])
    xdf = pd.DataFrame(x[1])
    mean = []
    for part in xdf.groupby(["filename", "gestureSet"]):
        e = part[1][xdf["tEnd(ms)"]==0].count()["tEnd(ms)"]
        t = part[1].count()["tEnd(ms)"]
        mean.append(e/t)
    #mean = [x[1].count()["tEnd(ms)"] for x in ]#[1]["tEnd(ms)"]
    #print(mean)
    
    #allData = [x[1].count()["tEnd(ms)"] for x in xdf.groupby(["filename", "gestureSet"])]
    #print(allData)
    means.append(mean)
    print(np.mean(mean))
    

legend = [better_legend(x) for x in legend]
plt.boxplot(means)
plt.xticks(*list(zip(*enumerate(legend,1))))
plt.title("comparison of error rates")
plt.ylabel("mean error rate [%]")
plt.savefig("img/error.png")
for x, y in zip([means[0]]*3 ,means[1:]):
    print(scipy.stats.mannwhitneyu(x,y))


# %%

# %% [markdown]
# Error rate is significantly higher for 1--Flat gesture.

# %% [markdown]
# ## Data Cleansing/Preparation

# %%
def remove_incorrect(data):
    return data[data["result"]=="correct"]


# %%
hicks_law_data = remove_incorrect(hicks_law_data)
plt.hist(data_correct[var_name],20)
plt.title("distribution of reaction time (errors removed)")
plt.xlabel("reaction time [ms]")
#plt.savefig("img/fig3.svg", dpi = 300)
plt.show()


# %% [markdown]
# As we can see there are still some outliers in the data, but lets see how this looks in a scatter plot.
#

# %%
def take_log(data):
    data["logtime"] = np.log(data[var_name])
    return data
hicks_law_data = take_log(hicks_law_data)


# %%
plt.hist(hicks_law_data["logtime"],30)
plt.title("log distribution of reaction time (errors removed)")
plt.xlabel("log reaction time [log ms]")
#plt.savefig("img/fig3.svg", dpi = 300)
plt.show()


# %% [markdown]
# As we can see most values are between 400 and 800 ms with some outliers below 100 and above 1000. We can assume that these are not real values but instead are errors in the experiment. We are going to remove all values that are more than 3 standard deviations away from the mean. Since we are not interested in absolute values but rather deviation between clases, we could implement this also using the z tranform and throw away everything with $|z| >3$.

# %%
def remove_outliers(data,var, std_mul = 2):
    th1 =  np.mean(data[var]) + std_mul*np.std(data[var])
    th2 =  np.mean(data[var]) - std_mul*np.std(data[var])
    print(f"lower-threshold: {th1} upper-threshold: {th2}")
    return data[(data[var] <= th1) &
            (data[var] >= th2)]



# %%

hicks_law_data = remove_outliers(hicks_law_data, "logtime",2)


# %%
plt.hist(hicks_law_data["logtime"],30)
plt.title("log distribution of reaction time (cleaned)")
plt.xlabel("log of reaction time [ms]")
plt.savefig("img/fig6.svg", dpi = 300)
plt.show()


# %% [markdown]
# ## Normality test

# %%
from scipy import stats
import pylab
from scipy.stats import shapiro
gesture_set_types = ["Half", "Combined"]
for x in hicks_law_data.groupby(["fNmb","gesture", "gestureSet"]):
    xdf = pd.DataFrame(x[1])
    s = stats.shapiro(xdf["logtime"])
    #s= stats.normaltest(xdf["logtime"])
    #s = stats.kstest(xdf["logtime"],"norm")
    print(x[0])
    print(s)
    stats.probplot(xdf["logtime"], dist="norm", plot=pylab)
    pylab.show()


# %%
def print_table_row(lbl, data):
    print(f"\\textit{{{lbl[0]} finger -- {lbl[1].lower()}}} & {data:.4f}\\\\")


# %%
import statsmodels.stats.multitest as multi

gesture_set_types = ["Half", "Combined"]
pvals =[]
lbl = []
for x in hicks_law_data.groupby(["fNmb","gesture"]):
    xdf = pd.DataFrame(x[1])
    u = scipy.stats.mannwhitneyu((xdf[xdf["gestureSet"] == gesture_set_types[0]] [ "logtime"])
                              , (xdf[xdf["gestureSet"] == gesture_set_types[1]] ["logtime"]),
                                 alternative="two-sided")
    lbl.append(x[0])
    pvals.append(u.pvalue)

    #bonferroni correction
pvals = multi.multipletests(pvals,0.25,"bonferroni")[1]   
for x, u in zip(lbl,pvals):
    print_table_row(x,u)

# %%
ages = [45,17.5,25,25,25,25,25]
print(f"min: {min(ages)} max: {max(ages)} mean: {np.mean(ages)} std: {np.std(ages)}")


# %% [markdown]
# ## Interaction plot

# %%
gesture_set_types = ["Half", "Combined"]
legend =[]
for x in hicks_law_data.groupby(["fNmb","gesture"]):
    legend.append(x[0])
    xdf = pd.DataFrame(x[1])
    plt.plot(xdf.groupby("gestureSet").mean()["logtime"])
plt.legend([better_legend(l) for l in legend])
plt.title("interaction plot")
plt.ylabel("mean log(time) [log(ms)]")
plt.savefig("img/interaction.png")

# %%
gesture_set_types = ["Half", "Combined"]
for x in hicks_law_data.groupby(["gesture","fNmb"]):
    xdf = pd.DataFrame(x[1])
    reaction_times = [xdf[xdf.gestureSet == gesture_set][var_name]
                      for gesture_set in gesture_set_types]
    plt.boxplot(reaction_times)
    plt.xticks(*list(zip(*enumerate(gesture_set_types,1))))
    plt.ylabel("reaction time [ms]")
    plt.title(f"{x[0][1]} Finger {x[0][0]}")
    plt.show()


# %%
# TODO: Anova

# %%
# TODO: pairwise ttest (two sided)


# %%
def make_boxplots(data):
    gestureSets = ["Half", "Combined"]
    for x in data.groupby(["fNmb","gesture"]):
        xdf = pd.DataFrame(x[1])
        title = f"{x[0][0]} Finger{'s' if (int(x[0][0])>1) else ''} - {x[0][1]}"
        plt.title(title)
        reaction_times = [xdf[xdf.gestureSet == gesture_set]["logtime"]
                          for gesture_set in gesture_set_types]
        plt.boxplot(reaction_times)
        plt.xticks(*list(zip(*enumerate(gestureSets,1))))
        plt.ylabel("log reaction time [log ms]")
        plt.savefig(f"img/{title.replace(' ', '')}-box.png",dpi=300)
        plt.show()
make_boxplots(hicks_law_data)

# %%

# dsk = {'load': (read_data_from_participant, 'combined2'),
#        'clean': (remove_incorrect, 'load'),
#        'takelog':(take_log,"clean")
#        ,'box': (make_boxplots, 'takelog'),
#        #'clean-3': (clean, 'load-3'),
#        #'analyze': (analyze, ['clean-%d' % i for i in [1, 2, 3]]),
#        #'store': (store, 'analyze')
#       }

# from dask.multiprocessing import get
# get(dsk, 'box')  # executes in parallel

# %%
import pandas as pd
import scipy.stats as stats
import researchpy as rp
import statsmodels.api as sm
from statsmodels.formula.api import ols

# %%
results = ols('logtime ~ gestureSet*gesture*fNmb + partiID', data=hicks_law_data).fit()
results.summary()


# %%
