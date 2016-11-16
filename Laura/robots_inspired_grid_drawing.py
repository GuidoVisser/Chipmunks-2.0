# -*- coding: utf-8 -*-
"""
Created on Fri Nov 04 15:04:31 2016

@author: Laura
object: grid drawing
"""
import math
import time
import numpy

from Tkinter import *

class GridVisualization:
    def __init__(self, width, height):
        "Initializes a visualization with the specified parameters."
        self.max_dim = max(width, height)
        self.width = width
        self.height = height

        # Initialize a drawing surface
        self.master = Tk()
        self.w = Canvas(self.master, width=500, height=500)
        self.w.pack()
        self.master.update()

        # Draw a backing and lines
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(width, height)
        self.w.create_rectangle(x1, y1, x2, y2, fill = "white")

        # Draw gridlines
        # Vertical lines
        for i in range(width + 1):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, height)
            self.w.create_line(x1, y1, x2, y2)
        # Horizontal lines
        for i in range(height + 1):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(width, i)
            self.w.create_line(x1, y1, x2, y2)

    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
                250 + 450 * ((self.height / 2.0 - y) / self.max_dim))

    def done(self):
        "Indicate that the animation is done so that we allow the user to close the window."
        mainloop()

netlist_1 = numpy.array([[23, 4], [5, 7]])
       
anim = GridVisualization(17, 12)
anim.done()
