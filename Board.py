import unittest

import Tags

from collections import deque

import random

import pdb

#This is a board for python. 

###################################################################################
################################### Game Parts ###################################
###################################################################################

class Player:
  name = 0
  def __init__(self, board, princ):
    self.name = Player.name
    Player.name += 1
    self.board = board

    self.princ = princ

    # self.actionsTaken = []

  def __repr__(self):
    return "{0}".format(self.name)

  #Takes in a string of the conditions just taken, along with the possible actions
  #ValidActions is a dictionary, with slots, then combinations
  #Returns list of name, slot, resources
  def getAction(self, actString, validActions):
    #returns the actionpair, along with an object of additional information. 
    pass

class RandomPlayer(Player):
  def __init__(self, board, princ):
    super().__init__(board, princ)
    

  def getAction(self, actString, validActions):
    #pdb.set_trace()
    #We want to get all valid actions if we can take an action
    actions = [i for i in list(validActions.keys()) if i != Tags.TURNEND and i != Tags.DONOTHING]

    actionToTake = None
    if len(actions) == 0:
      #Check if both have occured
      if len(validActions.keys()) > 1:
        raise Exception("Should not have these together {0}".format(validActions.keys()))
      else:
        actionToTake = list(validActions.keys())[0]
    else:
      actionToTake = random.choice(list(actions))

    # self.actionsTaken.append(actionToTake)

    if len(validActions[actionToTake]) == 0:
      return [actionToTake, []]

    slot = random.choice(validActions[actionToTake][0])
    resources = random.choice(validActions[actionToTake][1])

    return [actionToTake, slot, resources]

