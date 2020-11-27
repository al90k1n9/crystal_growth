import numpy as np
import random as rd
from tqdm import tqdm
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit as cf
from scipy.optimize import leastsq
import os

def drop_one_particle(crystal):
    x_dim, y_dim= np.shape(crystal)        #getting the dimensions of the crystal
    col = rd.randint(0,y_dim-1)             #choosing a random column simulating a random deposition of particles
    if crystal[0,col] == 0:                 #makes sure that the chosen column is not already full
        for row in range(x_dim):
            if row == x_dim - 1:            #the particle has reached the bottom of the substrate
                crystal[row,col] = 1
                break
            if crystal[row + 1, col] == 1 or (row != 0 and crystal[row, (col+1)%y_dim] == 1) or (row!=0 and crystal[row, (col-1)%y_dim] == 1):
                crystal[row,col] = 1
                break
        limit_condition = False
        if row == 1:
            new_crystal = np.zeros([x_dim+3,y_dim])
            new_crystal[3:, :y_dim] = crystal
            crystal = new_crystal

    else:                                   #chosen column is full. let the user know
        limit_condition = True
    return(crystal, limit_condition)


def height_per_column(col):
    for i in range(len(col)):
        if col[i]:
            return (len(col) - i)
    return 0

def height_analysis(crystal):       #returns std dev and mean height of the crystal
    column_heights = []
    for col in range(L):
        column_heights.append(height_per_column(crystal[:,col]))

    column_heights = np.asarray(column_heights)
    mean_height = np.mean(column_heights)
    std_height = np.std(column_heights)
    return(mean_height, std_height, column_heights)

def heavy_side(x):                          #step function
    return x>0

def test_func(x, beta, alpha):
    global L
    tx = L**(alpha/beta)
    return heavy_side(tx-x)*(x**beta) + heavy_side(x-tx)*(L**alpha)

def cost_func(param, y, x):
    model = test_func(x, param[0], param[1], param[2])
    return y - model


L = 100                       #dimension of the square lattice
monolayers = 200
n_particles = monolayers * L
y_dim = 3


std_height_time = np.zeros(n_particles)

routines = 5
for iteration in tqdm(range(routines)):
    crystal = np.zeros([y_dim, L])
    for i in tqdm(range(n_particles)):
        crystal, error = drop_one_particle(crystal)
        if error:
            print("Error!! number of particles deposited so far: ", i-1)
            break
        mean, std, column_heights = height_analysis(crystal)
        std_height_time[i]+=std

std_height_time = std_height_time/routines
print(height_analysis(crystal))


"""file = open("std_height_time.dat", "w")
for elem in std_height_time:
    file.write(str(elem)+"\n")
file.close()
print(len(std_height_time))"""

xlist = np.arange(n_particles)
best_param, covar = cf(test_func, xlist, std_height_time,p0 = [1, 1])
print(best_param)
tx = L**(best_param[1]/best_param[0])
print("t0: ", tx)
print("z: ",np.log(tx-L))
print(covar)


"""fig = plt.imshow(crystal)
fig.axes.get_xaxis().set_visible(False)
fig.axes.get_yaxis().set_visible(False)"""
plt.plot(std_height_time)
plt.plot(xlist, test_func(xlist, best_param[0], best_param[1]))
"""plt.imshow(crystal)"""
plt.show()
