""""
README:
Ik heb de naam 'value' in 'position' veranderd.
start, value, en goal hebben geen 'value' meer, maar zijn een positie object.
De afstand tussen twee posities, in 3D, is delta_x plus delta_y plus delta_z

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




            # for i in xrange(len(self.goal) - 1):
            #     val = self.position
            #     val = val[:i] + val[i+1] + val[i] + val[i+2:]
            #     child = State_Position(val, self)
            #     self.children.append(child)

# class AStar_Solver:
#     def __init__(self, start, goal):
#         self.path = []
#         self.visitedQueue = []
#         self.priorityQueue = PriorityQueue()
#         self.start = start
#         self.goal = goal
#
#     def Solve(self):
#         startState = State_Position(self.start,
#                                   0,
#                                   self.start,
#                                   self.goal)
#         # id-count
#         count = 0
#         self.priorityQueue.put((0, count, startState))
#         while not self.path and self.priorityQueue.qsize():
#             closestChild = self.priorityQueue.get()[2]
#             closestChild.createChildren()
#             self.visitedQueue.append(closestChild.position)
#             for child in closestChild.children:
#                 if child.position not in self.visitedQueue:
#                     count += 1
#                     if not child.dist:
#                         self.path = child.path
#                         break
#                     self.priorityQueue.put((child.dist, count, closestChild))
#         if not self.path:
#             "Goal of " + self.goal + " is not possible."
#         return self.path

