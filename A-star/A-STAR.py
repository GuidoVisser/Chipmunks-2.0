""""
README:
De afstand tussen twee posities, in 3D, is delta_x plus delta_y plus delta_z

Dit programma rekent het kortste pad uit tussen twee objecten.
Er wordt nog geen regening gehouden met obstakels en de randen van de grid.
Tot nu toe wordt de Position class gebruikt om posities op de grid op te slaan,
maar in de toekomst willen we naar de GridPosition class, omdat we dan simpel kunnen bijhouden welke
punten wel en niet toegankelijk zijn voor volgende paden
"""

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

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z


class GridPosition(Position):
    """"
    Position on the grid
    """
    def __init__(self, x=0, y=0, z=0):
        super(GridPosition, self).__init__(x, y, z)
        isPath = False


class State(object):
    def __init__(self, position, parent,
                 start=Position(0, 0, 0), goal=Position(0, 0, 0)):
        self.children = []
        self.parent = parent
        self.position = position
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
    def __init__(self, position, parent,
                 start=Position(0, 0, 0), goal=Position(0, 0, 0)):
        super(StatePosition, self).__init__(position, parent, start, goal)
        self.dist = self.getDist()

    def getDist(self):
        """"
        Returns the distance between goal and itself.
        """
        if self.position == self.goal:
            return 0
        x = abs(self.position.x - self.goal.x)
        y = abs(self.position.y - self.goal.y)
        z = abs(self.position.z - self.goal.z)
        return x + y + z

    def createChildren(self):
        if not self.children:

            # Childern in x direction
            child1 = StatePosition(self.position + Position(1, 0, 0),
                                    self,
                                    self.start,
                                    self.goal)
            self.children.append(child1)

            child2 = StatePosition(self.position + Position(-1, 0, 0),
                                    self,
                                    self.start,
                                    self.goal)
            self.children.append(child2)

            # children in y direction
            child3 = StatePosition(self.position + Position(0, 1, 0),
                                    self,
                                    self.start,
                                    self.goal)
            self.children.append(child3)

            child4 = StatePosition(self.position + Position(0, -1, 0),
                                    self,
                                    self.start,
                                    self.goal)
            self.children.append(child4)

            # children in z direcion
            child5 = StatePosition(self.position + Position(0, 0, 1),
                                    self,
                                    self.start,
                                    self.goal)
            self.children.append(child5)

            child6 = StatePosition(self.position + Position(0, 0, -1),
                                    self,
                                    self.start,
                                    self.goal)
            self.children.append(child6)


class AStar_Solver:
    def __init__(self, start, goal):
        self.path = []
        self.visited = []
        self.priorityQueue = PriorityQueue()
        self.start = start
        self.goal = goal

    def Solve(self):
        # initialize starting point
        startState = StatePosition(self.start,
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

##====================
## MAIN

start = Position(3,0,1)
goal = Position(1,4,2)
print 'running...'
a = AStar_Solver(start, goal)
a.Solve()
print 'pathlength is: ', len(a.path) - 1
for elem in a.path:
    print elem.x, elem.y, elem.z


