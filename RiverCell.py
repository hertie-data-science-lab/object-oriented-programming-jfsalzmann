# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 2023
@author: Johann-Friedrich Salzmann
"""

from Creatures import Fish, Bear

class RiverCell:
# Each river cell is implemented as a class instance in order to contain creatures in different process status levels (containing, incoming, outgoing)
            
    def __init__(self,i):
        self.__i = i # cell number in the river
        self.__contains = [] # creatures in the cell
        self.__incoming = [] # creatures about to move into the cell from another
        self.__incoming_cells = {} # incoming creatures' origin cell instance
        self.__outgoing = [] # creatures about to move to another cell from this one
        
    def __str__(self): # string representation for river chart
        return ''.join(str(creature) for creature in self.__contains) if self.__contains else "."

    def add(self, creature): # hard-add a creature to a cell, just used for initial allocation
        if(not self.empty()):
            raise NameError('Trying to double allocate')
        self.__contains.append(creature)
        
    def remove(self,creature): # remove a creature from the cell
        self.__contains.remove(creature)
        
    def incoming(self, creature, cell): # register an incoming creature
        self.__incoming.append(creature)
        self.__incoming_cells[creature] = cell
        
    def remove_incoming(self, creature): # unregister an incoming creature
        self.__incoming.remove(creature)
        self.__incoming_cells.pop(creature)
        
    def admit(self,creature): # admit an incoming creature to the cell
        self.__incoming_cells[creature].letgo(creature) # by finally removing it from the previous one
        self.remove_incoming(creature) # and unregistering it
        if(not self.empty()):
            raise NameError('Trying to double admit')
        self.__contains.append(creature) # and adding it to the cell
        
    def refuse(self,creature): # refuse entrance after mating:
        self.__incoming_cells[creature].rollback(creature) # roll back outgoing status in their previous cell
        self.remove_incoming(creature) # and unregister in this cell
        
    def vanish(self,creature): # let an animal disappear
        self.__incoming_cells[creature].letgo(creature) # by unregistering it both from the previous cell
        self.remove_incoming(creature) # and the current one
        
    def outgoing(self,creature,cell): # register an outgoing creature
        self.__contains.remove(creature)
        self.__outgoing.append(creature)
        cell.incoming(creature,self)
        
    def letgo(self,creature): # similar to admission, but for outstream unregistering
        self.__outgoing.remove(creature)
        
    def rollback(self,creature): # revert outstream move after mating
        self.__outgoing.remove(creature)
        if(not self.empty()):
            raise NameError('Trying to double rollback')
        self.__contains.append(creature)
        
    def empty(self): # cell is empty with regards to finally committed creatures
        return not self.__contains
        
    def let_move(self,river): # let a creature in the cell move
        if(self.empty()):
            return
        creature = self.__contains[0] # in this implementation, there can only be one creature in each cell
        delta = creature.get_location_delta() # relative movement indicator (-1,0,1)
        if delta != 0 and 0 <= self.__i + delta < len(river): # movement destination in range
            self.outgoing(creature,river[self.__i + delta]) # register movement to next cell
            
    def clear(self,river): # clearing function
        
        if not self.__incoming and len(self.__contains) <= 1:
            return False # nobody comin in, nothing changes
        
        if len(self.__incoming) + len(self.__contains) <= 1:
            return False # somebody comin in, enough space, handled when committing (see below)
        
        fishes_c = [creature for creature in self.__contains if isinstance(creature, Fish)] # fishes currently in cell
        fishes_i = [creature for creature in self.__incoming if isinstance(creature, Fish)] # fishes incoming
        fishes = fishes_c + fishes_i # all fishes
        
        bears_c = [creature for creature in self.__contains if isinstance(creature, Bear)] # bears currently in cell
        bears_i = [creature for creature in self.__incoming if isinstance(creature, Bear)] # bears incoming
        bears = bears_c + bears_i # all bears
        
        if(bool(fishes) & bool(bears)): # all fishes are eaten
            for fish in fishes_i: # incoming fishes are vanishing
                self.vanish(fish)
                fishes_i.remove(fish) # removed for mating logic
                fishes.remove(fish)
            for fish in fishes_c: # while fishes currently in cell are removed
                self.remove(fish)
                fishes_c.remove(fish)
                fishes.remove(fish)
                
        if(len(fishes) + len(bears) > 1): # mating going on
            creatures = [Fish() for i in range(len(fishes)-1)] + [Bear() for i in range(len(bears)-1)] # new creatures: assuming n-1 same-type creatures being spawned when n creatures of the same type meet
            river.birth_queue(creatures) # add new creatures to the birth queue
            [self.refuse(creature) for creature in fishes_i + bears_i] # push incoming creatures participating in mating back to their previous cells
            
        return True # some changes in position that require another clearing round
    
    def commit(self,river): # committing function to finalise movements after clearing
        if not self.__incoming and len(self.__contains) <= 1:
            return False # nobody comin in, nothing changes
        
        if len(self.__incoming) + len(self.__contains) <= 1:
            [self.admit(creature) for creature in self.__incoming]
            return True # somebody comin in, enough space, committing
        
        return False # no more cases at this point
