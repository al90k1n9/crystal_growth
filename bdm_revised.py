import os
from tqdm import tqdm
from matplotlib import pyplot as plt
import numpy as np
import random as rd
from datetime import datetime

start = datetime.now()
L = 1000
monolayers =75
n_particles = L*monolayers
routines = 500
correlation_time_stamps = np.arange(1,72,10) #np.concatenate((correlation_time_stamps,np.asarray([500,900])))

#crystal = np.zeros([monolayers*4,L])
std_height_time = np.zeros(monolayers)
time = []
correlation_matrix = np.zeros([len(correlation_time_stamps),L+1])

for iteration in tqdm(range(routines)):
    correlation = []
    heights = np.zeros(L)
    std_index=0
    for i in tqdm(range(n_particles)):
        col = rd.randint(0,L-1)
        heights[col] = max(heights[col]+1, heights[col-1], heights[(col+1)%L])
        #crystal[np.shape(crystal)[0]-(int(heights[col])), col] = 1
        if i/L in correlation_time_stamps:
            mean_height = np.mean(heights)
            g = []
            g.append(i/L)
            for r in range(-L//2, L//2):
                g.append(np.mean((np.roll(heights, -r)-mean_height) * (heights-mean_height)))
            correlation.append(g)
    correlation_matrix += np.asarray(correlation)
correlation = np.asarray(correlation_matrix)/routines

#std_height_time = std_height_time/routines
"""for i in range(len(correlation)):
    plt.plot(correlation[i])
plt.legend(time)
plt.show()"""

"""os.chdir("/home/algoking/Documents/M2/crystal_growth/output")
file = open("w_vs_t(" + str(L) + ", " + str(monolayers) + ", " + str(routines) + ")", "w")
for index in range(len(std_height_time)):
    file.write(str(index) + " " + str(std_height_time[index])+"\n")
file.close()
print(datetime.now()-start)"""


print(np.shape(correlation))
col = -L/2
os.chdir("/home/algoking/Documents/M2/crystal_growth/output")
file = open("correlation_avenorm_["+ str(correlation_time_stamps[0]) +","+ str(correlation_time_stamps[-1])+"]_(" + str(L) + ", " + str(routines) + ")", "w")
for index in range(np.shape(correlation)[0]):
    for g_r in range(np.shape(correlation)[1]):
        file.write(str(correlation[index][g_r])+" ")
    file.write("\n")
file.close()
