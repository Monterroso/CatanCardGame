import unittest

import Tags

from collections import deque

import random

#This is a board for python. 

###################################################################################
################################### Game Parts ###################################
###################################################################################

class Player:
  def __init__(self, board, princ):
    self.board = board

    self.princ = princ

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
    actionToTake = random.choice(validActions.keys())

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
    top = self.resourceCards.pop()
    bottom = self.resourceCards.pop()

    town = Town(princ, Tags.SETTLEMENT)
    townSlot.expand(princ, top, bottom)

    townSlot.setItem(town)

  #Builds a city at the desired location
  def buildCity(self, princ, townSlot):
    townSlot.upgradeSettlement()

  #Builds an expantion at the desired location
  def buildExpansion(self, princ, expansion, expansionSlot):
    expansionSlot.setItem(expansion)

  #Returns a list of valid actions, and a list of costs and or targets
  def getValidActions(self, princ):
    validActions = dict()
    for action in self.actions:
      actionName = action[0]
      cost = action[1] 
      turnRestriction = action[2]

      #Check to see if the player is able to play any actions
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

    #Now append our turnend action
    if turnRestriction == (princ.player == princ.board.getCurrentPlayer()):
      validActions[Tags.TURNEND] = []
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
      playerAction = player.getActions(Tags.MAINPHASE, self.getValidActions(player.princ))

      #Action is name, then slot, then resources
      actionName = playerAction[0]
      if actionName == Tags.BUILDROAD:
        for slot in playerAction[2]:
          slot.item.spendResc()
        self.buildRoad(player.princ, playerAction[1])    
      elif actionName == Tags.BUILDSETTLEMENT:
        for slot in playerAction[2]:
          slot.item.spendResc()   
        self.buildSettlement(player.princ, playerAction[1])
      elif actionName == Tags.BUILDCITY:
        for slot in playerAction[2]:
          slot.item.spendResc()
        self.buildCity(player.princ, playerAction[1])
      elif actionName == Tags.TURNEND:
        self.setWin()
        return True

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
    return self.principalities[self.currentTurn]

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

  def getRoadSlots(self):
    roadSlots = []
    for town in self.getTownSlots():
      for road in town.getTownRoadSlots():
        if road != None:
          roadSlots.append(road)
    return roadSlots


  #Returns the phantom road slot on left, returns it or None if not there
  def getLeftPhantomRoadSlot(self):
    return None

  def getRightPhantomRoadSlot(self):
    return None

  def getLeftPhantomTownSlot(self):
    return None

  def getRightPhantomTownSlot(self):
    return None


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
    return len(self.getSettlementSlots()) + 2 * len(self.getCitySlots)

  def getPhantomTownSlots(self):
    return [i for i in self.townSlots if i.item == None]

  def getTownSlots(self):
    return [i for i in self.townSlots if i.item != None]

  def getSettlementSlots(self):
    return [i for i in self.townSlots if i.item != None and i.item.townType == Tags.SETTLEMENT]

  def getCitySlots(self):
    return [i for i in self.townSlots if i.item != None and i.item.townType == Tags.CITY]


  def getExpansionSlots(self):
    expansionSlots = []
    for town in self.getTownSlots():
      for section in town.getTownExpansionSlots():
        for slot in section:
          expansionSlots.append(slot)
    return expansionSlots

  def getPhantomRoadSlots(self):
    return [i for i in self.getRoadSlots() if i.item == None]


  def getPhantomTownExpansionSlots(self):
    return [i for i in self.getExpansionSlots() if i.item == None]

  def getPhantomCityExpansionSlots(self):
    return [i for i in self.getExpansionSlots() if i.item == None and i.townSlot.item.townType == Tags.CITY]

  def getResourceSlots(self):
    rescList = set()
    for town in self.getTownSlots():
      for rescSlot in town.getTownResourceSlots():
        rescList.add(rescSlot)
    return list(rescList)

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
    return "Number={0} Amount={1} Resc={2}".format(self.number, self.amount, self.resource)
  
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
    return "Town {0}, {1} ".format(self.name, self.item)


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

    if lefttown == None:
      self.leftTownSlot = TownSlot(princ, None, self)
    else:
      self.leftTownSlot = lefttown

    if righttown == None:
      self.rightTownSlot = TownSlot(princ, self, None)
    else:
      self.rightTownSlot = righttown

  def __repr__(self):
    return "Road {0}".format(self.name)

