import os
from tqdm import tqdm
from matplotlib import pyplot as plt
import multiprocessing as mp
import numpy as np
import random as rd
from datetime import datetime

L = 1000
monolayers = L*50
routines = 100
diff_range = 1
correlation_time_stamps = np.arange(1,20)
output_directory = "/home/algoking/Documents/M2/crystal_growth/output/diffusion/"

calc_correlation = False
calc_w = True
if calc_correlation: monolayers = max(correlation_time_stamps) + 1
n_particles = L*monolayers

crystal = np.zeros([monolayers*2, L])

#crystal[np.shape(crystal)[0]-(int(heights[col])), col] = 1

def correlation_func(time, heights):
    #gives the correlation of a given crystal for a given time
    mean_height = np.mean(heights)
    g = []
    g.append(time)
    for r in range(-L//2, L//2):
        g.append(np.mean((np.roll(heights, -r)-mean_height) * (heights-mean_height)))
    return np.asarray(g)

def find_min_col(heights, col):
    global diff_range, L
    min_col = col
    for i in range(1, diff_range + 1):
        if heights[(col+i)%L] == heights[col-i]:
            continue
        if heights[(col+i)%L]<heights[col]:
            min_col = (col+i)%L
        if heights[col-i]<heights[col]:
            min_col = col-i
    return min_col


def one_deposition():
    global L, monolayers, n_particles, diff_range, crystal
    #std_height_time = np.zeros(monolayers)
    heights = np.zeros(L)
    std_index = 0
    std_height_time = np.zeros(monolayers)
    correlation = []
    for i in tqdm(range(n_particles)):
        col = rd.randint(0,L-1)
        min_col = find_min_col(heights, col)
        heights[min_col] += 1
        """if (i//(10*L))%2 == 0:
            crystal[np.shape(crystal)[0] - int(heights[min_col]), min_col] = 1
        else:
            crystal[np.shape(crystal)[0] - int(heights[min_col]), min_col] = 2"""
        if i%L == 0 and calc_w:
            std_height_time[std_index] = np.std(heights)
            std_index += 1
        if calc_correlation and i/L in correlation_time_stamps:
            g = correlation_func(i/L, heights)
            correlation.append(g)
    if calc_w:
        return std_height_time
    if calc_correlation:
        return np.asarray(correlation)




pool = mp.Pool(mp.cpu_count())
results = [pool.apply_async(one_deposition, args=()) for iteration in range(routines)]
Results = [elem.get() for elem in results]
pool.close()

os.chdir(output_directory)

if calc_w:
    std_height_time_matrix = np.zeros([monolayers, routines])
    for index in range(len(Results)):
        std_height_time_matrix[:,index] = Results[index]
    file = open("diffusion_w(t)_allroutines_("+ str(L) + ", " + str(monolayers) + ", " + str(routines) +", " + str(diff_range) +")", "w")
    for index in range(np.shape(std_height_time_matrix)[0]):
        file.write(str(index + 1) + " ")
        for col in range(np.shape(std_height_time_matrix)[1]):
            file.write(str(std_height_time_matrix[index,col])+" ")
        file.write("\n")
    file.close()


if calc_correlation:
    correlation_matrix = np.zeros([len(correlation_time_stamps), L+1])
    for correlation in Results:
        correlation_matrix += correlation
    correlation_matrix = correlation_matrix/routines
    file = open("diff_correlation_(" +  str(L) + ", " + str(monolayers) + ", " + str(routines) +", " + str(diff_range) +")", "w")
    for row in range(np.shape(correlation_matrix)[0]):
        for col in range(np.shape(correlation_matrix)[1]):
            file.write(str(correlation_matrix[row,col])+" ")
        file.write("\n")
    file.close()


"""crystal = one_deposition()
plt.imshow(crystal)
plt.show()"""
