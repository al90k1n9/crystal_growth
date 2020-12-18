from matplotlib import pyplot as plt
import numpy as np
import os

filename = "correlation_[1,19]_(100, 21, 1000)"
data = np.loadtxt(filename)
print(np.shape(data))
prefix1, time_stamp_range, L_m_r = filename.split("_")
L= int(L_m_r[1:-1].split(",")[0])

plot_legend=[]
for i in range(0,np.shape(data)[0]):
    plt.plot(np.arange(-L/2, L/2, 1), data[i,1:])
    plot_legend.append("m = "+str(data[i,0]))

os.chdir("/home/algoking/Documents/M2/crystal_growth/results")
plt.xlabel("r")
plt.ylabel("g(r)")
plt.title("correlation function of a crystal with L="+str(L))
plt.legend(plot_legend)
plt.savefig(filename + ".png")
plt.show()
