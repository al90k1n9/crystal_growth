import os
from tqdm import tqdm
from matplotlib import pyplot as plt
import multiprocessing as mp
import numpy as np
import random as rd
from datetime import datetime

L = 10
monolayers = 10
n_particles = L*monolayers
routines = 1
diff_range = 3

#crystal[np.shape(crystal)[0]-(int(heights[col])), col] = 1


def one_deposition():
    global L
    global n_particles
    std_height_time = np.zeros(monolayers)
    heights = np.zeros(L)
    std_index=0
    for i in tqdm(range(n_particles)):
        col = rd.randint(0,L-1)
        local_heights=[]
        for i in range(col-diff_range, col+diff_range+1):
            local_heights.append(heights[i])
        min_col = local_heights.index(min(local_heights))
        heights[min_col] += 1
        """if i%L == 0:
            std_height_time[std_index] += np.std(heights)
            std_index+=1"""
    return heights

pool = mp.Pool(mp.cpu_count())
results = [pool.apply_async(one_deposition, args=()) for iteration in range(routines)]
Results = [elem.get() for elem in results]
pool.close()
std_height_time = np.zeros(n_particles//L)
"""for elem in Results:
    std_height_time += elem
std_height_time = std_height_time/routines"""
plt.imshow(Results[0])
plt.show()


"""os.chdir("/home/algoking/Documents/M2/crystal_growth/output")
file = open("w_vs_t_(" + str(L) + ", " + str(monolayers) + ", " + str(routines) + ")", "w")
for index in range(len(std_height_time)):
    file.write(str(index) + " " + str(std_height_time[index])+"\n")
file.close()
print(datetime.now()-start)"""
