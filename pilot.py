# %% [markdown]
# # Hick's Law Study

# %% [markdown]
# ## Imports

# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#use a costum stylesheet
#https://matplotlib.org/3.1.0/gallery/style_sheets/style_sheets_reference.html
plt.style.use("ggplot")
#plt.rcParams["figure.figsize"] = [16,9]
plt.rcParams.update({'font.size': 22,"figure.figsize":[16,9]})
# %%
DATA_PATH = "data"


# %% [markdown]
# ## Data Import

# %% [markdown]
# Let's see if we can load the data correctly and show the top rows of the loaded dataframe.

# %%
def read_data_from_participant(participant_id):
    return pd.read_csv(f"{DATA_PATH}/{participant_id}.txt",sep="\t")


# %%
data = read_data_from_participant("1_114920")
data.head()
# %%
for x in data.groupby(["gesture","fNmb"]):
    #print(x)
    xdf = pd.DataFrame(x[1])
    half = xdf[xdf.gestureSet == "Half"]
    combined = xdf[xdf.gestureSet == "Combined"]
    plt.boxplot([half["tEnd(ms)"],combined["tEnd(ms)"]])
    plt.show()

# %% [markdown]
# ## Data Visualization

# %%
var_name = "tEnd(ms)"

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
plt.show()

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
