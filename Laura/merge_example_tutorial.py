# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 19:34:01 2016

@author: Laura
"""
from mpl_toolkits.mplot3d import proj3d
import matplotlib.pyplot as plt
import numpy as np
import csv

width = 12
height = 17

x, y, z = [], [], []

with open('datapoint.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        data = map(int, row)
        if not x:
            x = data
        elif not y:
            y = data
        elif not z:
            z = data

array = np.array((x, y, z))
X = np.transpose(array)

def visualize3DData (X):
    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c = 'r', marker = 'o', picker = True)
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_zlim(-4, 4)
    
    ax.axis('off')
    #grid(b = True, which = 'major', color = 'b')

    def distance(point, event):
        # Project 3d data space to 2d data space
        x2, y2, _ = proj3d.proj_transform(point[0], point[1], point[2], plt.gca().get_proj())
        # Convert 2d data space to 2d screen space
        x3, y3 = ax.transData.transform((x2, y2))

        return np.sqrt ((x3 - event.x)**2 + (y3 - event.y)**2)


    def calcClosestDatapoint(X, event):
        distances = [distance (X[i, 0:3], event) for i in range(X.shape[0])]
        return np.argmin(distances)


    def annotatePlot(X, index, event):
        """Create popover label in 3d chart

        Args:
            X (np.array) - array of points, of shape (numPoints, 3)
            index (int) - index (into points array X) of item which should be printed
        Returns:
            None
        """
        # If we have previously displayed another label, remove it first
        if hasattr(annotatePlot, 'label'):
            annotatePlot.label.remove()
        #if event.x < 300:
            #annotatePlot.label.remove()
        # Get data point from array of points X, at position index
        x2, y2, _ = proj3d.proj_transform(X[index, 0], X[index, 1], X[index, 2], ax.get_proj())
        annotatePlot.label = plt.annotate( "%d" % (index + 1),
                xy = (x2, y2), xytext = (-20, 20), textcoords = 'offset points', ha = 'right', va = 'bottom',
                bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
                arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
        fig.canvas.draw()
                    
        
    def onMouseMotion(event):
        closestIndex = calcClosestDatapoint(X, event)
        annotatePlot (X, closestIndex, event)

    fig.canvas.mpl_connect('motion_notify_event', onMouseMotion)  # on mouse motion
    plt.show()

visualize3DData(X)