import os
from tqdm import tqdm
from matplotlib import pyplot as plt
import numpy as np
import random as rd
from datetime import datetime

start = datetime.now()
L = 100
monolayers = L*40
n_particles = L*monolayers
routines = 100

#crystal = np.zeros([monolayers*4,L])
std_height_time = np.zeros(n_particles//L)

for iteration in tqdm(range(routines)):
    heights = np.zeros(L)
    std_index=0
    for i in tqdm(range(n_particles)):
        col = rd.randint(0,L-1)
        heights[col] = max(heights[col]+1, heights[col-1], heights[(col+1)%L])
        #crystal[np.shape(crystal)[0]-(int(heights[col])), col] = 1
        """if i%L == 0:
            std_height_time[std_index] += np.std(heights)
            std_index+=1"""

std_height_time = std_height_time/routines


os.chdir("/home/algoking/Documents/M2/crystal_growth/output")
file = open("revised_w_vs_t_(" + str(L) + ", " + str(monolayers) + ", " + str(routines) + ")", "w")
for index in range(len(std_height_time)):
    file.write(str(index) + " " + str(std_height_time[index])+"\n")
file.close()
print(datetime.now()-start)
