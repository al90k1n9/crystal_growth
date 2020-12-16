import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit as cf
import os


def test_func1(x, beta, c):
    return c*(x**beta)

def test_func2(x, d):
    return d

def alpha_fit(x, q, alpha):
    return q*(x**alpha)

prefix = "w_vs_t_"
suffix = [(50,2500,100),(100,5000,100),(200, 10000,100),(500,25000,100),(800,40000,100),(1000,50000,100)]
linear_xmin = [10,10,10,10, 5, 5]
linear_xmax = [26,70,70,100,300,300]
constant_xmin = [500,900,2500,3000,10000,30000]
best_parameters = []
for index in range(len(suffix)):
    filename = prefix + str(suffix[index])
    ylist = np.loadtxt(filename)
    xlist, ylist = ylist[:,0] , ylist[:,1]
    L = suffix[index][0]
    #plot_legend.append("L=" + str(L))
    n_particles = suffix[index][0] * suffix[index][1]
    best_param1, covar1 = cf(test_func1, xlist[linear_xmin[index]:linear_xmax[index]], ylist[linear_xmin[index]:linear_xmax[index]])
    best_param2, covar2 = cf(test_func2, xlist[constant_xmin[index]:], ylist[constant_xmin[index]:])
    best_parameters.append([L,best_param1[0], best_param1[1], best_param2[0]])
    #plt.plot(xlist, ylist)
    #plt.plot(xlist, test_func1(xlist, best_param1[0], best_param1[1]))
    #plt.plot(xlist, test_func2(xlist, best_param2[0]) * np.ones(np.shape(xlist)))

best_parameters = np.asarray(best_parameters)
L = best_parameters[:,0]
tx = (best_parameters[:,3]/best_parameters[:,2])**(1/best_parameters[:,1])
tx.shape= (6,1)
best_parameters = np.concatenate((best_parameters, tx), axis = 1)
print("L, beta, c, d, tx : \n", best_parameters)
constants = best_parameters[:,2]
alpha_fit_params, alpha_fit_covar =  cf(alpha_fit, L, constants)
print("beta: ", np.mean(best_parameters[:,1]), " +- ", np.std(best_parameters[:,1]))
print("alpha: ", alpha_fit_params[1], " +- ", alpha_fit_covar[1,1])



"""plt.yscale("log")
plt.xscale("log")
#plt.legend(plot_legend)
plt.xlabel("Number of monolayers")
plt.ylabel("w")
#os.chdir("/home/algoking/Documents/M2/crystal_growth/results")
#plt.savefig("w_monolayers_L_50_1000_logscale.png")
#os.chdir("/home/algoking/Documents/M2/crystal_growth")
plt.show()"""
