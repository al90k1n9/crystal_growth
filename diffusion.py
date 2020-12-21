import os
from tqdm import tqdm
from matplotlib import pyplot as plt
import multiprocessing as mp
import numpy as np
import random as rd
from datetime import datetime

L = 800
monolayers = L*50
n_particles = L*monolayers
routines = 100
diff_range = 1
output_directory = "/home/algoking/Documents/M2/crystal_growth/output/diffusion/"

calc_correlation = False
calc_w = True

crystal = np.zeros([monolayers*2, L])

#crystal[np.shape(crystal)[0]-(int(heights[col])), col] = 1

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
    for i in tqdm(range(n_particles)):
        col = rd.randint(0,L-1)
        min_col = find_min_col(heights, col)
        heights[min_col] += 1
        """if (i//(10*L))%2 == 0:
            crystal[np.shape(crystal)[0] - int(heights[min_col]), min_col] = 1
        else:
            crystal[np.shape(crystal)[0] - int(heights[min_col]), min_col] = 2"""
        if i%L == 0:
            std_height_time[std_index] = np.std(heights)
            std_index += 1
    if calc_w:
        return std_height_time




pool = mp.Pool(mp.cpu_count())
results = [pool.apply_async(one_deposition, args=()) for iteration in range(routines)]
Results = [elem.get() for elem in results]
pool.close()

os.chdir(output_directory)
if calc_w:
    std_height_time = np.zeros(monolayers)
    for elem in Results:
        std_height_time += elem
    std_height_time = std_height_time/routines
    file = open("diffusion_w(t)_("+ str(L) + ", " + str(monolayers) + ", " + str(routines) + ")", "w")
    for index in range(len(std_height_time)):
        file.write(str(index) + " " + str(std_height_time[index])+"\n")
    file.close()


"""crystal = one_deposition()
plt.imshow(crystal)
plt.show()"""
