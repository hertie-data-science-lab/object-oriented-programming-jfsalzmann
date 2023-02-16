# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 2023
@author: Johann-Friedrich Salzmann
"""

import numpy as np
import random
from Creatures import Bear
from Creatures import Fish
from RiverCell import RiverCell
        
class River:
# River class maintains both the river cells as a list, and runs the simulation actions on its cells
    
    def __init__(self, n_room):
        self.__n_room = n_room # number of cells
        self.__river = [RiverCell(i) for i in range(self.__n_room)]  # initialize the river list with empty cell objects
        self.__full = False # shows whether empty cells are available, i.e. continuing simulation is meaningful
        self.__new_creatures = [] # list of creatures waiting for birth
        self.__time_steps = 0
    
    def initialize(self, creatures):
        # iterate through the given list of creatures and randomly place them in the river
        for creature in creatures:
            empty = [cell for cell in self.__river if cell.empty()]  # find all empty cells in the river
            if empty:
                random.choice(empty).add(creature) # add it to a random empty cell
            if len(empty) == 1:
                self.__full = True  # set True if there are no empty cells left
                break
            
    def birth_queue(self, creatures):
        self.__new_creatures += creatures
        
    def give_birth(self):
        self.initialize(self.__new_creatures)
        self.__new_creatures = []
    
    def next_time_step(self,time=1):
        for j in range(time): # repeat for n simulation steps
            if self.__full:
                print("No more space. Terminating simulation\n")
                break
            self.__time_steps += 1
            [cell.let_move(self.__river) for cell in self.__river] # move the creatures according to their behavior
            while any([cell.clear(self) for cell in self.__river]):
                pass # clear each cell until nothing's movin anymore
            while any([cell.commit(self) for cell in self.__river]):
                pass # commit final moves after clearing
            self.give_birth() # let new creatures be added to the river for the next time step
   
    def display(self):
        print("Ecosystem after",self.__time_steps,"steps:")
        print("="*self.__n_room)
        print(''.join(str(cell) for cell in self.__river))
        print("="*self.__n_room,"\n")
        