class Board:
  def __init__(self, decks, resourceCards, numberofPiles, principalities, firstTurn, actions):
    self.decks = decks
    self.resourceCards = resourceCards
    self.numberofPiles = numberofPiles

    self.principalities = principalities

    self.actions = actions

    self.knightToken = Tags.KTOKEN
    self.commerceToken = Tags.CTOKEN
    
    self.currentTurn = firstTurn

    self.nextProductionRoll = None
    self.nextActionRoll = None

    self.winner = None

    # self.actionsTaken = []
    

  #Checks if a road can be built
  def canBuildRoad(self, princ):
    return len(princ.getPhantomRoadSlots()) != 0

  #Checks if a settlement can be built
  def canBuildSettlement(self, princ):
    return len(princ.getPhantomTownSlots()) != 0

  #Checks if a settlement can be built
  def canBuildCity(self, princ):
    return len(princ.getSettlementSlots()) != 0
    
  #Builds a road at the desired location
  def buildRoad(self, princ, roadSlot):
    road = Road(princ)
    roadSlot.setItem(road)

  #Builds a settlement at the desired location
  def buildSettlement(self, princ, townSlot):
    #pop the two resources
    topRaw = self.resourceCards.pop()
    topSlot = ResourceSlot(princ, None, None) 
    top = Resource(princ, topRaw[0], 0, topRaw[1])
    topSlot.setItem(top)

    bottomRaw = self.resourceCards.pop()
    bottomSlot = ResourceSlot(princ, None, None)
    bottom = Resource(princ, bottomRaw[0], 0, bottomRaw[1])
    bottomSlot.setItem(bottom)

    town = Town(princ, Tags.SETTLEMENT)
    townSlot.expand(princ, topSlot, bottomSlot)

    townSlot.setItem(town)

  #Builds a city at the desired location
  def buildCity(self, princ, townSlot):
    townSlot.item.upgradeSettlement()

  #Builds an expantion at the desired location
  def buildExpansion(self, princ, expansion, expansionSlot):
    expansionSlot.setItem(expansion)

  
  #Checks if some action is in valid actions
  def canPerformAction(self, princ, validActions, actionType, info):
    #Check for the type of action

    #Check if it's a build type action 
    if actionType == Tags.BUILDCITY or actionType == Tags.BUILDROAD or actionType == Tags.BUILDSETTLEMENT:
      #Info now should be a list 
      if actionType in validActions:
        #This should get us a list 
        if info[0] in validActions[actionType][0]:
          if info[0] in validActions[actionType][1]:
            return True
      
    if actionType == Tags.TURNEND:
      return princ.player == princ.board.getCurrentPlayer()

    if actionType == Tags.DONOTHING:
      return princ.player != princ.board.getCurrentPlayer()
    
    return False

  #Performs the action
  def performAction(self, princ, actionObject):
    #Action is name, then slot, then resources
    actionName = actionObject[0]

    # self.actionsTaken[-1].append("Player {0} took {1}".format(player, actionName))

    if actionName == Tags.BUILDROAD or \
      actionName == Tags.BUILDSETTLEMENT or actionName == Tags.BUILDCITY:

      resources = actionObject[2]
      buildSlot = actionObject[1]
      #pdb.set_trace()
      if actionName == Tags.BUILDROAD:
        princ.spendResources(resources)

        princ.buildRoad(princ, buildSlot)  

      elif actionName == Tags.BUILDSETTLEMENT:
        princ.spendResources(resources)

        princ.buildSettlement(princ, buildSlot)
      elif actionName == Tags.BUILDCITY:
        princ.spendResources(resources)

        princ.buildCity(princ, buildSlot)

      elif actionName == Tags.TURNEND:
        return True
      elif actionName == Tags.DONOTHING:
        pass



  #Returns a list of valid actions, and a list of costs and or targets
  def getValidActions(self, princ):
    validActions = dict()
    for action in self.actions:
      actionName = action[0]
      cost = action[1] 
      turnRestriction = action[2]

      #Check to see if the player is able to play any actions
      #pdb.set_trace()
      if turnRestriction == (princ.player == princ.board.getCurrentPlayer()):
        combos = princ.getResourceCombos(cost)
        #If we can pay for the action
        if len(combos) != 0:
          #Now we go through the possible actions
          locations = []
          if actionName == Tags.BUILDROAD:
            locations = princ.getPhantomRoadSlots()
          if actionName == Tags.BUILDSETTLEMENT:
            locations = princ.getPhantomTownSlots()
          if actionName == Tags.BUILDCITY:
            locations = princ.getSettlementSlots()

          #Check if there were any available slots
          if len(locations) != 0:
            validActions[actionName] = [locations, combos]

    #Now append our turnend action, or do nothing
    if turnRestriction == (princ.player == princ.board.getCurrentPlayer()):
      validActions[Tags.TURNEND] = []
    else:
      validActions[Tags.DONOTHING] = []
    return validActions

  def playGame(self):
    #First we would want our players to search through the decks, skip for now
    
    #Now we start our mainphase loop
    while True:
      self.mainPhase()

      #We check if there is a winner
      if self.checkWin() == True:
        return self.winner

  def mainPhase(self):
    self.rollProductionDice()

    #Now we give each player a chance to take their turn.
    end = False
    while end != True:
      end = self.turnPhase()
    #Now we are done, we give the turn to the next player
    self.getNextPlayer()

  def turnPhase(self):
    for player in self.getPriorityOrder():
      #pdb.set_trace()
      playerAction = player.getAction(Tags.MAINPHASE, self.getValidActions(player.princ))
      
      #Action is name, then slot, then resources
      actionName = playerAction[0]

      # self.actionsTaken[-1].append("Player {0} took {1}".format(player, actionName))

      if actionName == Tags.BUILDROAD or \
        actionName == Tags.BUILDSETTLEMENT or actionName == Tags.BUILDCITY:

        resources = playerAction[2]
        buildSlot = playerAction[1]
        #pdb.set_trace()
        if actionName == Tags.BUILDROAD:
          player.princ.spendResources(resources)

          self.buildRoad(player.princ, buildSlot)  

        elif actionName == Tags.BUILDSETTLEMENT:
          player.princ.spendResources(resources)

          self.buildSettlement(player.princ, buildSlot)
        elif actionName == Tags.BUILDCITY:
          player.princ.spendResources(resources)

          self.buildCity(player.princ, buildSlot)

        self.setWin()

        if self.checkWin():
          return True

      elif actionName == Tags.TURNEND:
        return True
      elif actionName == Tags.DONOTHING:
        pass

    self.setWin()
    return False

  def rollProductionDice(self):
    roll = None
    if self.nextProductionRoll == None:
      roll = random.randint(1, 6)
    else:
      roll = self.nextProductionRoll
      self.nextProductionRoll = None

    #Now we go through each player and tag their principalities
    for princ in self.principalities:
      for resourceSlot in princ.getResourceSlots():
        resourceSlot.item.rollResc(roll)


  #Only either a year of plenty or "Null", impliment this later
  # def rollActionDice(self):
  #   roll = None
  #   if self.nextActionRoll == None:
  #     roll = random.randint(1,6)
  #   else:
  #     roll = self.nextActionRoll
  #     self.nextActionRoll = None

  #   if roll == 1:
  #     pass
  #   else:
  #     pass

  #Incriments who's turn it is. 
  def getNextPlayer(self):
    self.currentTurn += 1
    if len(self.principalities) == self.currentTurn:
      self.currentTurn = 0
  
  def getCurrentPlayer(self):
    return self.principalities[self.currentTurn].player

  #get the order in which the players act, based upon the current turn
  def getPriorityOrder(self):
    order = [i.player for i in self.principalities[self.currentTurn:]]

    for princ in self.principalities[:self.currentTurn]:
      order.append(princ.player)

    return order

  #Checks if a player is designated as the winner
  #Returns true if a player has one and sets the winner
  def checkWin(self):
    if self.winner != None:
      return True

    return False

  #Determines if a player should have won
  def setWin(self):
    for player in self.getPriorityOrder():
      if player.princ.getPoints() == Tags.WINPOINTS:
        self.winner = player
        break

