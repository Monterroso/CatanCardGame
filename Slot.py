from __future__ import annotations

import unittest

import Tags

import random

import json

from Piece import Piece, Town, Road, Expansion, Resource


#############################################################################
################################### Slots ###################################
#############################################################################

#A slot holds info for the type it holds, and a pointer to what it holds. 
class Slot:
  """ Used to hold game objects
  
  Every object is held within a slot, and it's assume all possible coordinates 
  to be used will have a slot within them, and can have things directly placed 
  within them.
  """

  def __init__(self, princ, item, location):
    self.princ = princ

    #Append to the location of the principality. 
    princ.coordinates[location[0]][location[1]] = self

    self.location = location

    self.item = item    

  def __repr__(self):
    if self.item == None:
      return "N/A"
    else:
      return str(self.item)

  #Returns a dictionary of all elements of this slot
  def encode(self):
    pass

  def changeLocation(self, location):
    self.location = location

  def setItem(self, item):
    self.item = item
    item.slot = self

  def unsetItem(self):
    temp = self.item
    self.item = None
    item.slot = None
    return temp

class TownSlot(Slot):
  name = 0
  def __init__(self, princ, location):
    super().__init__(princ, None, location)

    self.name = TownSlot.name
    TownSlot.name += 1

  def encode(self):
    if self.item == None:
      return {}
    return {"Type":self.item.townType}


  def getTL(self):
    return self.princ.coordinates[Tags.TOPRESOURCELEVEL][self.location[1] - 1]

  def getTR(self):
    return self.princ.coordinates[Tags.TOPRESOURCELEVEL][self.location[1] + 1]

  def getBR(self):
    return self.princ.coordinates[Tags.BOTTOMRESOURCELEVEL][self.location[1] + 1]

  def getBL(self):
    return self.princ.coordinates[Tags.BOTTOMRESOURCELEVEL][self.location[1] - 1]

  def getLeftRoadSlot(self):
    return self.princ.coordinates[Tags.TOWNLEVEL][self.location[1] - 1]

  def getRightRoadSlot(self):
    return self.princ.coordinates[Tags.TOWNLEVEL][self.location[1] + 1]

  def getTopSlot1(self):
    return self.princ.coordinates[Tags.TOPRESOURCELEVEL][self.location[1]]

  def getTopSlot2(self):
    return self.princ.coordinates[Tags.TOPCITYLEVEL][self.location[1]]

  def getBottomSlot1(self):
    return self.princ.coordinates[Tags.BOTTOMRESOURCELEVEL][self.location[1]]

  def getBottomSlot2(self):
    return self.princ.coordinates[Tags.BOTTOMCITYLEVEL][self.location[1]]

  def expand(self, princ, Top, Bottom):
    """If we build a settlement, we set the resources

    Top and Bottom are the resources that are to be added
    to the free locations of this settlement, either to the right
    or to the left, by default it goes right if both are free.

    Args:
      princ (Principality): The principality that will be expanding
      Top (Resource): The resource we want to add to the top slot
      Bottom (Resource): The resource we want to add to the bottom slot
    """

    #Check the slots of the road which side it is on. 
    if self.getRightRoadSlot().item != None:
      self.getTL().setItem(princ.convertResource(Top))
      self.getBL().setItem(princ.convertResource(Bottom))
    else:
      self.getTR().setItem(princ.convertResource(Top))
      self.getBR().setItem(princ.convertResource(Bottom))

    #we want to pair the town and create it
    town = Town(princ, Tags.SETTLEMENT)
    self.setItem(town)

  def initiate(self, princ, TL, TR, BR, BL):
    
    #Link the resources
    self.getTL().setItem(princ.convertResource(TL))
    self.getBL().setItem(princ.convertResource(BL))
    self.getTR().setItem(princ.convertResource(TR))
    self.getBR().setItem(princ.convertResource(BR))

    #we want to pair the town and create it
    town = Town(princ, Tags.SETTLEMENT)
    self.setItem(town)

  def getTownRoadSlots(self):
    return [self.getLeftRoadSlot(), self.getRightRoadSlot()]

  def getTownExpansionSlots(self):
    return [self.getTopSlot1(), self.getTopSlot2(), self.getBottomSlot1(), self.getBottomSlot2()]

  def getTownResourceSlots(self):
    rescSlot = []

    rescSlot.append(self.getTL())
    rescSlot.append(self.getBL())
    rescSlot.append(self.getTR())
    rescSlot.append(self.getBR())

    return rescSlot

class RoadSlot(Slot):
  name = 0
  def __init__(self, princ, location):
    super().__init__(princ, None, location)

    self.name = RoadSlot.name
    RoadSlot.name += 1

  def encode(self):
    if self.item == None:
      return {}
    return {"Type":Tags.ROAD}

  def getLeftSettlementSlot(self):
    return princ.coordinates[Tags.TOWNLEVEL][self.location[1] - 1]

  def getRightSettlementSlot(self):
    return princ.coordinates[Tags.TOWNLEVEL][self.location[1] + 1]

class ExpansionSlot(Slot):
  name = 0
  def __init__(self, princ, location):
    super().__init__(princ, None, location)

    self.name = ExpansionSlot.name
    ExpansionSlot.name += 1

  def encode(self):
    if self.item == None:
      return {}
    return {"Type":self.item.name}

  def getTownSlot(self):
    return princ.coordinates[Tags.TOWNLEVEL][self.location[1]]
    

class ResourceSlot(Slot):
  name = 0
  def __init__(self, princ, location):
    super().__init__(princ, None, location)

    self.name = ResourceSlot.name
    ResourceSlot.name += 1

  def encode(self):
    if self.item == None:
      return {}
    return {"Type":Tags.RESOURCENAME[self.item.resource], "Amount":self.item.amount, "Number":self.item.number}

  def getLeftTownSlot(self):
    return princ.coordinates[Tags.TOWNLEVEL][self.location[1] - 1]

  def getRightTownSlot(self):
    return princ.coordinates[Tags.TOWNLEVEL][self.location[1] + 1]


if __name__ == '__main__':
    unittest.main()

