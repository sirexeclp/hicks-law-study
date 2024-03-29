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
data = read_data_from_participant("combined2")
data.head()
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

#subplots nach subjekten geteilt
#combiniert mit gleicher part id

# %%
plt.rcParams.update({'font.size': 22,"figure.figsize":[16,9]})
def plot_raw(data):
    plt.plot(data[var_name],marker="o",linestyle = 'None')
    plt.ylim(bottom=True)
    #plt.xlim(left=True)
    plt.xlabel("trial")
    plt.ylabel("reaction time [ms]")


# %% [markdown]
# If we plot `tEnd(ms)` as a scatter plot, we get the following image:

# %%
plot_raw(data)
plt.title("reaction time vs. trails (raw)")
plt.savefig("img/fig1.svg", dpi = 300)
plt.savefig("img/fig1.png", dpi = 300)
plt.show()

# %%
# library & dataset
data["index"]=data.index

def z_transform(val):
    return (np.array(val) - np.mean(val))/np.std(val)

import seaborn as sns
#plt.figure(figsize=(16, 9))
for s in data.groupby("partiID"):
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

# %%
# ?sns.lmplot

# %% [markdown]
# Next, well have a look at the distribution. Therefore we'll create a histogram.

# %%
plt.hist(data[var_name],20)
plt.title("overall distribution of reaction time")
plt.xlabel("reaction time [ms]")
plt.savefig("img/fig2.svg", dpi = 300)
plt.show()


# %% [markdown]
# As expected, this looks somewhat like a normal distribution. We can remove all incorrect trials, to make it "prettier".

# %% [markdown]
# ## Data Cleansing/Preparation

# %%
def remove_incorrect(data):
    return data[data["result"]=="correct"]


# %%
data_correct = remove_incorrect(data)
plt.hist(data_correct[var_name],20)
plt.title("distribution of reaction time (errors removed)")
plt.xlabel("reaction time [ms]")
plt.savefig("img/fig3.svg", dpi = 300)
plt.show()

# %% [markdown]
# As we can see there are still some outliers in the data, but lets see how this looks in a scatter plot.

# %%
plot_raw(data_correct)
plt.title("reaction time vs. trails (errors removed)")
plt.savefig("img/fig4.svg", dpi = 300)
plt.show()
# %% [markdown]
# As we can see most values are between 400 and 800 ms with some outliers below 100 and above 1000. We can assume that these are not real values but instead are errors in the experiment. We are going to remove all values that are more than 3 standard deviations away from the mean. Since we are not interested in absolute values but rather deviation between clases, we could implement this also using the z tranform and throw away everything with $|z| >3$.

# %%
def remove_outliers(data, std_mul = 3):
    th1 =  np.mean(data[var_name]) + std_mul*np.std(data[var_name])
    th2 =  np.mean(data[var_name]) - std_mul*np.std(data[var_name])
    print(f"lower-threshold: {th1} upper-threshold: {th2}")
    return data[(data[var_name] <= th1) &
            (data[var_name] >= th2)]

def prepare_data(data):
    cleaned_data = remove_incorrect(data)
    cleaned_data = remove_outliers(cleaned_data)
    return cleaned_data


# %%
old_len = len(data)
data_clean = prepare_data(data)
new_len = len(data_clean)
print(f"{old_len-new_len} records removed")

# %%
plt.hist(np.log(data_clean[var_name]),20)
plt.title("log distribution of reaction time (cleaned)")
plt.xlabel("log of reaction time [ms]")
plt.savefig("img/fig6.svg", dpi = 300)
plt.show()

# %% [markdown]
# To see which data points have been removed, let's overlay raw and cleaned data.

# %%
plot_raw(data)
plot_raw(data_clean)
plt.title("reaction time vs. trails (raw & cleaned)")
plt.legend(["raw","cleaned"])
plt.savefig("img/fig5.svg", dpi = 300)
plt.show()

# %%
gesture_set_types = ["Half", "Combined"]
for x in data_clean.groupby(["gesture","fNmb"]):
    xdf = pd.DataFrame(x[1])
    reaction_times = [xdf[xdf.gestureSet == gesture_set][var_name]
                      for gesture_set in gesture_set_types]
    plt.boxplot(reaction_times)
    plt.xticks(*list(zip(*enumerate(gesture_set_types,1))))
    plt.ylabel("reaction time [ms]")
    plt.title(f"{x[0][1]} Finger {x[0][0]}")
    plt.show()


# %% [markdown]
# ## Tutorial

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
hicks_law_data = pd.read_csv("data/combined2.txt",sep="\t")
hicks_law_data.head()

# %%
hicks_law_data.partiID = hicks_law_data.partiID.astype('category')

# %% [markdown]
# ## Plot raw data

# %%
plt.plot(hicks_law_data["tEnd(ms)"], "bo")

# %% [markdown]
# ## Compare error rates

# %%
gesture_set_types = ["Half", "Combined"]
legend =[]
for x in hicks_law_data.groupby(["fNmb","gesture"]):
    print(x[0])
    legend.append(x[0])
    xdf = pd.DataFrame(x[1])
    print(xdf[xdf["tEnd(ms)"]==0].groupby("gestureSet").count()["tEnd(ms)"])
    plt.plot(xdf[xdf["tEnd(ms)"]==0].groupby("gestureSet").count()["tEnd(ms)"])
plt.legend(legend)

# %% [markdown]
# ## Remove "errors"

# %%
hicks_law_data = hicks_law_data[hicks_law_data["tEnd(ms)"]!=0]

# %%
plt.plot(hicks_law_data["tEnd(ms)"], "bo")

# %% [markdown]
# ## Global Histogram

# %%
plt.hist(hicks_law_data["tEnd(ms)"])


# %%
def take_log(data):
    data["logtime"] = np.log(data["tEnd(ms)"])
    return data
hicks_law_data = take_log(hicks_law_data)

# %%
gesture_set_types = ["Half", "Combined"]
for x in hicks_law_data.groupby(["fNmb","gesture", "gestureSet"]):
    xdf = pd.DataFrame(x[1])
    plt.hist(xdf["logtime"],30)
    plt.show()

# %%
plt.boxplot([pd.DataFrame(x[1])["logtime"] for x in hicks_law_data.groupby(["condiID"])])
plt.show()

# %% [markdown]
# ## Interaction plot

# %%
gesture_set_types = ["Half", "Combined"]
legend =[]
for x in hicks_law_data.groupby(["fNmb","gesture"]):
    #print(x[0])
    legend.append(x[0])
    xdf = pd.DataFrame(x[1])
    #print(xdf[xdf["tEnd(ms)"]!=0].groupby("gestureSet").mean()["tEnd(ms)"])
    plt.plot(xdf.groupby("gestureSet").mean()["logtime"])
plt.legend(legend)

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