class ExpansionSlot(Slot):
  name = 0
  def __init__(self, princ, town):
    super().__init__(princ, None)

    self.name = ExpansionSlot.name
    ExpansionSlot.name += 1

    self.townSlot = town

  def __repr__(self):
    return "Exp {0}".format(self.item)
    

class ResourceSlot(Slot):
  name = 0
  def __init__(self, princ, leftTown, rightTown):
    super().__init__(princ, None)

    self.name = ResourceSlot.name
    ResourceSlot.name += 1

    self.leftTownSlot = leftTown
    self.rightTownSlot = rightTown

  def __repr__(self):
    return "Resc {0}".format(self.item)



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

    resourceCards = [(1, Tags.BRICK), (1, Tags.WOOD), (2, Tags.WHEAT), (2, Tags.ORE)]

    numberofPiles = 0

    firstTurn = 0

    actions = Tags.SIMPLEACTIONS

    board = Board(decks, resourceCards, numberofPiles, [None, None], firstTurn, actions)

    princ1 = Principality(board, player1, rescList1)
    princ2 = Principality(board, player2, rescList2)

    board.principalities[0] = princ1
    board.principalities[0] = princ2

    return board

############################################################################################
################################### Visualizer Functions ###################################
############################################################################################  
"""
#This will, given a board, visualize it in text
#
#does not return


#Given a card, adds it to the player's hand
#
#gets the string, adds it to the list of player cards. 
def giveCard(card, princ):
  princ.cards.Add(card)

#Allows the player to search a deck, and select any card from it
#
#Gives the player the list
#The player then returns a an index of that list for the card they want
#That card is then removed from the deck, and added to their hand
#The deck is then reshuffled. 
def searchDeck(deck, player):
  #Just send the deck and the tag to the player for them to select
  result = player.action(Tags.DRAWFROMDECK, deck)

  #Give the card to the player
  giveCard(result, player.princ)

  #Shuffle the deck
  shuffle(deck)


#This shuffles the deck randomly
#
#Given this list, shuffles the list
def shuffle(deck):
  pass

#A valid function determines when an action can be played
#
#If an action can be played in multiple ways, it should return all of them. 
#The returned actions, include the resources and cards spent on the action. 
#Action string is extra info. 
# 
# Returns list of "actions" which is list of name input, then name output 
def validActions(player, board, actionString):
  #We check trades here, we will do that later, not now

  #Now we check to see if we can build, get all phantoms. 
  phantoms = getPhantoms(player.princ)

  actionPairs = set()

  #We get all of the buildings now that we can bulid. 
  #We won't use action cards for now, only buildings
  for action in board.actions:
    #Each action is a building and a cost.
    #Cost is a list of resources
    partitions = getRescCombinations(player.princ, action[1])

    if len(partitions) != 0:
      for partition in partitions:
        if player == board.currentTurn:

          if action[0] == Tags.BUILDROAD:
            for slot in getRoadPhantoms(player.princ):
              actionPairs.add(action[0], partition, [slot])
          
          if action[0] == Tags.BUILDSETTLEMENT:
            for slot in getSettlementExpansionPhantoms(player.princ):
              actionPairs.add(action[0], partition, [slot])

          if action[0] == Tags.BUILDCITY:
            for slot in player.princ.towns:
              actionPairs.add(action[0], partition, [slot])

          #Now we want to append to action pairs, the latter is a list of targets
          #if action

  #Send the action list to player
  return actionPairs
  

#Gets all possible combintations of the elements. 




#Signals to the players that a settlement is being built
#
#board is sent to players, sending the phantom settlement, along with the current board state
#each card has a valid function to determine if can be played
#Each card is searched with that valid function, list of valid actions are then sent to the player
def onSetBuild(board):
  pass

#Signals to the players that a road is being built
#
#board is sent to players, sending the phantom road, along with the current board state
#each card has a valid function to determine if it can be played
#Each card is searched with that valid function, list of valid actions are then sent to the player
def onRoadBuild(board):
  pass

#Signals to the players that a city is being built
#
#board is sent to players, sending the phantom city, along with the current board state
#each card has a valid function to determine if it can be played
#Each card is searched with that valid function, list of valid actions are then sent to the player
def onCityBuild(board):
  pass

#Signals to the players that an action is being played
#
#Actions cards differ, so board is sent to the player, as is the action card being played
#Each card has a valid function to determine if it can be played
#Each card is searched with that valid function, list of valid actions are then sent to the player
def onActionPlay(board):
  pass

#Singls to the players that a turn has started
def onTurnStart(board):
  pass

#Signals to the players that a mainphase turn has begun. 
def onMainPhase(board):
  pass

#Signals to the players that the endturn is occuring.
def onTurnEnd(board):
  pass

#Checks to see if the game has ended, and awards a winner
#
#goes through each person's principalities, checks all the objects for ones with victory points
#returns the number of victory points
def checkEnd(board):
  pass


##################
#Player Functions#
##################
#
#These give the board and the trigger to the player, and get an action 
#from a player. 

##################
#Helper Functions#
##################
#
#These do not modify the board, and just get information in some way

#Determines which player goes first. 
#
#returns the number of who goes first
def detFirst(player1, player2):
  return player1

#Determines which player acts first in the case of a tie, based on board state
#
#Returns the player
def detPrior(board):
  return board.currentTurn

#Gets the knight strength of a player
#
#Goes through each expansion, gets it's knight strength, and then returns that value
#
#Returns an integer of the strength
def getStrength(princ):
  pass

#Gets the tournament strength of a player
#
#Goes through each expansion, gets it's knight tourney, and returns that value
#
#returns an integer of the tourney value
def getTourney(princ):
  pass

#Gets the commerce points of a player
#
#Goes through each expansion, gets it's commerce strength, and returns that value. 
#
#Returns the value as an integer. 
def getCommerce(princ):
  pass

#Searches the pile of things 
#
#Goes through all of the things, and selects the items with the tag
def getTagItems(princ, tag):
  pass

###############
#Game Function#
###############
#
#These functions fasciliate the running of the game of catan

#Rolls the production dice
#
#Dice rolls are pregenerated before, this pops from the dice list
def rollProductionDice(board):
  roll = board.resolveRolls.pop()

  #We should assign resources to people.
  # 
  #We simply go through each settlement and get all of the resources and their numbers
  #Then, we assign resources to them as we see fit.  

  princs = [board.princ2, board.princ1]

  #We assign to both players
  for princ in princs:
    rescs = getObjects(getRescTiles(princ))

    #We assign resources
    for res in rescs:
      if res.number == roll:

        #We check if there is overflow
        if res.amount == 3:
          pass
        #We then assign resource otherwise
        else:
          res.amount += 1

  #We have now assigned resources properly


  

#Rolls the action dice
#
#Dice rolls are pregenerated before, this pops from the dice list
def rollActionDice(board):
  board.resolveRolls.pop()

  #We go and handle what happens with each event

  #We actually don't have to do anything right now, just ignore this



#Takes in a list and partitions the list into a list of how many
#
#Takes in the list of all the cards, shuffles them
#Then breaks them into equal partitions, or nearly equal
#
#Returns the number as lists
def partitionDecks(numdecks, listofCards):
    return 0

#When called, allows the player to have a mainphase action
#
#Sends player Board
#Player returns action, string of action, pool of resources, and card
#Call begin that specific action phase. 
#resolve action
#return true if action wasn't empty action, return false if was
def mainphase(board):
  return 0

#When called, simulates a turn of one player. 
#
#Speed up, allow suppression of phases
#
#First calls turnstart()
#Calls rollaction()
#resolves actiontaken
#
#calls rollproduction
#calls productiontaken()
#
#calls mainphase loop of player
#once completed, call turnend
#call resolveturnend
def turn(board):
  onTurnStart(board)

  rollActionDice(board)

  rollProductionDice(board)

  turnEnd = Tags.TURNCONTINUE

  while turnEnd == Tags.TURNCONTINUE:
    turnEnd = mainphase(board)

    if turnEnd == Tags.GAMEEND:
      return True
      


#Function that when called, runs the game
#
#Initialize the cards to be played with in a deck. 
#Call initPrincipality twice, for both players, assign names
#Initiate respective tokens
#
#Call function to determine who goes first
#Allow both to select and search a deck, determining who goes first.
#Once both select the deck, cause them to do this operation three times. 
#
#Proceed with turn loop game until completion
#
#Log any information of the game as appropriate then exit
def playGame(board, player1, player2):

  #We initiate everything we need for the board
  cards = []
  cardDefs = dict()

  resourceCards = [Tags.BRICK, Tags.BRICK, Tags.WOOD, Tags.WHEAT]

  numberofPiles = 0

  productionRolls = [1,2,3,4,5,6,6,5,4,3,2,1]

  actionRolls = [6,5,4,3,2,1,1,2,3,4,5,6]
  
  resolveRolls = [3,3,3,3,3,3,3,3,3,3,3]

  actions = Tags.ACTIONS

  board = initBoard(cards, resourceCards, cardDefs, numberofPiles, player1, player2, productionRolls, actionRolls, resolveRolls, actions)

  #Allow both players to select a deck, skip this step for now, do this three times

  end = False

  while not end:
    end = turn(board)

  #Now we are done with the game
  


#Initiates the board to be played on. 
#
#Initiates all the tokens, the principalities, 
def initBoard(cards, resourceCards, cardDefs, numberofPiles, player1, player2, productionRolls, actionRolls, resolveRolls, actions):

    decks = partitionDecks(numberofPiles, cards)

    rescList1 = [(Tags.SHEEP, 3), (Tags.GOLD, 6), (Tags.BRICK, 5), (Tags.ORE, 2),(Tags.WOOD,4),(Tags.WHEAT,1)]
    rescList2 = [(Tags.WOOD, 5), (Tags.WHEAT, 2), (Tags.SHEEP, 4), (Tags.ORE, 3), (Tags.GOLD, 1), (Tags.BRICK, 6)]
    
    currentTurn = detFirst(player1, player2)

    princ1 = initPrincipality(None, rescList1, player1)
    princ2 = initPrincipality(None, rescList2, player2)

    board = Board(decks, resourceCards, cardDefs, numberofPiles, princ1, princ2, currentTurn, productionRolls, actionRolls, resolveRolls, actions)

    return board
"""

