import os
from tqdm import tqdm
from matplotlib import pyplot as plt
import multiprocessing as mp
import numpy as np
import random as rd
from datetime import datetime

def correlation(time, heights):
    mean_height = np.mean(heights)
    g = []
    g.append(time)
    for r in range(-L//2, L//2):
        g.append(np.mean((np.roll(heights, -r)-mean_height) * (heights-mean_height)))
    return np.asarray(g)



L = 100
monolayers = L*50
n_particles = L*monolayers
routines = 100

#crystal = np.zeros([monolayers*4,L])
#crystal[np.shape(crystal)[0]-(int(heights[col])), col] = 1

std_height_time_matrix = np.zeros([monolayers, routines])

def one_deposition():
    global L
    global n_particles
    std_height_time = np.zeros(monolayers)
    heights = np.zeros(L)
    std_index=0
    for i in tqdm(range(n_particles)):
        col = rd.randint(0,L-1)
        heights[col] = max(heights[col]+1, heights[col-1], heights[(col+1)%L])
        if i%L == 0:
            std_height_time[std_index] = np.std(heights)
            std_index+=1
    return std_height_time

pool = mp.Pool(mp.cpu_count())
results = [pool.apply_async(one_deposition, args=()) for iteration in range(routines)]
Results = [elem.get() for elem in results]
pool.close()
for index in range(len(Results)):
    std_height_time_matrix[:,index] = Results[index]




os.chdir("/home/algoking/Documents/M2/crystal_growth/output")
file = open("all_routines_(" + str(L) + ", " + str(monolayers) + ", " + str(routines) + ")", "w")
for index in range(np.shape(std_height_time_matrix)[0]):
    file.write(str(index + 1) + " ")
    for col in range(np.shape(std_height_time_matrix)[1]):
        file.write(str(std_height_time_matrix[index,col])+" ")
    file.write("\n")
file.close()
