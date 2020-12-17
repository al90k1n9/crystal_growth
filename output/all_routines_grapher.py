import numpy as np
from matplotlib import pyplot as plt
import os
from scipy.optimize import curve_fit as cf

results_directory = "/home/algoking/Documents/M2/crystal_growth/results"
output_directory = "/home/algoking/Documents/M2/crystal_growth/output"

def test_func1(x, beta, c):
    return c*(x**beta)


suffix = (100,5000,100)
L,m,routines = suffix
prefix = "all_routines_"
filename = prefix + str(suffix)
data = np.loadtxt(filename)
print("Data shape : ",np.shape(data))
linear_xmin = 10
linear_xmax = 70
pure_data = data[:,1:]
pure_data_ave = np.sum(pure_data, axis = 1)/np.shape(pure_data)[1]

#fitting all the curves
"""xlist = np.arange(linear_xmin, linear_xmax,1)
betas = []
for col in range(np.shape(pure_data)[1]):
     best_param, covar = cf(test_func1, xlist, data[linear_xmin:linear_xmax,col])
     betas.append(best_param[0])
print("# betas, min beta, max_beta: ",len(betas), min(betas), max(betas))
best_param,covar = cf(test_func1, xlist, pure_data_ave[linear_xmin:linear_xmax])
c = best_param[1]"""

for i in range(np.shape(data)[1]-1):
    plt.plot(data[:,0], data[:,i+1], alpha = 0.2)
plt.axvspan(linear_xmin,linear_xmax, color = 'red', alpha = 0.3)
plt.plot(data[:,0], pure_data_ave)
#xlist = np.arange(1,np.shape(data)[0])
#plt.plot(xlist, test_func1(xlist, min(betas), c),color = 'r')
#plt.plot(xlist, test_func1(xlist, max(betas), c), color = 'r')
plt.xscale("log")
plt.yscale('log')
plt.xlabel("number of monolayers")
plt.ylabel("w(t)")
plt.title("height deviation of " + str(routines) + " different depositions of L="+ str(L)+ ", m=" + str(m))


os.chdir(results_directory)
#plt.savefig("all_routines_" + str(suffix) + ".png")
plt.show()
