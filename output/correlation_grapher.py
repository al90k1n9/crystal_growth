import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
from matplotlib.animation import FuncAnimation
plt.style.use('seaborn-pastel')


correlation_t = np.loadtxt("cor_(100,200,1)")
min = 0
max = 0
for row in range(np.shape(correlation_t)[0]):
    for col in range(np.shape(correlation_t)[1]):
        if correlation_t[row,col] < min:
            min = correlation_t[row,col]
        if correlation_t[row,col] > max:
            max = correlation_t[row,col]


fig = plt.figure()
ax = plt.axes(xlim=(0, np.shape(correlation_t)[0]), ylim=(min, max))
line, = ax.plot([], [], lw=3)

def init():
    line.set_data([], [])
    return line,
def animate(i):
    x = np.linspace(0, np.shape(correlation_t)[0], np.shape(correlation_t)[0])
    y = correlation_t[:,i]
    line.set_data(x, y)
    fig.legend("t=" + str(i))
    print(i)
    return line,

anim = FuncAnimation(fig, animate, init_func=init, frames=np.shape(correlation_t)[1], interval=20, blit=True,repeat = False)


anim.save('correlation(100,200).mp4', writer='ffmpeg')
#plt.show()
