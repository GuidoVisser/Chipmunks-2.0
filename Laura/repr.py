# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 10:56:27 2016

@author: Floris
"""

import numpy as np

# Representing the grid for our Chips n Circuits problem.
# Lists are the way to go I think. You can make a 3D matrix by using
# three times the bracket notation, e.g. board = [x][y][z]
# For now I made just the board with chips in 2D.
#  The grid is navigated through indices of the lists where [0,0] is the top left point
# and [17,12] is the most down-right point.

def MakeBoard2D():
    # width and height specify the dimensions
    # np.zeros fills the specified matrix with zero's on all points
    width = 17
    height = 12
    board = np.zeros((height, width))
    # these are all the chips for print#1
    board[1][1] = 1
    board[1][6] = 2
    board[1][10] = 3
    board[1][15] = 4
    board[2][3] = 5
    board[2][12] = 6
    board[2][14] = 7
    board[3][12] = 8
    board[4][8] = 9
    board[5][1] = 10
    board[5][4] = 11
    board[5][11] = 12
    board[5][16] = 13
    board[7][13] = 14
    board[7][16] = 15
    board[8][2] = 16
    board[8][6] = 17
    board[8][9] = 18
    board[8][11] = 19
    board[8][15] = 20
    board[9][1] = 21
    board[10][2] = 22
    board[10][9] = 23
    board[11][1] = 24
    board[11][12] = 25
    print board

MakeBoard2D()