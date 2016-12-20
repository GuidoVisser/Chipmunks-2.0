""""
A-Star algorithm - Returns shortest possible route, accounting for walls, gates,
(grand)children of gates and other paths. X- Y- and Z-moves are random at the moment.
"""
import csv
from Queue import PriorityQueue

class Position(object):
    """
    a Position object represents a location in three-dimensional space
    """
    def __init__(self, x=0, y=0, z=0):
        """
        initializes a position with coordinates (x, y, z).
        """
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        """
        specifies addition of x + y + z
        """
        new = Position()
        new.x = self.x + other.x
        new.y = self.y + other.y
        new.z = self.z + other.z
        return new

    def getDist(self, other):
        """"
        returns the distance between goal (other) and itself.
        """
        x = abs(self.x - other.x)
        y = abs(self.y - other.y)
        z = abs(self.z - other.z)
        return x + y + z

    def inList(self, list):
        """"
        check if self position is in a list of positions
        """
        for pos in list:
            if pos.x == self.x:
                if pos.y == self.y:
                    if pos.z == self.z:
                        return True
        return False

    def adjacent(self):
        """
        create Position object for children of self and add to adjacent array
        """
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
    grid of points that are either a wall, a gate, (grand)children of gates or free space
    """
    def __init__(self, gates, max_x, max_y, max_z = 7):
        self.gates = gates
        self.walls = []
        self.gates_children = []
        self.gates_grandchildren = []
        #self.gates_grand_grandchildren = []

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

        # create children and grandchildren for gates without overlap
        for gate in gates:
            self.gates_children += gate.adjacent()
        for child in self.gates_children:
            grandchildren = child.adjacent()
            for grandchild in grandchildren:
                if not grandchild.inList(self.gates_grandchildren):
                    self.gates_grandchildren.append(grandchild)
        """
        for child in self.gates_grandchildren:
            grand_grandchildren = child.adjacent()
            for grand_grandchild in grand_grandchildren:
                if not grand_grandchild.inList(self.gates_grand_grandchildren):
                    self.gates_grand_grandchildren.append(grand_grandchild)
        """

class State(object):
    """
    State object for the grid with start-, current- and endposition, parent of child,
    cost variables of distance to goal, extra static and dynamic cost, all resulting
    in rating for child. Update path with every move.
    """
    def __init__(self, grid, position, parent,
                 start=Position(0, 0, 0), goal=Position(0, 0, 0)):
        self.children = []
        self.parent = parent
        self.position = position
        self.grid = grid
        self.dist = 0
        self.cost = 0
        self.rating = 0
        if parent:
            self.path = parent.path[:]
            self.cost = parent.cost
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
    """
    Super State object. Create children and define child rating by distance,
    static and dynamic cost. If goal found, break.
    """
    def __init__(self, grid, position, parent,
                 start=Position(0, 0, 0), goal=Position(0, 0, 0)):
        super(StatePosition, self).__init__(grid, position, parent, start, goal)

        # distance to goal
        self.dist = self.position.getDist(self.goal)

    def createChildren(self, visited_list, children_list):
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
                            visited_list) and not child.position.inList(self.grid.gates) and not child.position.inList(children_list):

                        for pos in self.grid.gates_children:
                            if pos.x == child.position.x:
                                if pos.y == child.position.y:
                                    if pos.z == child.position.z:
                                        child.cost += 21

                        for pos in self.grid.gates_grandchildren:
                            if pos.x == child.position.x:
                                if pos.y == child.position.y:
                                    if pos.z == child.position.z:
                                        child.cost += 1
                        """
                        for pos in self.grid.gates_grand_grandchildren:
                            if pos.x == child.position.x:
                                if pos.y == child.position.y:
                                    if pos.z == child.position.z:
                                        child.cost += 1
                        """
                        child.cost += 10
                        child.rating = child.dist * 10 + child.cost
                        self.children.append(child)

class AStar_Solver:
    def __init__(self, grid, start, goal):
        """"
        Keep track of path, visited positions (drawn lines), priority move.
        """
        self.path = []
        self.visited = []
        self.positions_children = []
        self.priorityQueue = PriorityQueue()
        self.start = start
        self.goal = goal
        self.grid = grid

    def Solve(self):
        """
        Returns path if found,
        """
        # initialize starting point (position to start, parent to 0)
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
            closestChild.createChildren(self.visited, self.positions_children)

            # add the closest child to the visited list
            self.visited.append(closestChild.position)

            # check for all children if it is already in children
            for child in closestChild.children:

                # check if child is goal
                if child.dist == 0:
                    self.path = child.path
                    break

                # add child to children list
                self.positions_children.append(child.position)
                self.priorityQueue.put((child.rating, child))

        # return found path if found
        if len(self.path) == 0:
            return None
        else:
            return self.path

def create_print(filename):
    """"
    takes a string as argument that holds the path to a csv file
    copies the contents of the csv file into a list of Position objects
    """
    with open(filename, 'rb') as printfile:
        # check files extension
        if not filename.endswith('.csv'):
           raise TypeError('File is not a .csv file')

        # add coordinates in file to list
        gateslist = []
        csvfile = csv.DictReader(printfile)
        for row in csvfile:
            gateslist.append(Position(int(row['x']), int(row['y']), int(row['z'])))

    printfile.close()

    # return list of positions
    return gateslist


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