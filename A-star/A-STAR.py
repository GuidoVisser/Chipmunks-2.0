""""
README:
De afstand tussen twee posities, in 3D, is delta_x plus delta_y plus delta_z

Dit programma rekent het kortste pad uit tussen twee objecten.
Er wordt nog geen regening gehouden met obstakels en de randen van de grid.
Tot nu toe wordt de Position class gebruikt om posities op de grid op te slaan,
maar in de toekomst willen we naar de GridPosition class, omdat we dan simpel kunnen bijhouden welke
punten wel en niet toegankelijk zijn voor volgende paden
"""

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

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z


class Grid(object):
    """"
    Grid of points that are either a wall, a gate or free space
    """
    def __init__(self, gates, max_x, max_y, max_z = 7):
        self.walls = []
        self.gates = gates
        for x in xrange(-1, max_x+2):
            for y in xrange(-1, max_y+2):
                self.walls.append(Position(x, y, -1))
                self.walls.append(Position(x, y, max_z+1))
        for y in xrange(-1, max_y+2):
            for z in xrange(0, max_z+1):
                self.walls.append(Position(-1, y, z))
                self.walls.append(Position(max_x+1, y, z))
        for x in xrange(0, max_x+1):
            for z in xrange(0, max_z+1):
                self.walls.append(Position(x, -1, z))
                self.walls.append(Position(x, max_y+1, z))


class State(object):
    def __init__(self, grid, position, parent,
                 start=Position(0, 0, 0), goal=Position(0, 0, 0)):
        self.children = []
        self.parent = parent
        self.position = position
        self.grid = grid
        self.dist = 0
        self.rating = 0
        if parent:
            self.path = parent.path[:]
            self.path.append(position)
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
        self.rating = self.dist + self.position.getDist(self.start)

    def createChildren(self, visited_list):
        if not self.children:
            direct_children = []
            direct_children.append(StatePosition(self.grid,
                                                 self.position + Position(1, 0, 0),
                                                 self,
                                                 self.start,
                                                 self.goal))

            direct_children.append(StatePosition(self.grid,
                                                 self.position + Position(-1, 0, 0),
                                                 self,
                                                 self.start,
                                                 self.goal))

            direct_children.append(StatePosition(self.grid,
                                                 self.position + Position(0, 1, 0),
                                                 self,
                                                 self.start,
                                                 self.goal))

            direct_children.append(StatePosition(self.grid,
                                                 self.position + Position(0, -1, 0),
                                                 self,
                                                 self.start,
                                                 self.goal))

            direct_children.append(StatePosition(self.grid,
                                                 self.position + Position(0, 0, 1),
                                                 self,
                                                 self.start,
                                                 self.goal))

            direct_children.append(StatePosition(self.grid,
                                                 self.position + Position(0, 0, -1),
                                                 self,
                                                 self.start,
                                                 self.goal))

            # check if the position of the direct child is available
            for child in direct_children:
                if child.dist == 0:
                    self.children.append(child)
                else:
                    if not child.position.inList(self.grid.walls):
                        if not child.position.inList(visited_list):
                            if not child.position.inList(self.grid.gates):
                                self.children.append(child)
            # print self.children


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
            return None

        # return the path that was found
        return self.path

def create_print(filename):
    """"
    takes a string as argument that holds the path to a csv file
    copies the contents of the csv file into a list of position classes
    """
    file = open(filename, 'rb')
    outputlist = []
    csvfile = csv.reader(file)
    for row in csvfile:
        if row[0] != 'ID':
            outputlist.append(Position(int(row[1]), int(row[2]), int(row[3])))
    file.close()
    return outputlist

def create_netlist(filename):
    """"
    takes a string as argument that holds the path to a csv file
    copies the contents of the csv file into a list of tuples
    the tuples map to positions in a list made by create_print
    """
    file = open(filename, 'rb')
    csvfile = csv.reader(file)
    netlist = []
    for row in csvfile:
        netlist.append((int(row[0]), int(row[1])))
    file.close()
    return netlist

##====================
## MAIN

print 'running...'
print

# initialize board
gates = create_print('print1.csv')
netlist = create_netlist('netlist1.csv')
grid = Grid(gates, 17, 12)

# total length necessary to connect gates
total_length = 0

# list of all found paths
all_paths = []

count = 1

# run A-Star solver on entire board
for connection in netlist:

    # initialize solver
    a = AStar_Solver(grid, gates[connection[0]], gates[connection[1]])

    # if no solution was found for current path, stop
    if not a.Solve():
        break

    # log progress
    print 'number of paths found: ', count, '/', len(netlist)

    # add found path to list of paths
    all_paths.append(a.path)

    # add found path to list of walls
    grid.walls += a.path

    # change total length of paths
    total_length += len(a.path) - 1

    count += 1


# print out results
count = 1
for path in all_paths:

    # print length of individual paths
    print 'length of path #', count, ': ', len(path) - 1

    # print positions in individual paths
    for position in path:
        print position.x, position.y, position.z
    count += 1

# print total length
print 'The total length is: ', total_length

print
print 'done.'
