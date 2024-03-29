import numpy as np
from math import *
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter



# load in 3d point cloud
with open("airport.pts", "r") as f:
    pts3 = [ [ float(x) for x in l.split(" ") ] for l in f.readlines() ]
pts3

def animate_above(frame_number): 

    global tx, ty, tz, yaw, tilt, twist
    ty += 20 
    tz += 0.2 * frame_number

    m1 = np.array([[f,0,0],
                   [0,f,0],
                   [0,0,1]])
    m2 = np.array([[1,0,0],
                   [0,np.cos(tilt), - np.sin(tilt)],
                   [0, np.sin(tilt), np.cos(tilt)]])
    m3 = np.array([[np.cos(twist), 0 , -np.sin(twist)],
                   [0,1,0],
                   [np.sin(twist), 0, np.cos(twist)]])
    m4 = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                   [np.sin(yaw), np.cos(yaw), 0],
                   [0,0,1]])
    m5 = np.array([[1,0,0,tx],
                  [0,1,0,ty],
                  [0,0,1,tz]])
    projection_matrix = m1 @ m2 @ m3 @ m4 @ m5
    projection_matrix
    pts4 = [p +[1] for p in pts3]

    t_3D = pts4 @ projection_matrix.T
    t_3D = [p for p in t_3D if p[2] > 0]
    pr=[]
    pc=[]
    for p in t_3D:
        pr += [p[0]/p[2]]
        pc += [p[1]/p[2]]

    plt.cla()
    plt.gca().set_xlim([-0.002, 0.002])
    plt.gca().set_ylim([-0.002, 0.002])
    line, = plt.plot(pr, pc, 'k',  linestyle="", marker=".", markersize=2)

    return line,

(tx, ty, tz) = (0, 0, 5)
(tilt, twist, yaw) = (pi/2, 0 , pi)
f = 0.002


# create animation!
fig, ax  = plt.subplots()
frame_count = 50
ani = animation.FuncAnimation(fig, animate_above, frames=range(0,frame_count))

#writer = FFMpegWriter(fps=20, metadata=dict(artist='Me'), bitrate=1800)
#ani.save('movie.mp4', writer=writer)

plt.show()