class Principality:
  def __init__(self, board, player, resourceList):

    self.board = board
    self.townSlots = deque()
    self.tokens = []
    self.handCards = []
    self.player = player

    player.princ = self
    player.board = board

    initialRoad = Road(self)
    initialRoadSlot = RoadSlot(self, None, None)
    initialRoadSlot.setItem(initialRoad)

    #Initiate the resources
    rescs = []
    rescSlots = []
    for i in range(len(resourceList)):
      rescs.append(Resource(self, resourceList[i][0], 1, resourceList[i][1]))
      rescSlots.append(ResourceSlot(self, None, None))

      rescSlots[i].setItem(rescs[i])
  
    #Create the left settlement
    leftTown = Town(self, Tags.SETTLEMENT)
    leftTownSlot = initialRoadSlot.leftTownSlot
    leftTownSlot.initiate(self, rescSlots[0], rescSlots[1], rescSlots[4],\
      rescSlots[5])

    leftTownSlot.setItem(leftTown)

    #Create the right settlement
    rightTown = Town(self, Tags.SETTLEMENT)
    rightTownSlot = initialRoadSlot.rightTownSlot
    rightTownSlot.initiate(self, rescSlots[1], rescSlots[2], rescSlots[3],\
    rescSlots[4]) 

    rightTownSlot.setItem(rightTown)

  def __repr__(self):
    #These are the towns
    towns = self.getTownSlots()

    firstTown = towns[0]

    TL = firstTown.topLeftSlot
    BL = firstTown.bottomLeftSlot

    retString = "{0}          {1}          {2}\n\n".format(BL, firstTown.leftRoadSlot, TL)

    for town in towns:

      down1 = town.downSlots[0]
      down2 = town.downSlots[1]

      up1 = town.upSlots[0]
      up2 = town.upSlots[1]

      retString += "                 {0}                \n\n".format(town)

      TR = town.topRightSlot
      BR = town.bottomRightSlot

      retString += "{0}          {1}          {2}\n\n".format(BR, town.rightRoadSlot, TR)

    retString += "We have {0} victory points\n\n".format(self.getPoints())
    #retString += "Actions taken in order were {0}\n\n".format(self.player.actionsTaken)
    return retString


  def getALLRoadSlots(self):
    roadSlots = []
    for town in self.getTownSlots():
      for road in town.getTownRoadSlots():
        if road not in roadSlots:
          roadSlots.append(road)
    return roadSlots

  def getPhantomRoadSlots(self):
    return [i for i in self.getALLRoadSlots() if i.item == None]

  def getRoadSlots(self):
    return [i for i in self.getALLRoadSlots() if i.item != None]

  def getAllTownSlots(self):
    return self.townSlots

  def getPhantomTownSlots(self):
    return [i for i in self.getAllTownSlots() if i.item == None]

  def getTownSlots(self):
    return [i for i in self.getAllTownSlots() if i.item != None]

  def getSettlementSlots(self):
    return [i for i in self.getTownSlots() if i.item.townType == Tags.SETTLEMENT]

  def getCitySlots(self):
    return [i for i in self.getTownSlots() if i.item.townType == Tags.CITY]

  #Functions to help where you can build. 
  def getLeftPhantomRoadSlot(self):
    if self.townSlots[0].item == None:
      return self.townSlots[0]
    
    return None

  def getRightPhantomRoadSlot(self):
    if self.townSlots[-1].item == None:
      return self.townSlots[-1]
    
    return None

  def getLeftPhantomTownSlot(self):
    if self.townSlots[0].item == None:
      return None

    return self.townSlots[0].leftRoadSlot

  def getRightPhantomTownSlot(self):
    if self.townSlots[-1].item == None:
      return None

    return self.townSlots[-1].rightRoadSlot


  #Get the strength score of the principality
  def getStrength(self):
    return 0

  #Gets the tournament score of the principality
  def getTourney(self):
    return 0

  #Get the commerce of the principality
  def getCommerce(self):
    return 0

  def getPoints(self):
    return len(self.getSettlementSlots()) + (2 * len(self.getCitySlots()))

  def getALLExpansionSlots(self):
    expansionSlots = []
    for town in self.getTownSlots():
      for section in town.getTownExpansionSlots():
        for slot in section:
          if slot not in expansionSlots:
            expansionSlots.append(slot)
    return expansionSlots

  def getPhantomTownExpansionSlots(self):
    return [i for i in self.getALLExpansionSlots() if i.item == None]

  def getPhantomCityExpansionSlots(self):
    return [i for i in self.getALLExpansionSlots() if i.item == None and i.townSlot.item.townType == Tags.CITY]

  def getResourceSlots(self):
    rescList = set()
    for town in self.getTownSlots():
      for rescSlot in town.getTownResourceSlots():
        rescList.add(rescSlot)
    return list(rescList)

  #Given a list of list of resource slots, we spend them
  def spendResources(self, rescList):
    for rescType in rescList:
      for rescSlot in rescType:
        rescSlot.item.spendResc()

  def getResourceCombos(self, resourceList):
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

