import numpy as np
from matplotlib import pyplot as plt
import os
import random as rd
from tqdm import tqdm

p = 0.9
L = 100
limiting_time = 100
routines = 10000

std_height_time = np.zeros(limiting_time)
for j in tqdm(range(routines)):
    particles = 0
    heights = np.zeros(L)
    for time in range(limiting_time):
        for i in range(L):
            if rd.random() < p:
                new_heights = np.copy(heights)
                new_heights[i] = max(heights[i]+1, heights[i-1], heights[(i+1)%L])
                heights = new_heights
                particles += 1
        std_height_time[time] += np.std(heights)

plt.plot(np.arange(0,limiting_time, 1), std_height_time)
plt.show()
