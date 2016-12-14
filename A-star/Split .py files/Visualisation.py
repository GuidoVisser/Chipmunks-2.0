# -*- coding: utf-8 -*-
"""
Visualisation of board after A-star run
"""
from mpl_toolkits.mplot3d import proj3d
import matplotlib.pyplot as plt
import numpy as np
import csv

class DrawScatter:
    """
    visualise gates
    """
    def __init__(self, width, height, gates):
        self.gates = gates
        x, y, z = [], [], []

        for i in range(0, len(gates)):
            x.append(gates[i].x)
            y.append(gates[i].y)
            z.append(gates[i].z)
            
        self.X = np.array((x, y, z))
        self.fig = plt.figure()
        self.ax = self.fig.gca(projection='3d')

        # load gate data
        self.ax.scatter(self.X[:, 0], self.X[:, 1], self.X[:, 2], c='r', marker='o', s=60, alpha=1)

        # set dimensions
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        self.ax.set_zlim(0, 6)

    def distance(point, event):
        # Project 3d data space to 2d data space
        x2, y2, _ = proj3d.proj_transform(point[0], point[1], point[2], plt.gca().get_proj())
        # Convert 2d data space to 2d screen space
        x3, y3 = ax.transData.transform((x2, y2))

        return np.sqrt((x3 - event.x) ** 2 + (y3 - event.y) ** 2)

    def calcClosestDatapoint(X, event):
        
        distances = [distance(X[i, 0:3], event) for i in range(X.shape[0])]
        return np.argmin(distances)

    def annotatePlot(X, index, event):        
        # If we have previously displayed another label, remove it first
        if hasattr(annotatePlot, 'label'):
            annotatePlot.label.remove()
            # if event.x < 300:
            # annotatePlot.label.remove()
        # Get data point from array of points X, at position index
        x2, y2, _ = proj3d.proj_transform(X[index, 0], X[index, 1], X[index, 2], ax.get_proj())
        annotatePlot.label = plt.annotate("%d" % (index + 1),
                                          xy=(x2, y2), xytext=(-20, 20), textcoords='offset points', ha='right',
                                          va='bottom',
                                          bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                                          arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        fig.canvas.draw()

    def onMouseMotion(self, event):
        closestIndex = calcClosestDatapoint(X, event)
        annotatePlot(X, closestIndex, event)
    
    def initiate(self):
        # show plot without axes
        self.ax.axis('off')
        plt.show()
        self.fig.canvas.mpl_connect('motion_notify_event', onMouseMotion(self, self.event))
        

def drawXYplane(width, height):
    for line in range(0, width + 1):
        plt.plot([line, line], [0, height], color='black', lw=1, alpha=0.5)
    for line in range(0, height + 1):
        plt.plot([0, width], [line, line], color='black', lw=1, alpha=0.5)

def drawMoves(moves, paths_length, total_length):
    i, j, count_length = 1, 0, 0
    k = int(paths_length[j])
    while count_length < total_length:
        plt.plot([moves[i - 1][0], moves[i][0]], [moves[i - 1][1], moves[i][1]], 
                 [moves[i - 1][2], moves[i][2]], color='black', lw=2, alpha=1)
        count_length += 1
        if (i == k) and (j < len(paths_length) - 1):
            i += 1
            j += 1
            k += paths_length[j] + 1
        i += 1