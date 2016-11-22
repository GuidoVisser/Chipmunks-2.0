import numpy as np


def MakeBoard2D():
    # width and height specify the dimensions
    # np.zeros fills the specified matrix with zero's on all points
    width = 9
    height = 8
    board = np.zeros((height+1,width+1))
    board[2][2] = 1
    board[2][7] = 2
    board[3][5] = 3
    board[5][7] = 4
    board[6][4] = 5
    # print(np.matrix(board))
    return board

# MakeBoard2D()

def LocationChip(chip):
    board = MakeBoard2D()
    if chip in board:
        # np.where function takes value of chip and returns its index
        a = np.where(board == chip)
        y = a[0]
        x = a[1]
    return [y[0]][x[0]]




# def LocationChipX(chip):
#     board = MakeBoard2D()
#     if chip in board:
#         a = np.where(board == 2)
#         x = a[1]
#     return x[0]
# LocationChip()

# DistanceChips returns the distance between two chips in a grid

def DistanceChips(chip1,chip2):
    (x1,y1) = LocationChip(chip1)
    (x2,y2) = LocationChip(chip2)
    print abs(x1 - x2) + abs(y2-y1)

# DistanceChips(1,4)

def DistanceY(chip1, chip2):
    (x1,y1) = LocationChip(chip1)
    (x2,y2) = LocationChip(chip2)
    return abs(y1-y2)



def MakeLine(chip1, chip2):
    Line = []
    board = MakeBoard2D()
    while(DistanceY(LocationChip(chip1),LocationChip(chip2)) != 0):


    # MoveX()

# def MoveX():
#     board = MakeBoard2D()
#     x = 2
#     y = 2
#     x += 1

def MoveY(board[x][y]):
    board[x] = 0
    board[y] += 1
    print board[x][y]
    return board[x][y]




