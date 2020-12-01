import numpy as np
import os
from matplotlib import pyplot as plt
import random as rd

"""All particles are given a chance to diffuse but only one step at a time, only a certain number of times, defined by the diffusion_range variable. The order of diffusion is going to be random. If the particle finds itself in a local maximum, then the particle MUST move randomly. If the particle finds itself in a flat region, we assume that the thermal agitation of the system is large enough to make the particle randomly in the flat surface."""

def height_per_column(col):
    for i in range(len(col)):
        if col[i]:
            return (len(col) - i)
    return 0

def diffuse(crystal):
    rows, cols = np.shape(crystal)
    print(rows, cols)
    diffusion_order = np.arange(cols)
    rd.shuffle(diffusion_order)
    print(diffusion_order)
    diffusion_range = 1
    for col in diffusion_order:
        h = height_per_column(crystal[:,col])
        h_plus = height_per_column(crystal[:,(col+1)%cols])
        h_minus = height_per_column(crystal[:,col-1])
        print(h, h_minus, h_plus)
        if crystal[rows-h, col] < diffusion_range+1 and h != 0:
            if (h_minus < h and h_plus < h):
                if rd.random()>0.5:
                    crystal[rows-h_plus-1,(col+1)%cols] = 1 + crystal[rows-h,col]
                else :
                    crystal[rows-h_minus-1, col-1] = 1 + crystal[rows-h,col]
                crystal[rows-h,col] = 0
                continue
            if h_minus < h:
                crystal[rows-h_minus-1, col-1] = 1 + crystal[rows-h,col]
                crystal[rows-h,col] = 0
                continue
            if h_plus < h:
                crystal[rows-h_plus-1,(col+1)%cols] = 1 + crystal[rows-h,col]
                crystal[rows-h,col] = 0
                continue
    return crystal

def peek_in_diffuse(crystal):
    rows, cols = np.shape(crystal)
    print(rows, cols)
    diffusion_order = np.arange(cols)
    rd.shuffle(diffusion_order)
    print(diffusion_order)
    diffusion_range = 1
    for col in diffusion_order:
        h = height_per_column(crystal[:,col])
        h_plus = height_per_column(crystal[:,(col+1)%cols])
        h_minus = height_per_column(crystal[:,col-1])
        print(h, h_minus, h_plus)
        if crystal[rows-h, col] < diffusion_range+1 and h != 0:
            if h_plus < h-1 and h_minus < h-1:
                print("condition 1")
                if h_plus < h_minus: crystal[rows-h_plus-1,(col+1)%cols] = 1 + crystal[rows-h,col]
                elif h_minus < h_plus :crystal[rows-h_minus-1,(col-1)] = 1 + crystal[rows-h,col]
                else:
                    if rd.random()<0.5 : crystal[rows-h_plus-1,(col+1)%cols] = 1 + crystal[rows-h,col]
                    else : crystal[rows-h_minus-1,(col-1)] = 1 + crystal[rows-h,col]
                crystal[rows-h,col] = 0
                continue
            if h_minus < h-1:
                print("condition 2")
                crystal[rows-h_minus-1,(col-1)] = 1 + crystal[rows-h,col]
                crystal[rows-h,col] = 0
                continue
            if h_plus < h-1:
                print("condition 3")
                crystal[rows-h_plus-1,(col+1)%cols] = 1 + crystal[rows-h,col]
                crystal[rows-h,col] = 0
                continue
    return crystal

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

initial_crystal = np.copy(crystal)
print("initial number of particles: ", np.sum(crystal))
print("\n\n\n")

crystal = peek_in_diffuse(crystal)

print("final number of particles: ", np.sum(crystal))
fig, axs = plt.subplots(1,3)
fig.suptitle("crystal before and after diffusion of range 1")
axs[0].imshow(initial_crystal)
axs[1].imshow(crystal)
axs[2].imshow(peek_in_diffuse(crystal))
plt.show()
