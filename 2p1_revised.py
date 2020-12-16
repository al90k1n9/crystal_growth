import os
from tqdm import tqdm
from matplotlib import pyplot as plt
import numpy as np
import random as rd

L = 1000
#monolayers = L*500
monolayers= 50
n_particles = L*monolayers * L
routines = 1

#crystal = np.zeros([monolayers*4,L])
std_height_time = np.zeros(monolayers)

for iteration in tqdm(range(routines)):
    heights = np.zeros([L,L])
    std_index = 0
    for i in tqdm(range(n_particles)):
        col = rd.randint(0,L-1)
        row = rd.randint(0,L-1)
        heights[col, row] = max(heights[col, row]+1, heights[col-1, row], heights[(col+1)%L, row], heights[col, row-1], heights[col, (row+1)%L] )
        #crystal[np.shape(crystal)[0]-(int(heights[col])), col] = 1
        if i%L**2 == 0:
            std_height_time[std_index] += np.std(heights)
            std_index += 1

std_height_time = std_height_time/routines


file = open("2p1_revised_w_vs_t_(" + str(L) + ", " + str(monolayers) + ", " + str(routines) + ")", "w")
for index in range(len(std_height_time)):
    file.write(str(index) + " " + str(std_height_time[index])+"\n")
file.close()
