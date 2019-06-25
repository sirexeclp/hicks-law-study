# %% [markdown]
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Hick's-Law-Study" data-toc-modified-id="Hick's-Law-Study-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Hick's Law Study</a></span><ul class="toc-item"><li><span><a href="#Imports" data-toc-modified-id="Imports-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Imports</a></span></li><li><span><a href="#Data-Import" data-toc-modified-id="Data-Import-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Data Import</a></span></li><li><span><a href="#Data-Visualization" data-toc-modified-id="Data-Visualization-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Data Visualization</a></span></li><li><span><a href="#Data-Cleansing/Preparation" data-toc-modified-id="Data-Cleansing/Preparation-1.4"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>Data Cleansing/Preparation</a></span></li><li><span><a href="#Tutorial" data-toc-modified-id="Tutorial-1.5"><span class="toc-item-num">1.5&nbsp;&nbsp;</span>Tutorial</a></span></li><li><span><a href="#Plot-raw-data" data-toc-modified-id="Plot-raw-data-1.6"><span class="toc-item-num">1.6&nbsp;&nbsp;</span>Plot raw data</a></span></li><li><span><a href="#Remove-&quot;errors&quot;" data-toc-modified-id="Remove-&quot;errors&quot;-1.7"><span class="toc-item-num">1.7&nbsp;&nbsp;</span>Remove "errors"</a></span></li><li><span><a href="#Global-Histogram" data-toc-modified-id="Global-Histogram-1.8"><span class="toc-item-num">1.8&nbsp;&nbsp;</span>Global Histogram</a></span></li></ul></li></ul></div>

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
    dat = pd.DataFrame(s[1])
    for i in dat.groupby("filename"):
        p = pd.DataFrame(i[1])
        plt.plot(np.arange(0,len(p)),z_transform(p[var_name]),marker="o",linestyle = 'None')
    #sns.lmplot(x = "index", y=var_name, data=dat, fit_reg=False
    #       #  , hue='filename', legend=False, palette="Set2", height=9,aspect=19/9)
    plt.title(f"plot of raw data (set order {s[0]})")
    # Move the legend to an empty part of the plot
    plt.legend([x.split(".")[0] for x in dat["filename"]], loc='upper right')
    plt.show()
    plt.savefig(f"raw_plot{s[0]}")

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
hicks_law_data = pd.read_csv("data/combined.txt",sep="\t")
hicks_law_data.head()

# %%
hicks_law_data.partiID = hicks_law_data.partiID.astype('category')

# %% [markdown]
# ## Plot raw data

# %%
plt.plot(hicks_law_data["tEnd(ms)"], "bo")

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
li

# %%
hicks_law_data["logtime"] = np.log(hicks_law_data["tEnd(ms)"])

gesture_set_types = ["Half", "Combined"]
for x in hicks_law_data.groupby(["fNmb","gesture", "gestureSet"]):
    xdf = pd.DataFrame(x[1])
    plt.hist(xdf["logtime"],30)
    plt.show()

# %%
plt.boxplot([pd.DataFrame(x[1])["logtime"] for x in hicks_law_data.groupby(["condiID"])])
plt.show()

# %%
# TODO: Anova

# %%
# TODO: pairwise ttest (two sided)

# %%
