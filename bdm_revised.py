import os
from tqdm import tqdm
from matplotlib import pyplot as plt
import numpy as np
import random as rd
from datetime import datetime

start = datetime.now()
L = 1000
monolayers = 2200
n_particles = L*monolayers
routines = 1

#crystal = np.zeros([monolayers*4,L])
std_height_time = np.zeros(monolayers)
correlation = []
time = []

for iteration in tqdm(range(routines)):
    heights = np.zeros(L)
    std_index=0
    for i in tqdm(range(n_particles)):
        col = rd.randint(0,L-1)
        heights[col] = max(heights[col]+1, heights[col-1], heights[(col+1)%L])
        #crystal[np.shape(crystal)[0]-(int(heights[col])), col] = 1
        if i/L in np.arange(10,2200,250):
            mean_height = np.mean(heights)
            g = []
            time.append(i/L)
            for r in range(-L//2, L//2):
                g.append(np.mean((np.roll(heights, -r)-mean_height) * (heights-mean_height)))
            correlation.append(g)

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
file = open("correlation(" + str(L) + ", " + str(monolayers) + ", " + str(routines) + ")", "w")
for index in range(np.shape(correlation)[0]):
    for g_r in range(np.shape(correlation)[1]):
        file.write(str(correlation[index][g_r])+" ")
    file.write("\n")
file.close()
