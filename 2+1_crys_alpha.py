import numpy as np
import random as rd
from tqdm import tqdm
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

L = 5
n_particles = int(0.5*L**2)
crystal = np.zeros([L,L,L])

def neighbours(crystal, i,j,k):
    global L
    status = crystal[i,j,k+1]
    status = status or crystal[i-1,j,k] or crystal[(i+1)%L,j,k]
    status = status or crystal[i,j-1,k] or crystal[i,(j+1)%L,k]
    return bool(status)

def drop_one_particle_3D(crystal):
    global L
    i = rd.randint(0,L-1)
    j = rd.randint(0,L-1)
    if crystal[i,j,0] == 0:
        for k in range(L):
            if k == L-1:
                crystal[i,j,k] = 1
                break
            if neighbours(crystal,i,j,k):
                crystal[i,j,k] = 1
                break
        limit_condition = False
    else:
        limit_condition=True
    return (crystal, limit_condition)

for i in tqdm(range(n_particles)):
    crystal, error = drop_one_particle_3D(crystal)
    if error:
        print("Crystal maxed out. total number of particles deposited so far: ",i-1)
        break

pos = np.where(crystal == 1)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(pos[0],pos[1], pos[2], c= "black", marker = "s",s=1000)
plt.show()
