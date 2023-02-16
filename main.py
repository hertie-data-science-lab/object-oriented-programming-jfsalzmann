# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 2023
@author: Johann-Friedrich Salzmann
"""

from River import River
from Creatures import Bear
from Creatures import Fish

# Create a River of size 20 with 2 Bears and 2 Fishes
river = River(20)
river.initialize([Bear(),Bear(),Fish(),Fish()])
river.display()

# Have 5 rounds of 10 simulation steps
for i in range(5):
    river.next_time_step(10)
    river.display()