##############################################################################
################################### Pieces ###################################
##############################################################################

class Piece:
  def __init__(self, princ, conditions=None, slot=None):
    self.princ = princ

    self.conditions = conditions
    self.slot = slot

class Town(Piece):
    def __init__(self, princ, townType, slot=None):
      super().__init__(princ, None, slot)

      self.townType = townType

    def __repr__(self):
      return "{0}".format(self.townType)

    def upgradeSettlement(self):
      self.townType = Tags.CITY


class Resource(Piece):
  def __init__(self, princ, number, amount, resc, slot=None):
    super().__init__(princ, None, slot)
    self.number = number
    self.amount = amount
    self.resource = resc

  def __repr__(self):
    return "|{0}| {2} +{1}".format(self.number, self.amount, self.resource)
  
  def rollResc(self, rolledNumber):
    if rolledNumber == self.number and self.amount < 3:
      self.amount += 1

  def giveResc(self):
    if self.amount < 3:
      self.amount += 1

  def spendResc(self):
    if self.amount == 0:
      raise Exception("You cannot spend a resource you don't have")
    else:
      self.amount -= 1

class Expansion(Piece):
  def __init__(self, princ, name, tags, slot=None):
    super().__init__(princ, None, slot)

    self.name = name
    self.tags = tags

  def __repr__(self):
    return "{0}".format(self.name)

class Road(Piece):
  def __init__(self, princ, slot=None):
    super().__init__(princ, None, slot)

  def __repr__(self):
    return "Road"

#############################################################################
################################### Slots ###################################
#############################################################################

#A slot holds info for the type it holds, and a pointer to what it holds. 
class Slot:
  def __init__(self, princ, item):
    self.princ = princ

    self.item = item    

  def setItem(self, item):
    self.item = item

  def unsetItem(self):
    temp = self.item
    self.item = None
    return temp

