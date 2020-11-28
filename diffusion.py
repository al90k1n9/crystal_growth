import numpy as np
import os
from matplotlib import pyplot as plt
import random as rd

L=10

crystal= np.asarray([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
 [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
 [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
 [1., 0., 1., 0., 0., 0., 0., 0., 0., 0.],
 [1., 1., 1., 0., 0., 1., 0., 0., 0., 0.],
 [1., 0., 0., 0., 0., 1., 1., 0., 0., 0.],
 [1., 1., 0., 0., 0., 1., 0., 0., 0., 1.],
 [1., 0., 0., 0., 0., 1., 0., 0., 0., 0.],
 [1., 0., 0., 0., 0., 1., 0., 0., 0., 0.],
 [1., 0., 1., 1., 1., 1., 1., 0., 0., 0.],
 [1., 0., 1., 0., 1., 0., 1., 0., 1., 0.],
 [1., 1., 1., 1., 1., 0., 1., 1., 1., 0.],
 [0., 0., 0., 1., 1., 0., 0., 1., 1., 0.],
 [0., 0., 1., 1., 1., 0., 0., 1., 1., 0.],
 [0., 1., 1., 0., 0., 0., 0., 1., 1., 1.]])

"""All particles are given a chance to diffuse but only one step at a time, only a certain number of times, defined by the diffusion_range variable. The order of diffusion is going to be random. If the particle finds itself in a local maximum, then the particle MUST move randomly. If the particle finds itself in a flat region, we assume that the thermal agitation of the system is large enough to make the particle randomly in the flat surface."""

initial_crystal = np.copy(crystal)
print("initial number of particles: ", np.sum(crystal))
print("\n\n\n")
def height_per_column(col):
    global L
    for i in range(len(col)):
        if col[i]:
            return (L - i)
    return 0

rows, cols = np.shape(crystal)
diffusion_order = np.arange(cols)
rd.shuffle(diffusion_order)
print(diffusion_order)
diffusion_range = 1


for col in diffusion_order:
    h = height_per_column(crystal[:,col])
    h_plus = height_per_column(crystal[:,(col+1)%cols])
    h_minus = height_per_column(crystal[:,col-1])
    if crystal[L-h, col] < diffusion_range+1:
        if (h_minus < h and h_plus < h) or (h_minus == h_plus == h):
            print(col,"first")
            if rd.random()>0.5:
                crystal[cols-h_plus-1,(col+1)%cols] = 1 + crystal[L-h,col]
            else :
                crystal[cols-h_minus-1, col-1] = 1 + crystal[L-h,col]
            crystal[L-h,col] = 0
            continue
        if h_minus <= h:
            print(col,"second")
            crystal[cols-h_minus-1, col-1] = 1 + crystal[L-h,col]
            crystal[L-h,col] = 0
            continue
        if h_plus <= h:
            print(col,"third")
            crystal[cols-h_plus-1,(col+1)%cols] = 1 + crystal[L-h,col]
            crystal[L-h,col] = 0
            continue




print("final number of particles: ", np.sum(crystal))
fig, axs = plt.subplots(1,2)
fig.suptitle("crystal before and after diffusion of range 1")
axs[0].imshow(initial_crystal)
axs[1].imshow(crystal)
plt.show()
