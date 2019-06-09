
# %%
a = data[data.gestureSet == "Half"]
b = data[data.gestureSet == "Combined"]
# %%
# #%matplotlib qt5
plt.boxplot([a["tEnd(ms)"],b["tEnd(ms)"]])
plt.savefig("test.png")
# %%
#b["tEnd(ms)"]

# %%
def t_test_wrapper(a,b,alternative, alpha):
    if alternative is "less":
        a,b=b,a
    test_result = ttest_ind(a,b)
    p_val = test_result.pvalue/2
    t = test_result.statistic
    if t < 0:
        p_val = 1-p_val
    if p_val < alpha:
        return True, p_val
    else:
        return False, p_val
#    if alternative is "greater":
#        if p_val < alpha and t >0:
#            return True, p_val
#        else:
#            return False, p_val
#    elif alternative is "less":
#        if p_val < alpha and t < 0:
#            return True, p_val
#        else:
#            return False, p_val
#    else:
#        raise ValueError("alternative must be 'greater' or 'less'")

# %%

data_f = read_data_from_participant("Felix_1")
plot_raw(data_f)
cleaned_f = prepare_data(data_f)
plot_raw(cleaned_f)
plt.legend(["raw","cleaned"])
# %%
f3 = cleaned_f[(cleaned_f["gesture"]=="Flat") & (cleaned_f["fNmb"]==3)]
# %%
plt.boxplot([f3[f3["gestureSet"]=="Half"]["t1st(ms)"],f3[f3["gestureSet"]=="Combined"]["t1st(ms)"]])
# %%
plt.hist(f3["t1st(ms)"],20)
# %%
from scipy.stats import ttest_ind
print(np.mean(f3[f3["gestureSet"]=="Half"]["t1st(ms)"]))
print(np.mean(f3[f3["gestureSet"]=="Combined"]["t1st(ms)"]))

t_test_wrapper(*[f3[f3["gestureSet"]=="Combined"]["t1st(ms)"],f3[f3["gestureSet"]=="Half"]["t1st(ms)"]],"greater",0.05)
# %%
a = np.random.normal(0,size=100)
b = np.random.normal(1,size=100)
result, p = t_test_wrapper(a,b,"less",0.05)
print(p)
assert result == True, "err"
result, p  = t_test_wrapper(a,b,"greater",0.05)
print(p)
assert result == False, "err"


# %%
a = np.random.normal(4,size=100)
b = np.random.normal(3,size=100)
result, p = t_test_wrapper(a,b,"greater",0.05)
print(p)
assert result == True, "err"
result, p  = t_test_wrapper(a,b,"less",0.05)
print(p)
assert result == False, "err"


# %%
