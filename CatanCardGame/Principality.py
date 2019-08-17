from __future__ import annotations

import unittest

import Tags

import random

import json

from Slot import Slot, TownSlot, RoadSlot, ExpansionSlot, ResourceSlot

from Player import Player, RandomPlayer

from Piece import Piece, Town, Road, Expansion, Resource


class Principality:
  #Takes in the player, game, the list of starting resources clockwise
  #Actions is a dictionary of actions, keys as the action, and it's phases
  def __init__(self, game, player, checkPlayer, resourceList):
    """This is a player's own personal game

    The principality starts out by having the coordinates initiated and the 
    empty slots placed in the correct places. 

    Args:
      game (Game) game that contains the game
      player (Player) Player agent that makes decisions
      checkPlayer (Player) agent that is able to determine what actions are possible
      resourceList (list) list of resources
    """

    self.game = game

    self.coordinates = [[None for _ in range(Tags.NUMCOLUMNS)] for _ in range(Tags.NUMLAYERS)]


    #For slots we use coordinates, making sure it's properly set. 
    for j in range(Tags.NUMCOLUMNS):
      #You're always gonna have expansion slot on the top and bottom layers
      self.coordinates[Tags.TOPCITYLEVEL][j] = \
          ExpansionSlot(self, (Tags.TOPCITYLEVEL, j))
      self.coordinates[Tags.BOTTOMCITYLEVEL][j] = \
          ExpansionSlot(self, (Tags.BOTTOMCITYLEVEL, j))
      #If it's even it's a road slice
      if j % 2 == 0:
        self.coordinates[Tags.TOPRESOURCELEVEL][j] = \
          ResourceSlot(self, (Tags.TOPRESOURCELEVEL, j))
        self.coordinates[Tags.TOWNLEVEL][j] = RoadSlot(self, (Tags.TOWNLEVEL, j))
        self.coordinates[Tags.BOTTOMRESOURCELEVEL][j] = \
          ResourceSlot(self, (Tags.BOTTOMRESOURCELEVEL, j))
      #Otherwise it's a settlement slice
      else:
        self.coordinates[Tags.TOPRESOURCELEVEL][j] = \
          ExpansionSlot(self, (Tags.TOPRESOURCELEVEL, j))
        self.coordinates[Tags.TOWNLEVEL][j] = TownSlot(self, (Tags.TOWNLEVEL, j))
        self.coordinates[Tags.BOTTOMRESOURCELEVEL][j] = \
          ExpansionSlot(self, (Tags.BOTTOMRESOURCELEVEL, j))
        



    #Now our grid that contains everything should have it. 

    self.tokens = []
    self.handCards = []
    self.player = player
    self.checkPlayer = checkPlayer

    player.princ = self
    player.game = game

    checkPlayer.princ = self
    checkPlayer.game = game

    #Create initial road
    self.coordinates[Tags.TOWNLEVEL][Tags.CENTERPOST].setItem(Road(self))

    #Create the left settlement
    leftTownSlot = self.coordinates[Tags.TOWNLEVEL][Tags.CENTERPOST - 1]
    leftTownSlot.initiate(self, resourceList[0], resourceList[1], resourceList[4],\
      resourceList[5])

    #Create the right settlement
    rightTownSlot = self.coordinates[Tags.TOWNLEVEL][Tags.CENTERPOST + 1]
    rightTownSlot.expand(self, resourceList[2], resourceList[3])

    self.leftMostSlotNumber = Tags.CENTERPOST - 1
    self.rightMostSlotNumber = Tags.CENTERPOST + 1

  def __repr__(self) -> str:
    retString = ""
    for layer in range(Tags.NUMLAYERS):
      for slot in range(Tags.NUMCOLUMNS):
        retString += " {0} ".format(self.coordinates[layer][slot])
      retString += "\n\n"
    return retString

  def display(self):
    """Returns info to display the game

    Returns:
      string of the player who controls the principality
      int of victory points
      list that represent all of the locations for the principality
    """
    return self.player, self.getPoints(), self.coordinates

  def getInfo(self) -> list:
    """Returns the information of the game into a JSON readable format

    The information of the dictionary should be enough information to recreate the 
    principality from scratch. What is added is a list of information. First is all 
    elements and their information.

    Returns:
      list information in a list format
    """

    #First create list to be the size of coordinates

    #Calls the encode which encodes the slot as a dictionary
    return [[slot.encode() for slot in layer] for layer in self.coordinates]

  #Returns all locations where a roadslot can be built
  def getPhantomRoadSlots(self) -> list:
    """Returns all open road slots

    Called when you need to get all places where the player could currently
    build a road

    Returns:
      list where a Road can be built
    """

    roadSlots = []
    if self.leftMostSlotNumber % 2 != 0:
      roadSlots.append(self.coordinates[Tags.TOWNLEVEL][self.leftMostSlotNumber - 1])
    if self.rightMostSlotNumber % 2 != 0:
      roadSlots.append(self.coordinates[Tags.TOWNLEVEL][self.rightMostSlotNumber + 1])

    return roadSlots

  def getRoadSlots(self) -> list:
    """Returns all the road slots

    Called when you need to get all the slots with roads currently 
    in the principality

    Returns:
      list where a Road is built
    """

    roadSlots = []
    for i in range(self.leftMostSlotNumber, self.rightMostSlotNumber + 1):
      if i % 2 == 0:
        roadSlots.append(self.coordinates[Tags.TOWNLEVEL][i])
    return roadSlots

  def getPhantomTownSlots(self) -> list:
    """Gets all slots where a Town can be built

    Returns:
      list where a Town can be built
    """

    townSlots = []
    if self.leftMostSlotNumber % 2 == 0 and self.leftMostSlotNumber != 0:
      townSlots.append(self.coordinates[Tags.TOWNLEVEL][self.leftMostSlotNumber - 1])
    if self.rightMostSlotNumber % 2 == 0 and self.rightMostSlotNumber != Tags.NUMCOLUMNS - 1:
      townSlots.append(self.coordinates[Tags.TOWNLEVEL][self.rightMostSlotNumber + 1])

    return townSlots

  def getTownSlots(self) -> list:
    """Gets all Towns in the Pricnipality

    Returns:
      list where a Town is built
    """

    townSlots = []
    for i in range(self.leftMostSlotNumber, self.rightMostSlotNumber + 1):
      if i % 2 != 0:
        townSlots.append(self.coordinates[Tags.TOWNLEVEL][i])
    return townSlots

  def getSettlementSlots(self) -> list:
    """Gets all Settlements in the Principality

    Returns:
      list where a Settlement is built
    """

    return [i for i in self.getTownSlots() if i.item.townType == Tags.SETTLEMENT]

  def getCitySlots(self) -> list:
    """Gets all Cities in the Principality

    Returns:
      list where a City is built
    """

    return [i for i in self.getTownSlots() if i.item.townType == Tags.CITY]
  
  def getALLExpansionSlots(self) -> list:
    """Gets all Expansions in the Principality

    Returns:
      list of expansion, either built in or empty
    """

    expansionSlots = []
    for i in range(self.leftMostSlotNumber, self.rightMostSlotNumber + 1):
      if i % 2 != 0:
        #Know if we want to add the city slots
        if self.coordinates[Tags.TOWNLEVEL][i].item.townType == Tags.CITY:
          expansionSlots.append(self.coordinates[Tags.TOPCITYLEVEL][i])
          expansionSlots.append(self.coordinates[Tags.BOTTOMCITYLEVEL][i])

        expansionSlots.append(self.coordinates[Tags.TOPRESOURCELEVEL][i])
        expansionSlots.append(self.coordinates[Tags.BOTTOMRESOURCELEVEL][i])
    return expansionSlots

  def getPhantomTownExpansionSlots(self) -> list:
    """Gets all slots where a town expansion can be built

    Returns:
      list where town expansions can be built
    """

    return [i for i in self.getALLExpansionSlots() if i.item == None]

  def getPhantomCityExpansionSlots(self) -> list:
    """Gets all Slots where a city expansion can be built

    Returns:
      list where city expansions can be built
    """

    return [i for i in self.getALLExpansionSlots() if i.item == None and i.townSlot.item.townType == Tags.CITY]

  def getTownexpansionSlots(self) -> list:
    """Gets all Slots where an expansion has been built in a town

    Returns:
      list in a town with a built expansion
    """

    return [i for i in self.getALLExpansionSlots() if i.item != None and i.townSlot.item.townType == Tags.SETTLEMENT]

  def getCityexpansionSlots(self) -> list:
    """Gets all Slots where an expansion has been built in a city

    Returns
      list in a city with a built expansion
    """
    return [i for i in self.getALLExpansionSlots() if i.item != None and i.townSlot.item.townType == Tags.CITY]

  def getResourceSlots(self) -> list:
    """Returns an unordered list of all resource slots 

    Returns:
      list containing resources
    """

    rescList = []
    for i in range(self.leftMostSlotNumber, self.rightMostSlotNumber + 1):
      if i % 2 == 0:
        rescList.append(self.coordinates[Tags.TOPRESOURCELEVEL][i])
        rescList.append(self.coordinates[Tags.BOTTOMRESOURCELEVEL][i])

    if self.leftMostSlotNumber % 2 != 0:
      rescList.append(self.coordinates[Tags.TOPRESOURCELEVEL][self.leftMostSlotNumber - 1])
      rescList.append(self.coordinates[Tags.BOTTOMRESOURCELEVEL][self.leftMostSlotNumber - 1])
    if self.rightMostSlotNumber % 2 != 0:
      rescList.append(self.coordinates[Tags.TOPRESOURCELEVEL][self.rightMostSlotNumber + 1])
      rescList.append(self.coordinates[Tags.BOTTOMRESOURCELEVEL][self.rightMostSlotNumber + 1])

    return rescList

  def getResourceSlotsOf(self, rescType) -> list:
    """Gets all Slots of a given type of resource

    Returns:
      list of given resource
    """

    return [i for i in self.getResourceSlots() if i.item.resource == rescType]

  #This returns a list of all resource slots with resource that's greater than zero 
  def getHaveResources(self) -> list:
    """Gets all Slots with resource value greater than 0
      
    Returns:
      list of resource greater than 0
    """

    return [i.item.resource for i in self.getResourceSlots() if i.item.amount > 0]

  #This returns a list of all resources that you can actively take on more of
  def getOpenResources(self) -> list:
    """Gets all Slots with resource value less than 3
      
    Returns:
      list of resource less than 3
    """

    return [i.item.resource for i in self.getResourceSlots() if i.item.amount < 3]

  #Get the strength score of the principality
  def getStrength(self) -> int:
    """Gets the strength value of the principality

    Returns:
      int value of the principality
    """

    return sum([i.getStrength() for i in self.getTownexpansionSlots()])

  #Gets the tournament score of the principality
  def getTourney(self) -> int:
    """Gets the tournament value of the principalicty

    Returns:
      int value of the principality
    """

    return sum([i.getTourney() for i in self.getTownexpansionSlots()])

  #Get the commerce of the principality
  def getCommerce(self) -> int:
    """Gets the commerce value of the principality

    Returns:
      int value of the principality
    """

    return sum([i.getCommerce() for i in self.getTownexpansionSlots()])

  def getPoints(self) -> int:
    """Gets the victory point value of the principality

    Returns:
      int point value of the principality
    """

    return len(self.getSettlementSlots()) + (3 * len(self.getCitySlots()))

  #Given a list of list of resource slots, we spend them
  def spendResources(self, rescList):
    """Spends the resource from the resource List

    Given a set of resource slots, it goes through each slot
    and spends the resource according to the resources
    spend function

    Args:
      rescList (list) of lists with organized slot format
    """

    for rescType in rescList:
      for rescSlot in rescType:
        rescSlot.item.spendResc()

  def giveResources(self, rescList):
    """Gives the resources to the slots in the resource list

    Given a set of resource slots, it goes through each slot
    and gives the resource according to the resources
    give function

    Args:
      rescList (list) of lists with organized slot format
    """

    for rescType in rescList:
      for rescSlot in rescType:
        rescSlot.item.giveResc()

  def rollResources(self, roll):
    """Dictates what should happen when a number is rolled

    Currently just calls rollResc function on all resource slots
    """

    for resourceSlot in self.getResourceSlots():
      resourceSlot.item.rollResc(roll)

  #Converts info an a resource blueprint into a resource
  def convertResource(self, info) -> Resource:
    """Converts a blueprint into a resource

    A blueprint is a tuple containing the number and the type, 
    converts it into a resource object

    Args:
      info (tuple) to make a resource

    Returns:
      Resource created resource
    """

    return Resource(self, info[0], 0, info[1])


  def getResourceCombos(self, resourceList) -> list:
    """Gets the combos of resources list

    Given values of resources, we return the combos of those resources

    Args:
      resourceList (list) of ints signialing how much of each
        resource that we need

    Returns:
      list of all combination
    """
    #We first get all of our resource tiles
    resourceSlots = self.getResourceSlots()


    listings = [[] for _ in range(Tags.NUMRESOURCES)]

    resourceCombos = [[] for _ in range(Tags.NUMRESOURCES)]
      
    for resource in resourceSlots:
      for i in range(Tags.NUMRESOURCES):
        if resource.item.resource == Tags.RESCOURCELIST[i]:
          listings[i].append(resource)

    for i in range(Tags.NUMRESOURCES):
      resourceCombos[i] = self.getSingleResourceCombination(resourceList[i], listings[i])

    #We return all possibilities now. 
    return self.getCombos(resourceCombos)

  #Takes in a list of list resources of list combos
  def getCombos(self, listings, start=0):
    total = []
    

    cur = listings[start]

    #check if we are at the end
    if len(listings) == start + 1:
      for curCombo in cur:
        total.append([curCombo])
    else:
      prevs = self.getCombos(listings, start + 1)
      for combo in prevs:
        for curCombo in cur:
          #Create a new list
          temp = [i for i in combo]
          temp.append(curCombo)

          total.append(temp)


    return total

  def getSingleResourceCombination(self, totAmount, resourceSlots, start=0):
    #Take a single resource out of the list, return either zero, one, two, three

    #Base is when it turns out of tiles and there aren't enough resources
    #Or when the resource cap is reached. 

    slotsUsed = []  
    
    curSlot = resourceSlots[start]

    start += 1

    amountLeft = sum([i.item.amount for i in resourceSlots[start:]])

    #Go through the amount we can give to our pool
    for curAmount in range(curSlot.item.amount + 1):
      #If we would have too much
      if curAmount > totAmount:
        break
      #Check if exact, if exact, you break at the end of this. 
      elif curAmount == totAmount:
        slotsUsed.append([curSlot for _ in range(curAmount)])
        break
      #Check if we would have enough down the line
      elif amountLeft + curAmount >= totAmount:
        recurse = self.getSingleResourceCombination\
          (totAmount - curAmount, resourceSlots, start)

        #Append number of this slot per each element in recurse
        for element in recurse:
          for _ in range(curAmount):
            element.append(curSlot)
          slotsUsed.append(element)

        
            
    return slotsUsed


if __name__ == '__main__':
    unittest.main()