class TownSlot(Slot):
  name = 0
  def __init__(self, princ, leftRoad, rightRoad):
    super().__init__(princ, None)

    self.leftRoadSlot = leftRoad
    self.rightRoadSlot = rightRoad

    self.name = TownSlot.name
    TownSlot.name += 1

    #Adds the slot to our list of town slots
    if self.leftRoadSlot == None:
      princ.townSlots.appendleft(self)
    else:
      princ.townSlots.append(self)

  def __repr__(self):
    return " {1} {0} ".format(self.name, self.item)


  def expand(self, princ, Top, Bottom, ups=None, downs=None):
    
    
    TL, TR, BR, BL = None, None, None, None 
    #Check the slots of the road which side it is on. 
    if self.rightRoadSlot != None:
      TL = Top
      BL = Bottom

      TR = self.rightRoadSlot.rightTownSlot.topLeftSlot
      BR = self.rightRoadSlot.rightTownSlot.bottomLeftSlot
    else:
      TR = Top
      BR = Bottom

      TL = self.leftRoadSlot.leftTownSlot.topRightSlot
      BL = self.leftRoadSlot.leftTownSlot.bottomRightSlot

    #Call initiate now
    #pdb.set_trace()
    self.initiate(princ, TL, TR, BR, BL, ups, downs)

  def initiate(self, princ, TL, TR, BR, BL, ups=None, downs=None):
    
    #Link the resources
    self.topLeftSlot = TL
    self.topRightSlot = TR  
    self.bottomRightSlot = BR
    self.bottomLeftSlot = BL

    #Links the expantions
    self.upSlots = ups
    self.downSlots = downs

    #Pair the slots to this town
    TL.rightTown = self
    BL.rightTown = self

    TR.leftTown = self
    TL.leftTown = self

    if self.leftRoadSlot == None:
      self.leftRoadSlot = RoadSlot(princ, None, self)

    if self.rightRoadSlot == None:
      self.rightRoadSlot = RoadSlot(princ, self, None)

    #sets the up Slots
    if ups == None:
      self.upSlots = []
      self.upSlots.append(ExpansionSlot(princ, self))
      self.upSlots.append(ExpansionSlot(princ, self))

    #sets the down Slots
    if downs == None: 
      self.downSlots = []
      self.downSlots.append(ExpansionSlot(princ, self))
      self.downSlots.append(ExpansionSlot(princ, self))

    #we want to pair the town and create it
    town = Town(princ, Tags.SETTLEMENT)
    self.setItem(town)

  def getTownRoadSlots(self):
    return [self.leftRoadSlot, self.rightRoadSlot]

  def getTownExpansionSlots(self):
    return [self.upSlots, self.downSlots]

  def getTownResourceSlots(self):
    rescSlot = []

    rescSlot.append(self.topLeftSlot)
    rescSlot.append(self.bottomLeftSlot)
    rescSlot.append(self.topRightSlot)
    rescSlot.append(self.bottomRightSlot)

    return rescSlot

  def visualizeTown(self):
    #Will look like road -exp,exp- :rescTL,rescBL: :towntype :rescTR,rescBR: -exp, exp- road
    if self.item == None:
      return "Phantom Town {0}".format(self.name)
    leftRoad = self.leftRoadSlot.name
    rightRoad = self.rightRoadSlot.name
    up1 = self.upSlots[0].item
    up2 = self.upSlots[1].item 
    down1 = self.downSlots[0].item
    down2 = self.downSlots[1].item

    TL = "{0} {1} {2}".format(self.topLeftSlot.item.resource, self.topLeftSlot.item.amount, \
      self.topLeftSlot.name)
    BL = "{0} {1} {2}".format(self.bottomLeftSlot.item.resource, self.bottomLeftSlot.item.amount,\
      self.bottomLeftSlot.name)
    TR = "{0} {1} {2}".format(self.topRightSlot.item.resource, self.topRightSlot.item.amount,\
      self.topRightSlot.name)
    BR = "{0} {1} {2}".format(self.bottomRightSlot.item.resource, self.bottomRightSlot.item.amount,\
      self.bottomRightSlot.name)

    return "{0} -{1},{2}- :{3},{4}: {5} :{6},{7}: -{8},{9}- {10}"\
    .format(leftRoad, up2, up1, TL, BL, self.name, TR, BR, down1, down2, rightRoad)

class RoadSlot(Slot):
  name = 0
  def __init__(self, princ, lefttown, righttown):
    super().__init__(princ, None)

    self.name = RoadSlot.name
    RoadSlot.name += 1

    self.rightTownSlot = righttown
    self.leftTownSlot = lefttown

  def __repr__(self):
    if self.item == None:
      return ""
    else:
      return "{1} {0}".format(self.name, self.item)

  def setItem(self, item):
    super().setItem(item)

    if self.leftTownSlot == None:
      self.leftTownSlot = TownSlot(self.princ, None, self)

    if self.rightTownSlot == None:
      self.rightTownSlot = TownSlot(self.princ, self, None)


