import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt
particles_pos = np.loadtxt("crystal.dat")

for index in tqdm(range(0,np.shape(particles_pos)[0],1000)):
    if (index / 1000)%2 == 1:
        plt.plot(particles_pos[index:index+1000,1], particles_pos[index:index+1000,0], linestyle="", marker = "s", color = "b")
    else:
        plt.plot(particles_pos[index:index+1000,1], particles_pos[index:index+1000,0], linestyle="", marker = "s", color = "r")
plt.show()