#Define the tests here
class TestStringMethods(unittest.TestCase):

  #We're just gonna test out the whole board to find the runtime errors
  def testBoard(self):
    #Lets create the board
    player1 = RandomPlayer(None, None)
    player2 = RandomPlayer(None, None)
    board = initSimpleBoard(player1, player2)
    

    #Build a settlement for player1
    princ1 = board.principalities[0]

    roadCons = princ1.getPhantomRoadSlots()

    roadCon = roadCons.pop()

    road = Road(princ1)

    roadCon.setItem(road)

    townslot = princ1.getPhantomTownSlots().pop()

    topResc = Resource(princ1, 7, 2, Tags.WHEAT)
    topRescSlot = ResourceSlot(princ1, None, None)
    topRescSlot.setItem(topResc)

    botResc = Resource(princ1, 7, 3, Tags.GOLD)
    botRescSlot = ResourceSlot(princ1, None, None)
    botRescSlot.setItem(botResc)

    townslot.expand(princ1, topRescSlot, botRescSlot)

    ###############################################

    roadCons1 = princ1.getPhantomRoadSlots()

    roadCon1 = roadCons1.pop()

    road1 = Road(princ1)

    roadCon1.setItem(road1)

    townslot1 = princ1.getPhantomTownSlots().pop()

    topResc1 = Resource(princ1, 7, 2, Tags.WOOD)
    topRescSlot1 = ResourceSlot(princ1, None, None)
    topRescSlot1.setItem(topResc1)

    botResc1 = Resource(princ1, 7, 2, Tags.BRICK)
    botRescSlot1 = ResourceSlot(princ1, None, None)
    botRescSlot1.setItem(botResc1)

    townslot1.expand(princ1, topRescSlot1, botRescSlot1)

    ###############################################


    # #Now get the settlement build locations
    # townCons = princ1.getSettlementSlots()

    # townCon = townCons.pop()

    # town = Town(princ1, Tags.SETTLEMENT)

    # townCon.setItem(town)

    #Now we want to test gettin g resources
    #RESCOURCELIST = [GOLD, ORE, BRICK, WOOD, WHEAT, SHEEP]

    #princ1.getCombos([["a", "b", "c"],["A","B","C"],[1,2,3]])

    #wants = [[[k.item.resource for k in i] for i in j] for j in princ1.getResourceCombos([2,1,1,1,6,1])]

    # goldSlots = [i for i in princ1.getResourceSlots() if i.item.resource == Tags.GOLD]

    # wantgold = [[i.name for i in j] for j in princ1.getSingleResourceCombination(3, goldSlots)]

    print("Winner is {0}".format(board.playGame()))



    for town in princ1.townSlots:
      print(town.visualizeTown())



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