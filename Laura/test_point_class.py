# -*- coding: utf-8 -*-
"""
Created on Fri Nov 04 14:25:47 2016

@author: Laura
"""

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

p1 = Point(0,3)
p2 = Point(1,0)

print p1.x
