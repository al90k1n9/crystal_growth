import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

x=[]
y=[]
file = open("anim_data", "r")
for line in file:
    u,v = line.split(" ")
    x.append(int(u))
    y.append(int(v))

x = np.asarray(x)
y = np.asarray(y)
(x,y) = (y,x)
print(x,y)
size = np.random.randint(150, size=10)
colors = np.random.choice(["r", "g", "b"], size=10)

fig = plt.figure()
plt.xlim(0, 25)
plt.ylim(0, 50)
graph = plt.scatter([], [], marker = "s", s= 120)
def animate(i):
    graph.set_offsets(np.vstack((x[:i+1], y[:i+1])).T)
    return graph

ani = FuncAnimation(fig, animate, repeat=False, interval=200)
plt.show()
