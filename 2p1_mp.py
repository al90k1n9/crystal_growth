import os
from tqdm import tqdm
from matplotlib import pyplot as plt
import numpy as np
import random as rd
import multiprocessing as mp
from datetime import datetime

start = datetime.now()
L = 50
monolayers= 50
n_particles = L*monolayers * L
routines = 100


def one_deposition():
    global L
    global monolayers
    global n_particles
    std_height_time = np.zeros(monolayers)
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
    return std_height_time

pool = mp.Pool(mp.cpu_count())
results = [pool.apply_async(one_deposition, args=()) for iteration in range(routines)]
Results = [elem.get() for elem in results]
pool.close()
std_height_time = np.zeros(monolayers)
for elem in Results:
    std_height_time += elem
std_height_time = std_height_time/routines


file = open("2p1_revised_w_vs_t_(" + str(L) + ", " + str(monolayers) + ", " + str(routines) + ")", "w")
for index in range(len(std_height_time)):
    file.write(str(index) + " " + str(std_height_time[index])+"\n")
file.close()
print(datetime.now()-start)
