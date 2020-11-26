import numpy as np
import random as rd
from matplotlib import pyplot as plt
from tqdm import tqdm

dim = np.array([50,25])
n_particles = 150

crystal = np.zeros(dim)

skipped_particles = 0
file = open("anim_data", "w")
for i in tqdm(range(n_particles)):
    col = rd.randint(0,dim[1]-1)
    if crystal[0,col] == 0:
        for j in range(dim[0]):
            if j == dim[0] - 1:
                crystal[j,col] = 1
                file.write(str(j)+" "+ str(col) + "\n")
                break
            if crystal[j+1, col] == 1 or (j != 0 and crystal[j, (col+1)%dim[1]]) == 1 or (j!=0 and crystal[j, (col-1)%dim[1]] == 1):
                crystal[j,col] = 1
                file.write(str(j)+" "+ str(col) + "\n")
                break
    else:
        skipped_particles += 1


file.close()
if skipped_particles > 0: print(skipped_particles, " have been skipped. ")
plt.imshow(crystal)
plt.show()
