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


    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z


# class GridPosition(Position):
#     """"
#     Position on the grid
#     """
#     def __init__(self, x=0, y=0, z=0, isWall = False, isGate = False):
#         super(GridPosition, self).__init__(x, y, z)
#         self.isWall = isWall
#         self.isGate = isGate


class Grid(object):
    """"
    Grid of points that are either a wall, a gate or free space
    """
    def __init__(self, max_x, max_y, max_z = 7):
        self.walls = []
        for x in range(-1, max_x + 1):
            for y in range(-1, max_y + 1):
                self.walls.append(Position(x, y, -1))
                self.walls.append(Position(x, y, max_z))
        for x in range(-1, max_x + 1):
            for z in range(0, max_z):
                self.walls.append(Position(x, -1, z))
                self.walls.append(Position(x, max_y, z))
        for y in range(0, max_y):
            for z in range(0, max_z):
                self.walls.append(Position(-1, y, z))
                self.walls.append(Position(max_x, y, z))

class State(object):
    def __init__(self, grid, position, parent,
                 start=Position(0, 0, 0), goal=Position(0, 0, 0)):
        self.children = []
        self.parent = parent
        self.position = position
        self.grid = grid
        self.dist = 0
        if parent:
            self.path = parent.path[:]
            self.path.append(position)
            self.start = parent.start
            self.goal = parent.goal
        else:
            self.path = [position]
            self.start = start
            self.goal = goal

    def getDist(self):
        pass

    def createChildren(self):
        pass


class StatePosition(State):
    def __init__(self, grid, position, parent,
                 start=Position(0, 0, 0), goal=Position(0, 0, 0)):
        super(StatePosition, self).__init__(grid, position, parent, start, goal)
        self.dist = self.getDist()

    def getDist(self):
        """"
        Returns the distance between goal and itself.
        """
        if self.position == self.goal:
            return 0
        distance = self.position.getDist(self.goal)
        return distance

    def createChildren(self):
        if not self.children:
            # Childern in x direction
            direct_children = []
            direct_children.append(StatePosition(grid,
                                   self.position + Position(1, 0, 0),
                                    self,
                                    self.start,
                                    self.goal))

            direct_children.append(StatePosition(grid,
                                   self.position + Position(-1, 0, 0),
                                    self,
                                    self.start,
                                    self.goal))

            direct_children.append(StatePosition(grid,
                                   self.position + Position(0, 1, 0),
                                    self,
                                    self.start,
                                    self.goal))

            direct_children.append(StatePosition(grid,
                                   self.position + Position(0, -1, 0),
                                    self,
                                    self.start,
                                    self.goal))

            direct_children.append(StatePosition(grid,
                                   self.position + Position(0, 0, 1),
                                    self,
                                    self.start,
                                    self.goal))

            direct_children.append(StatePosition(grid,
                                   self.position + Position(0, 0, -1),
                                    self,
                                    self.start,
                                    self.goal))

            for child in direct_children:
                check = False
                for wall in grid.walls:
                    if wall.x == child.position.x:
                        if wall.y == child.position.y:
                            if wall.z == child.position.z:
                                check = True
                                break
                if check == True:
                    direct_children.remove(child)
            self.children += direct_children


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
        startState = StatePosition(grid,
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
            closestChild.createChildren()

            # add the closest child to the visited list
            self.visited.append(closestChild.position)

            # check for all children if it is already in children
            for child in closestChild.children:
                if child.position not in self.visited:

                    # if distance is 0 child is goal
                    if not child.dist:
                        self.path = child.path
                        break

                    # add child to children list
                    self.priorityQueue.put((child.dist, child))

        # if no path was found give error message
        if not self.path:
            "Goal of " + self.goal + " is not possible."

        # return the path that was found
        return self.path

def create_print(filename):
    """"
    takes a string as argument that holds path to a csv file
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
    file = open(filename, 'rb')
    csvfile = csv.reader(file)
    netlist = []
    for row in csvfile:
        netlist.append((int(row[0]), int(row[1])))
    file.close()
    return netlist

##====================
## MAIN

print1 =create_print('print1.csv')
# print2 = create_print('print2.csv')
netlist1 = create_netlist('netlist1.csv')

# print
# print print1[netlist1[0][0]].x, print1[netlist1[0][0]].y, print1[netlist1[0][0]].z
# print print1[netlist1[0][1]].x, print1[netlist1[0][1]].y, print1[netlist1[0][1]].z
# print

# for elem in netlist1:
#     solver = AStar_Solver(print1[int(elem[0])-1], print1[int(elem[1])-1])

pos1 = Position()
pos2 = Position(0,1,1)
print pos1.getDist(pos2)

grid = Grid(17,12,7)

# start1 = print1[netlist1[0][0]]
# goal1 = print1[netlist1[0][1]]
#
# start2 = print1[netlist1[1][0]]
# goal2 = print1[netlist1[1][1]]

print 'running...'

length = 0
all_paths = []
for connection in netlist1:
    a = AStar_Solver(grid, print1[connection[0]], print1[connection[1]])
    a.Solve()
    all_paths.append(a.path)
    grid.walls += a.path
    length += len(a.path) - 1
    all_paths.append(a.path)

print length
for elem in all_paths:
    print elem

print 'done.'
