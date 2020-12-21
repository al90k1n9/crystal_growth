import os
from tqdm import tqdm
from matplotlib import pyplot as plt
import multiprocessing as mp
import numpy as np
import random as rd
from datetime import datetime

def correlation_func(time, heights):
    mean_height = np.mean(heights)
    g = []
    g.append(time)
    for r in range(-L//2, L//2):
        g.append(np.mean((np.roll(heights, -r)-mean_height) * (heights-mean_height)))
    return np.asarray(g)



L = 1000
monolayers = 21
n_particles = L*monolayers
routines = 500
calc_w = False
calc_correlation = True
correlation_time_stamps = np.arange(1,10,1)

#crystal = np.zeros([monolayers*4,L])
#crystal[np.shape(crystal)[0]-(int(heights[col])), col] = 1

std_height_time_matrix = np.zeros([monolayers, routines])
correlation_matrix = np.zeros([len(correlation_time_stamps), L+1])

def one_deposition():
    global L
    global n_particles
    global calc_w, calc_correlation, correlation_time_stamps
    std_height_time = np.zeros(monolayers)
    heights = np.zeros(L)
    std_index=0
    correlation = []
    for i in tqdm(range(n_particles)):
        col = rd.randint(0,L-1)
        heights[col] = max(heights[col]+1, heights[col-1], heights[(col+1)%L])
        if i%L == 0:
            if calc_w:
                std_height_time[std_index] = np.std(heights)
                std_index+=1
            if calc_correlation and i/L in correlation_time_stamps:
                g = correlation_func(i/L, heights)
                correlation.append(g)
    if calc_w and calc_correlation:
        return (std_height_time, correlation)
    if calc_correlation:
        return np.asarray(correlation)
    if calc_w:
        return std_height_time

pool = mp.Pool(mp.cpu_count())
results = [pool.apply_async(one_deposition, args=()) for iteration in range(routines)]
Results = [elem.get() for elem in results]
pool.close()


os.chdir("/home/algoking/Documents/M2/crystal_growth/output")
if calc_correlation:
    for correlation in Results:
        correlation_matrix += correlation
    correlation_matrix = correlation_matrix / routines
    file = open("correlation_[" + str(correlation_time_stamps[0]) + "," + str(correlation_time_stamps[-1]) + "]_(" + str(L) + ", " + str(monolayers) + ", " + str(routines) + ")","w")
    for index in range(np.shape(correlation_matrix)[0]):
        for col in range(np.shape(correlation_matrix)[1]):
            file.write(str(correlation_matrix[index,col]) + str(" "))
        file.write("\n")
    file.close()


if calc_w:
    for index in range(len(Results)):
        std_height_time_matrix[:,index] = Results[index]
    file = open("all_routines_(" + str(L) + ", " + str(monolayers) + ", " + str(routines) + ")", "w")
    for index in range(np.shape(std_height_time_matrix)[0]):
        file.write(str(index + 1) + " ")
        for col in range(np.shape(std_height_time_matrix)[1]):
            file.write(str(std_height_time_matrix[index,col])+" ")
        file.write("\n")
    file.close()
