""""
README:
De afstand tussen twee posities, in 3D, is delta_x plus delta_y plus delta_z
Dit programma rekent het kortste pad uit tussen twee objecten.
Er wordt nog geen regening gehouden met obstakels en de randen van de grid.
Tot nu toe wordt de Position class gebruikt om posities op de grid op te slaan,
maar in de toekomst willen we naar de GridPosition class, omdat we dan simpel kunnen bijhouden welke
punten wel en niet toegankelijk zijn voor volgende paden
TODO:
de cost van posities naast gates moet hoger zijn dan normale posities

Create children in positie te zetten
dynamic en static cost
hou de cost van het pad bij ipv de lengte


"""

from mpl_toolkits.mplot3d import proj3d
import matplotlib.pyplot as plt
import numpy as np
import csv
from Queue import PriorityQueue


class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """

    def __init__(self, x=0, y=0, z=0):
        """
        Initializes a position with coordinates (x, y, z).
        """
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        new = Position()
        new.x = self.x + other.x
        new.y = self.y + other.y
        new.z = self.z + other.z
        return new

    def getDist(self, other):
        """"
        Returns the distance between goal and itself.
        """
        x = abs(self.x - other.x)
        y = abs(self.y - other.y)
        z = abs(self.z - other.z)
        return x + y + z

    def inList(self, list):
        """"
        check if this position is in a list of positions
        """
        for pos in list:
            if pos.x == self.x:
                if pos.y == self.y:
                    if pos.z == self.z:
                        return True
        return False

    def adjacent(self):
        adjacent = []
        adjacent.append(self + Position(1, 0, 0))
        adjacent.append(self + Position(-1, 0, 0))
        adjacent.append(self + Position(0, 1, 0))
        adjacent.append(self + Position(0, -1, 0))
        adjacent.append(self + Position(0, 0, 1))
        adjacent.append(self + Position(0, 0, -1))
        return adjacent

class Grid(object):
    """"
    Grid of points that are either a wall, a gate or free space
    """

    def __init__(self, gates, max_x, max_y, max_z=7):
        self.walls = []
        self.gates = gates
        self.gates_children = []
        self.gates_grandchildren = []
        for x in xrange(-1, max_x + 2):
            for y in xrange(-1, max_y + 2):
                self.walls.append(Position(x, y, -1))
                self.walls.append(Position(x, y, max_z + 1))
        for y in xrange(-1, max_y + 2):
            for z in xrange(0, max_z + 1):
                self.walls.append(Position(-1, y, z))
                self.walls.append(Position(max_x + 1, y, z))
        for x in xrange(0, max_x + 1):
            for z in xrange(0, max_z + 1):
                self.walls.append(Position(x, -1, z))
                self.walls.append(Position(x, max_y + 1, z))
        for gate in gates:
            self.gates_children += gate.adjacent()
        for child in self.gates_children:
            grandchildren = child.adjacent()
            for grandchild in grandchildren:
                if not grandchild.inList(self.gates_grandchildren):
                    self.gates_grandchildren.append(grandchild)

class State(object):
    def __init__(self, grid, position, parent,
                 start=Position(0, 0, 0), goal=Position(0, 0, 0)):
        self.children = []
        self.parent = parent
        self.position = position
        self.grid = grid
        self.dist = 0
        self.static_cost = 0
        self.rating = 0
        self.dynamic_cost = 0
        if parent:
            self.path = parent.path[:]
            self.path.append(position)
            self.static_cost = parent.static_cost
            self.start = parent.start
            self.goal = parent.goal
        else:
            self.path = [position]
            self.start = start
            self.goal = goal

    def createChildren(self, visited_list):
        pass


class StatePosition(State):
    def __init__(self, grid, position, parent,
                 start=Position(0, 0, 0), goal=Position(0, 0, 0)):
        super(StatePosition, self).__init__(grid, position, parent, start, goal)

        # distance to goal
        self.dist = self.position.getDist(self.goal)

        # children are rated on distance to goal plus distance to start
        #self.rating = self.dist * 10 + self.static_cost + self.dynamic_cost
        
        # add rating if passing gate
        #for gate in gates:
        #    if (self.position.getDist(gate) == 1):
        #        self.rating += 21
       
    def createChildren(self, visited_list):
        if not self.children:
            adjacent_positions = self.position.adjacent()
            for pos in adjacent_positions:
                child = StatePosition(self.grid,
                                        pos,
                                        self,
                                        self.start,
                                        self.goal)
                if child.dist == 0:
                    self.children.append(child)
                    break
                else:
                    if not child.position.inList(self.grid.walls) and not child.position.inList(
                            visited_list) and not child.position.inList(self.grid.gates):
                        #if child.position.inList(self.grid.gates_children):
                        #    child.cost = 20
                        
                        for pos in self.grid.gates_children:
                            if pos.x == child.position.x:
                                if pos.y == child.position.y:
                                    if pos.z == child.position.z:
                                        child.static_cost += 21

                        for pos in self.grid.gates_grandchildren:
                            if pos.x == child.position.x:
                                if pos.y == child.position.y:
                                    if pos.z == child.position.z:
                                        child.static_cost += 1
 
                        child.static_cost += 10
                        child.rating = child.dist * 10 + child.static_cost + child.dynamic_cost
                        self.children.append(child)


class AStar_Solver:
    def __init__(self, grid, start, goal):
        """"
        start and goal are both Position classes
        """
        self.path = []
        self.visited = []
        self.priorityQueue = PriorityQueue()
        self.start = start
        self.goal = goal
        self.grid = grid

    def Solve(self):

        # initialize starting point
        startState = StatePosition(self.grid,
                                   self.start,
                                   0,
                                   self.start,
                                   self.goal)

        # add starting point to children
        self.priorityQueue.put((0, startState))

        # as long as path is not defined and there are available children
        while not self.path and self.priorityQueue.qsize():

            # The closest child is the one with the shortest distance to goal
            closestChild = self.priorityQueue.get()[1]
           
            # create the children for this closest child
            closestChild.createChildren(self.visited)

            # add the closest child to the visited list
            self.visited.append(closestChild.position)

            # check for all children if it is already in children
            for child in closestChild.children:

                # check if child is goal
                if child.dist == 0:
                    self.path = child.path
                    break

                # add child to children list
                self.priorityQueue.put((child.rating, child))

        # if no path was found give error message
        if len(self.path) == 0:
            print "Goal is not possible."
            # output.write('Goal is not possible.\n')
            return None

            # return the path that was found
        return self.path


def create_print(filename):
    """"
    takes a string as argument that holds the path to a csv file
    copies the contents of the csv file into a list of position classes
    """
    with open(filename, 'rb') as printfile:
        # check files extension
        if not filename.endswith('.csv'):
           raise TypeError('File is not a .csv file')

        # add coordinates in file to list
        outputlist = []
        csvfile = csv.DictReader(printfile)
        for row in csvfile:
            outputlist.append(Position(int(row['x']), int(row['y']), int(row['z'])))

        printfile.close()
    # return list of positions
    return outputlist


def create_netlist(filename):
    """"
    takes a string as argument that holds the path to a csv file
    copies the contents of the csv file into a list of tuples
    the tuples map to positions in a list made by create_print
    """
    with open(filename, 'rb') as netlistfile:
        # check files extension
        if not filename.endswith('csv'):
           raise TypeError('File is not a .csv file')

        # add connections in file to list
        csvfile = csv.reader(netlistfile)
        netlist = []
        for row in csvfile:
            netlist.append((int(row[0]), int(row[1])))

        netlistfile.close()
    # return list of tuples
    return netlist


def visualise_board(filename, width, height, moves, paths_length, total_length):
    """
    visualise gates
    """

    def drawScatter(X):
        fig = plt.figure()
        ax = fig.gca(projection='3d')

        # load gate data
        ax.scatter(X[:, 0], X[:, 1], X[:, 2], c='r', marker='o', s=60, alpha=1)

        # set dimensions
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        ax.set_zlim(0, 6)

        # show plot without axes
        ax.axis('off')
        plt.show()

        def distance(point, event):
            # Project 3d data space to 2d data space
            x2, y2, _ = proj3d.proj_transform(point[0], point[1], point[2], plt.gca().get_proj())
            # Convert 2d data space to 2d screen space
            x3, y3 = ax.transData.transform((x2, y2))

            return np.sqrt((x3 - event.x) ** 2 + (y3 - event.y) ** 2)

        def calcClosestDatapoint(X, event):
            """

            """
            distances = [distance(X[i, 0:3], event) for i in range(X.shape[0])]
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

        def onMouseMotion(event):
            closestIndex = calcClosestDatapoint(X, event)
            annotatePlot(X, closestIndex, event)

        fig.canvas.mpl_connect('motion_notify_event', onMouseMotion)  # on mouse motion

    def drawXYplane(width, height):
        for line in range(0, width + 1):
            plt.plot([line, line], [0, height], color='black', lw=1, alpha=0.5)
        for line in range(0, height + 1):
            plt.plot([0, width], [line, line], color='black', lw=1, alpha=0.5)

    def drawMoves(moves, paths_length, total_length):
        i, j, count_length = 1, 0, 0
        k = int(paths_length[j])
        while count_length < total_length:
            plt.plot([moves[i - 1][0], moves[i][0]], [moves[i - 1][1], moves[i][1]], [moves[i - 1][2], moves[i][2]],
                     color='black', lw=2, alpha=1)
            count_length += 1
            if (i == k) and (j < len(paths_length) - 1):
                i += 1
                j += 1
                k += paths_length[j] + 1
            i += 1

    with open(filename, 'rb') as printfile:
        ID, x, y, z = [], [], [], []
        X = []
        csvfile = csv.DictReader(printfile)
        for row in csvfile:
            x.append(int(row['x']))
            y.append(int(row['y']))
            z.append(int(row['z']))
            ID.append(int(row['ID']))

        array = np.array((x, y, z, ID))
        X = np.transpose(array)

        printfile.close()

    drawScatter(X)
    drawMoves(moves, paths_length, total_length)
    drawXYplane(width, height)


##====================
## MAIN

print 'running...'

# initialize board
width = 17
height = 12
gates = create_print('print1.csv')
netlist = create_netlist('netlist1.csv')
grid = Grid(gates, width, height)

# determine frequency of gates
freq = [0] * len(gates)
for line in netlist:
    for item in line:
        freq[item] += 1
print freq

queue = PriorityQueue()
sorted_netlist = []
#for elem in netlist:
#    queue.put((gates[elem[0]].getDist(gates[elem[1]]), elem))

for i in xrange(0, len(netlist)):
    sorted_netlist.append(queue.get()[1])

sorted_netlist = [(3,5), (3, 4), (3, 0), (3, 15), (3, 23), (15, 21), (15, 17), (15, 8), (15, 5), (5, 7), (19, 5), (7, 13), (10, 7), (7, 9), (13, 18), (22, 13), (9, 13), (10, 4), (16, 9), (20, 10), (19, 2), (20, 19), (2, 20), (22, 16), (22, 11), (23, 4), (23, 8), (1, 0), ]
    
# total length necessary to connect gates
total_length = 0

# list of all found paths
all_paths = []

count = 1

# run A-Star solver on entire board
for connection in sorted_netlist:

    # initialize solver
    a = AStar_Solver(grid, gates[connection[0]], gates[connection[1]])
    
    # if no solution was found for current path, stop
    if not a.Solve():
        break

    print 'Line %s solved, of length %s' % (count, len(a.path))
    
    # add found path to list of paths
    all_paths.append(a.path)

    # add found path to list of walls
    grid.walls += a.path

    # change total length of paths
    total_length += len(a.path) - 1

    # count amount of paths
    count += 1

filename = 'result%s_%s.txt' % (count - 1, total_length)
output = open(filename, "w")
output.write('%s\n' % (sorted_netlist))

# print out results
count = 1
paths_length, moves_x, moves_y, moves_z = [], [], [], []
for path in all_paths:

    # print length of individual paths
    # print 'length of path #', count, ': ', len(path) - 1
    output.write('Length of path # %s : %s\n' % (count, (len(path) - 1)))
    #print 'Length of  path # %s : %s\n' % (count, (len(path) -1))
    paths_length.append(len(path) - 1)

    # print positions in individual paths
    for position in path:
        moves_x.append(position.x)
        moves_y.append(position.y)
        moves_z.append(position.z)
        output.write('%s %s %s\n' % (position.x, position.y, position.z))
    count += 1

array = np.array((moves_x, moves_y, moves_z))
moves = np.transpose(array)

print 'Number of paths found: %s / %s' % (count - 1, len(sorted_netlist))
output.write('Number of paths found: %s / %s\n' % (count - 1, len(sorted_netlist)))

# for index in range(len(path_length)):
#    print path_length(index)

# print total length
print 'The total length is: ', total_length
output.write('The total length is: %s\n' % (total_length))

print 'done.'

# visualise board
visualise_board('print1.csv', width, height, moves, paths_length, total_length)

output.close()