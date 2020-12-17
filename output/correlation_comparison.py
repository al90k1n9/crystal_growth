from matplotlib import pyplot as plt
import numpy as np
import os

filename1 = "correlation_[1,71]_(1000, 500)"
data1 = np.loadtxt(filename1)
prefix1,time_stamp_range, dim_routines = filename1.split("_")
L1= int(dim_routines[1:-1].split(",")[0])

filename2 = "correlation_[1,71]_(100, 500)"
data2 = np.loadtxt(filename2)
prefix1,time_stamp_range, dim_routines = filename2.split("_")
L2= int(dim_routines[1:-1].split(",")[0])

"""fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle("correlation function of m=11 for different dimensions")
ax1.plot(np.arange(-L1/2, L1/2,1), data1[4,1:])
ax1.plot(np.arange(-L2/2, L2/2,1), data2[4,1:])
ax1.legend(["L="+str(L1), "L="+str(L2)])
ax1.set(xlabel= "r", ylabel = "g(r)")
ax1.set_title("without shift")


ax2.plot(np.arange(-L1/2, L1/2,1), data1[4,1:])
ax2.plot(np.arange(-L2/2, L2/2,1), data2[4,1:]+5)
ax2.legend(["L="+str(L1), "L="+str(L2)])
ax2.set(xlabel= "r", ylabel = "g(r)")
ax2.set_title("with shift")"""


plt.plot(np.arange(-L1/2, L1/2,1), data1[1,1:])
plt.plot(np.arange(-L2/2, L2/2,1), data2[1,1:])
plt.xlabel("r")
plt.ylabel("g(r)")
os.chdir("/home/algoking/Documents/M2/crystal_growth/results")
#plt.savefig("correlation_comparison_w_wo_shift.png")
plt.show()
