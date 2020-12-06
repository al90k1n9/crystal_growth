import numpy as np
import random as rd
from tqdm import tqdm
from matplotlib import pyplot as plt
import os

def drop_one_particle(crystal, particle_number):
    global L
    if (particle_number//(10*L))%2 == 1: particle_presence_value = 1
    else: particle_presence_value = 2
    x_dim, y_dim= np.shape(crystal)        #getting the dimensions of the crystal
    col = rd.randint(0,y_dim-1)             #choosing a random column simulating a random deposition of particles
    if crystal[0,col] == 0:                 #makes sure that the chosen column is not already full
        for row in range(x_dim):
            if row == x_dim - 1:            #the particle has reached the bottom of the substrate
                crystal[row,col] = particle_presence_value
                break
            if crystal[row + 1, col] != 0 or (row != 0 and crystal[row, (col+1)%y_dim] != 0) or (row!=0 and crystal[row, (col-1)%y_dim] != 0):
                crystal[row,col] = particle_presence_value
                break
        limit_condition = False
        if row == 1:
            new_crystal = np.zeros([x_dim+3,y_dim])
            new_crystal[3:, :y_dim] = crystal
            crystal = new_crystal
            row += 3

    else:                                   #chosen column is full. let the user know
        limit_condition = True
    #global file
    #file.write(str(np.shape(crystal)[0]-row) + " "+ str(col) + "\n" )
    return(crystal, limit_condition)


def peek_in_diffuse(crystal):
    rows, cols = np.shape(crystal)
    diffusion_order = np.arange(cols)
    rd.shuffle(diffusion_order)
    diffusion_range = 1
    for col in diffusion_order:
        h = height_per_column(crystal[:,col])
        h_plus = height_per_column(crystal[:,(col+1)%cols])
        h_minus = height_per_column(crystal[:,col-1])
        if h!=0:
            if crystal[rows-h, col] < diffusion_range+1:
                if h_plus < h-1 and h_minus < h-1:
                    if h_plus < h_minus: crystal[rows-h_plus-1,(col+1)%cols] = 1 + crystal[rows-h,col]
                    elif h_minus < h_plus :crystal[rows-h_minus-1,(col-1)] = 1 + crystal[rows-h,col]
                    else:
                        if rd.random()<0.5 : crystal[rows-h_plus-1,(col+1)%cols] = 1 + crystal[rows-h,col]
                        else : crystal[rows-h_minus-1,(col-1)] = 1 + crystal[rows-h,col]
                    crystal[rows-h,col] = 0
                    continue
                if h_minus < h-1:
                    crystal[rows-h_minus-1,(col-1)] = 1 + crystal[rows-h,col]
                    crystal[rows-h,col] = 0
                    continue
                if h_plus < h-1:
                    crystal[rows-h_plus-1,(col+1)%cols] = 1 + crystal[rows-h,col]
                    crystal[rows-h,col] = 0
                    continue
    return crystal

def height_per_column(col):
    for i in range(len(col)):
        if col[i]:
            return (len(col) - i)
    return 0

def deviation(x):
    return abs(np.mean(x - x.mean()))

def height_analysis(crystal):       #returns std dev and mean height of the crystal
    column_heights = []
    for col in range(L):
        column_heights.append(height_per_column(crystal[:,col]))

    column_heights = np.asarray(column_heights)
    mean_height = np.mean(column_heights)
    std_height = deviation(column_heights)
    return(mean_height, std_height, column_heights)



def correlation_r(heights):
    global L
    r_values = np.arange(L-1) + 1
    mean_height = np.mean(heights)
    g_r = np.zeros(L)
    for r in r_values:
        g = (np.roll(heights, -r)-mean_height) * (heights - mean_height)
        g_r[r] = np.mean(np.asarray(g))
    return(g_r)



####################################################################################################
####################################################################################################

monolayers = 200
L=100
n_particles = monolayers * L
y_dim = 3
std_height_time = np.zeros(n_particles)
routines = 100
#os.chdir("/home/algoking/Documents/M2/crystal_growth/output")
#file = open("crystal.dat", "w")
correlation_t = np.zeros([L,n_particles])
for iteration in tqdm(range(routines)):
    crystal = np.zeros([y_dim, L])
    for i in tqdm(range(n_particles)):
        crystal, error = drop_one_particle(crystal,i)
        if error:
            print("Error!! number of particles deposited so far: ", i-1)
            break
        #crystal = peek_in_diffuse(crystal)
        mean, std, column_heights = height_analysis(crystal)
        std_height_time[i]+=std
std_height_time = std_height_time/routines
"""plt.imshow(crystal)
plt.show()"""

os.chdir("/home/algoking/Documents/M2/crystal_growth/output")
file = open("w_vs_t_(" + str(L) + ", " + str(monolayers)+", " + str(routines)+")", "w")
for index in range(len(std_height_time)):
    file.write(str(index) + " " + str(std_height_time[index]) + "\n" )
file.close()
os.chdir("/home/algoking/Documents/M2/crystal_growth/")
