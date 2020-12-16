from matplotlib import pyplot as plt
import numpy as np
import os

data = np.loadtxt("correlation(1000, 50000, 1)")
print(np.shape(data))
L= 1000
correlation_stamps = np.arange(10,2200,250)

plt.plot(np.arange(-L/2, L/2, 1), data[0,:])
plt.plot(np.arange(-L/2, L/2, 1), data[1,:])
os.chdir("/home/algoking/Documents/M2/crystal_growth/results")
plt.xlabel("r")
plt.ylabel("g(r)")
plt.title("correlation function of a crystal with L=1000")
plt.legend([correlation_stamps[0], correlation_stamps[1]])
plt.savefig("correlation(1000,5000).png")
plt.show()
