# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 2023
@author: Johann-Friedrich Salzmann, Finn Krueger
"""

from abc import ABCMeta, abstractmethod
import numpy as np
import random

class Creature(metaclass=ABCMeta):
    
    _symbol = "C"
    
    def __init__(self):
        pass
        
    def __str__(self):
        return self._symbol
        
    def get_location_delta(self): # relative movement indicator (-1,0,1)
        return random.randint(-1, 1) 
        
class Bear(Creature): # Bears are Creatures with a specific symbol
    
    def __init__(self): 
        super().__init__()
        self._symbol = "B"
        
class Fish(Creature): # Fishes are Creatures with a specific symbol
    
    def __init__(self): 
        super().__init__()
        self._symbol = "F"