class ExpansionSlot(Slot):
  name = 0
  def __init__(self, princ, town):
    super().__init__(princ, None)

    self.name = ExpansionSlot.name
    ExpansionSlot.name += 1

    self.townSlot = town

  def __repr__(self):
    return "{0}".format(self.item)
    

class ResourceSlot(Slot):
  name = 0
  def __init__(self, princ, leftTown, rightTown):
    super().__init__(princ, None)

    self.name = ResourceSlot.name
    ResourceSlot.name += 1

    self.leftTownSlot = leftTown
    self.rightTownSlot = rightTown

  def __repr__(self):
    return "{0}".format(self.item)



#######################################################################################
################################### Board Functions ###################################
#######################################################################################

#Creates a standardBoard
#
#returns the created board
def initSimpleBoard(player1, player2):
    decks = []

    rescList1 = [(3,Tags.SHEEP), (6, Tags.GOLD), (5, Tags.BRICK),\
      (1, Tags.WHEAT), (4, Tags.WOOD), (2, Tags.ORE)]

    rescList2 = [(5, Tags.WOOD), (2, Tags.WHEAT), (4, Tags.SHEEP),\
      (6, Tags.BRICK), (1, Tags.GOLD), (3, Tags.ORE)]

    resourceCards = [(1, Tags.BRICK), (1, Tags.WOOD), (2, Tags.WHEAT), (2, Tags.ORE),\
      (1, Tags.BRICK), (1, Tags.WOOD), (2, Tags.WHEAT), (2, Tags.ORE),\
        (1, Tags.BRICK), (1, Tags.WOOD), (2, Tags.WHEAT), (2, Tags.ORE),\
          (1, Tags.BRICK), (1, Tags.WOOD), (2, Tags.WHEAT), (2, Tags.ORE),\
            (1, Tags.BRICK), (1, Tags.WOOD), (2, Tags.WHEAT), (2, Tags.ORE),\
              (1, Tags.BRICK), (1, Tags.WOOD), (2, Tags.WHEAT), (2, Tags.ORE),\
                (1, Tags.BRICK), (1, Tags.WOOD), (2, Tags.WHEAT), (2, Tags.ORE),\
                  (1, Tags.BRICK), (1, Tags.WOOD), (2, Tags.WHEAT), (2, Tags.ORE),\
                    (1, Tags.BRICK), (1, Tags.WOOD), (2, Tags.WHEAT), (2, Tags.ORE),\
                      (1, Tags.BRICK), (1, Tags.WOOD), (2, Tags.WHEAT), (2, Tags.ORE),\
                        (1, Tags.BRICK), (1, Tags.WOOD), (2, Tags.WHEAT), (2, Tags.ORE),\
                          (1, Tags.BRICK), (1, Tags.WOOD), (2, Tags.WHEAT), (2, Tags.ORE),]

    numberofPiles = 0

    firstTurn = 0

    actions = Tags.SIMPLEACTIONS

    #(self, decks, resourceCards, numberofPiles, principalities, firstTurn, actions)
    board = Board(decks, resourceCards, numberofPiles, [None, None], firstTurn, actions)

    princ1 = Principality(board, player1, rescList1)
    princ2 = Principality(board, player2, rescList2)

    board.principalities[0] = princ1
    board.principalities[1] = princ2

    return board


#Define the tests here
class TestStringMethods(unittest.TestCase):

  #We're just gonna test out the whole board to find the runtime errors
  def testBoard(self):
    #Lets create the board

    # totalsNot = 0
    # for _ in range(100):
    #   player1 = RandomPlayer(None, None)
    #   player2 = RandomPlayer(None, None)
    #   board = initSimpleBoard(player1, player2)    

    #   if board.playGame().princ.getPoints() != 10:
    #     totalsNot += 1

    # print(totalsNot)



    player1 = RandomPlayer(None, None)
    player2 = RandomPlayer(None, None)
    board = initSimpleBoard(player1, player2)    
    print(board.playGame().princ)


    """
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
    """

if __name__ == '__main__':
    unittest.main()