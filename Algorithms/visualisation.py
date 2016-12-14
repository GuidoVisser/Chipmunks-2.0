"""
Visualisation of board after A-star run
inspiration from http://stackoverflow.com/questions/10374930/matplotlib-annotating-a-3d-scatter-plot
"""
from mpl_toolkits.mplot3d import proj3d
import matplotlib.pyplot as plt
import numpy as np

def init(width, height, gates, moves, path_lengths, total_length):

    # draw gate positions as scatter data
    def drawScatter(gates, width, height):
        # load gate data
        for i in range(0, len(gates)):
            ax.scatter(gates[i].x, gates[i].y, gates[i].z, c='r', marker='o', s=60, alpha=1)
    
        # set dimensions
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        ax.set_zlim(0, 7)
        
        # show plot without axes
        ax.axis('off')
    
    # on mouse motion, recalculate closest gate and reannotate plot
    def onMouseMotion(event):
        closestIndex = calcClosestDatapoint(gates, event)
        annotatePlot(gates, closestIndex, event)   

    # returns index of smallest value in distances array (which is gate index)
    def calcClosestDatapoint(gates, event):        
        distances = [distance(np.array((gates[i].x, gates[i].y, gates[i].z)), event) for i in range(0, len(gates))]
        return np.argmin(distances)
    
    # returns distance of mouse to gate
    def distance(gate, event):
        # project 3d data space to 2d data space
        x2, y2, _ = proj3d.proj_transform(gate[0], gate[1], gate[2], plt.gca().get_proj())
        # Convert 2d data space to 2d screen space
        x_screen, y_screen = ax.transData.transform((x2, y2))
    
        return np.sqrt((x_screen - event.x) ** 2 + (y_screen - event.y) ** 2)
    
    # make label for closest gate
    def annotatePlot(gates, index, event):        
        # if there was a label already, remove it on mousemove
        if hasattr(annotatePlot, 'label'):
            annotatePlot.label.remove()
        # position and lay-out label
        x2, y2, _ = proj3d.proj_transform(gates[index].x, gates[index].y, gates[index].z, ax.get_proj())
        annotatePlot.label = plt.annotate("%d" % (index + 1), xy=(x2, y2), ha='right', va='bottom', 
                                          bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.9))
        fig.canvas.draw()
    
    # draw grid of XY plane            
    def drawXYplane(width, height):
        # draw x-directed lines
        for line in range(0, width + 1):
           plt.plot([line, line], [0, height], color='black', lw=1, alpha=0.5)
        # draw y-directed lines
        for line in range(0, height + 1):
            plt.plot([0, width], [line, line], color='black', lw=1, alpha=0.5)
    
    # draw moves (A-star output)
    def drawMoves(moves, path_lengths, total_length):
        # i is index of moves, j is index of array of path lengths
        i, j = 1, 0
        # k is length of j-th item in path lengths, count_length is count for drawn moves
        k = int(path_lengths[j])
        count_length = 0
        # keep drawing until all moves are drawn
        while count_length < total_length:
            plt.plot([moves[i - 1][0], moves[i][0]], [moves[i - 1][1], moves[i][1]], 
                     [moves[i - 1][2], moves[i][2]], color='black', lw=2, alpha=1)
            count_length += 1
            # if path length is reached and j is within scope, skip one move draw
            # (from end of one path to start of the other)
            if (i == k) and (j < len(path_lengths) - 1):
                i += 1
                j += 1
                k += path_lengths[j] + 1
            i += 1
    
    #print gates[0:1].x
    
    # initiate figure and 3d projection
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    
    # draw gates as scatter plot and annotate gates on mouse motion
    drawScatter(gates, width, height)
    fig.canvas.mpl_connect('motion_notify_event', onMouseMotion)
    
    # draw XY plane grid and moves
    drawXYplane(width, height) 
    drawMoves(moves, path_lengths, total_length) 