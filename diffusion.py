import os
from tqdm import tqdm
from matplotlib import pyplot as plt
import multiprocessing as mp
import numpy as np
import random as rd
from datetime import datetime

L = 10
monolayers = 3
n_particles = L*monolayers
routines = 1
diff_range = 3

calc_correlation = False
calc_w = True

crystal = np.zeros([L, monolayers * 4])

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
    for i in range(n_particles):
        col = rd.randint(0,L-1)
        min_col = find_min_col(heights, col)
        heights[min_col] += 1
        print(col,min_col, heights)
        crystal[np.shape(crystal)[0] - int(heights[min_col]), min_col] = 1

    if calc_w:
        return crystal

crystal = one_deposition()
plt.imshow(crystal)
plt.show()
