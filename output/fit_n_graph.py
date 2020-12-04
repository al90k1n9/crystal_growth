import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit as cf
import os

def heavy_side(x):                          #step function
    return x>0

def test_func(x, beta, alpha):
    global L
    tx = L**(alpha/beta)
    return heavy_side(tx-x)*(x**beta) + heavy_side(x-tx)*(L**alpha)

def interface_width(n_particles, std_height_time, show_params = False, data = True, data_fit = True):
    global L
    xlist = np.arange(n_particles)/L
    best_param, covar = cf(test_func, xlist, std_height_time,p0 = [1, 1])
    tx = L**(best_param[1]/best_param[0])
    if show_params:
        print(best_param, np.log(tx-L))
        #print("t0: ", tx)
        #print("z: ",np.log(tx-L))
        #print(covar)

    if data: plt.plot(xlist/tx,std_height_time/(L**best_param[1]))
    if data_fit: plt.plot(xlist/tx, test_func(xlist, best_param[0], best_param[1])/(L**best_param[1]))


prefix = "w_vs_t_"
suffix = [(50,200,100), (100,300,100), (200,500,100), (300,700,100)]
plot_legend=[]
for elem in suffix:
    filename = prefix + str(elem)
    ylist = np.loadtxt(filename)
    ylist = ylist[:,1]
    L = elem[0]
    plot_legend.append("L=" + str(L))
    n_particles = elem[0] * elem[1]
    interface_width(n_particles, ylist, data_fit=False)

plt.yscale("log")
plt.xscale("log")
plt.legend(plot_legend)
plt.xlabel("Number of monolayers/cross-over time")
plt.ylabel("w/saturation_value")

os.chdir("/home/algoking/Documents/M2/crystal_growth/results")
plt.savefig("w_monolayers_L_50_300_logscale_collapse.png")
#os.chdir("/home/algoking/Documents/M2/crystal_growth")
plt.show()
