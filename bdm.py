import numpy as np
import random as rd
from tqdm import tqdm
from matplotlib import pyplot as plt
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
            row += 3

    else:                                   #chosen column is full. let the user know
        limit_condition = True
    #global file
    #file.write(str(np.shape(crystal)[0]-row) + " "+ str(col) + "\n" )
    return(crystal, limit_condition)


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
        if crystal[(rows-h)%rows, col] < diffusion_range+1 and h != 0:
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

monolayers = 20
L=10
n_particles = monolayers * L
y_dim = 3
std_height_time = np.zeros(n_particles)
routines = 1
#os.chdir("/home/algoking/Documents/M2/crystal_growth/output")
#file = open("crystal.dat", "w")
correlation_t = np.zeros([L,n_particles])
for iteration in tqdm(range(routines)):
    crystal = np.zeros([y_dim, L])
    for i in tqdm(range(n_particles)):
        crystal, error = drop_one_particle(crystal)
        if error:
            print("Error!! number of particles deposited so far: ", i-1)
            break
        mean, std, column_heights = height_analysis(crystal)
        g_r = correlation_r(column_heights)
        correlation_t[:,i] = g_r
        #std_height_time[i]+=std
"""file.close()
os.chdir("/home/algoking/Documents/M2/crystal_growth/")"""
#std_height_time = std_height_time/routines
#plt.imshow(crystal)
#plt.show()
print(correlation_t)

os.chdir("/home/algoking/Documents/M2/crystal_growth/output")
file = open("cor_(100,200,1)", "w")
for row in range(np.shape(correlation_t)[0]):
    for col in range(np.shape(correlation_t)[1]):
        file.write(str(correlation_t[row,col])+" ")
    file.write("\n")
file.close()
os.chdir("/home/algoking/Documents/M2/crystal_growth/")
