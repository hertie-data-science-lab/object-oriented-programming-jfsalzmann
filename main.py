# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 18:05:41 2023

@author: Hannah
"""

from River import River

river = River(5)
river.initialize()
river.display()

river.next_time_step(10)