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
  """A player object given a state will give actions

  A player is assumed to, when asked for some object, return 
  a valid object, if none are valid, it should return None

  """
  name = 0
  def __init__(self, board, princ):
    self.name = Player.name
    Player.name += 1

    self.board = board

    self.princ = princ


  def __repr__(self):
    return "{0}".format(self.name)

  def getAction(self, phase, actionPerformed=None):
    """Given the current phase and the action taken by the main player, return the action string

    Args:
      phase (string): The phase this is occuring in
      actionPerformed (string): The action that the main player (if present) took

    Returns:
      string: The action this player chooses to perform, none if can't or chooses not to
    """

    return None

  def selectPlayer(self, phase, actionPerformed=None):
    """Given the current phase and the action taken by the main player, return the chosen player

    Args:
      phase (string): The phase this is occuring in
      actionPerformed (string): The action that the main player (if present) took

    Returns:
      player: The player who should be chosen, or none if not possible
    """

    return None

  def selectResourceSlots(self, phase, resourceTypes, actionPerformed=None):
    """Given the current phase and the action taken by the main player, selects resource slots

    The slots that are selected can be selected multiple times, though it must have
    the number of resources to support being selected for that many times. 

    Args:
      phase (string): The phase this is occuring in
      resourceTypes(list): A list of resources that need to be chosen
      actionPerformed (string): The action that the main player (if present) took

    Returns:
      list: the list of slot resources to be chosen
    """

    return None

  def selectOpenResourceSlots(self, phase, resourceType=None, actionPerformed=None):
    """Given the current phase and the action taken by the main player, selects resource slots

    All resource slots chosen must have less than 3 resources in them. Returns None
    if this action is not possible. Can select a slot multiple times, it can be added as 
    long as selecting it multiple times would not cause the slot to have 3 resources. If 
    resourceType array is None, you select any single OpenResource

    Args:
      phase (string): The phase this is occuring in
      resourceTypes(list): A list of resources that need to be chosen
      actionPerformed (string): The action that the main player (if present) took

    Returns:
      list: the list of slot resources to be chosen
    """

    return None

  def selectHaveResourceSlot(self, phase, resourceType=None, actionPerformed=None):
    """Given the current phase and the action taken by the main player, selects resource slots

    All resource slots chosen must have more than 0 resources in them. Returns None
    if this action is not possible. Can select the same slot multiple times, as long as 
    selecting a slot multiple times would not reduce a slot to 0 resources. If no resource
    type array is given, then select any Have resource slot. 

    Args:
      phase (string): The phase this is occuring in
      resourceTypes(list): A list of resources that need to be chosen
      actionPerformed (string): The action that the main player (if present) took

    Returns:
      list: the list of slot resources to be chosen
    """

    return None

  def selectOpenRoadSlot(self, phase, actionPerformed=None):
    """Selects a valid slot to build a road

    Args:
      phase (string): The phase this is occuring in
      actionPerformed (string): The action that the main player (if present) took

    Returns:
      RoadSlot: the road slot that is empty, None if there is none
    """

    return None

  def selectOpenSettlementSlot(self, phase, actionPerformed=None):
    """Selects a valid slot to build a settlement

    Args:
      phase (string): The phase this is occuring in
      actionPerformed (string): The action that the main player (if present) took

    Returns:
      TownSlot: the town slot that is empty, None if there is none
    """
    return None

  def selectSettlementSlot(self, phase, actionPerformed=None):
    """Selects a valid slot to build a city

    Args:
      phase (string): The phase this is occuring in
      actionPerformed (string): The action that the main player (if present) took

    Returns:
      TownSlot: the town slot that has a settlement, None if there is none
    """

    return None

  def selectCard(self, phase, deck, actionPerformed=None):
    """Selects a valid slot to build a city

    Args:
      phase (string): The phase this is occuring in
      deck (list): The list of strings where one is to be chosen
      actionPerformed (string): The action that the main player (if present) took

    Returns:
      string: the card from the deck that is intended to be selected. 
    """

    return None


class RandomPlayer(Player):
  def __init__(self, board, princ):
    super().__init__(board, princ)
    
  #Just returns one of the valid actions
  def getAction(self, phase, actionPerformed=None):

    validActions = self.board.getValidActions(self.princ)

    if len(validActions) == 0:
      return None

    return random.choice(validActions)

  #Selects a player from a list of players to return given the phase
  def selectPlayer(self, phase, actionPerformed=None):
    return random.choice(self.getOtherPlayers())

  #Given a list of resources and the phase, we return a processed
  #list of resources
  def selectResourceSlots(self, phase, resList, actionPerformed=None):
    #First we get the various combinations
    combinations = self.princ.getResourceCombos(resList)

    if len(combinations) == 0:
      return None

    return random.choice(combinations)


  #Selects a resource Slot that has less than 3 resources
  def selectOpenResourceSlot(self, phase, resourceType=None, actionPerformed=None):
    retraw = None
    if resourceType != None:
      retraw = [i for i in self.princ.getResourceSlotsOf(resourceType) if i.item.amount < 3]
    else:
      retraw = [i for i in self.princ.getResourceSlots() if i.item.amount < 3]

    if len(retraw)  == 0:
      return None
    return random.choice(retraw)

  #Selects a resource Slot that has more than 0 resources
  def selectHaveResourceSlot(self, phase, resourceType=None, actionPerformed=None):
    retraw = None
    if resourceType != None:
      retraw = [i for i in self.princ.getResourceSlotsOf(resourceType) if i.item.amount > 0]
    else:
      retraw = [i for i in self.princ.getResourceSlots() if i.item.amount > 0]

    if len(retraw)  == 0:
      return None
    return random.choice(retraw)

  #Selects an open road Slot
  def selectOpenRoadSlot(self, phase, actionPerformed=None):
    slots = self.princ.getPhantomRoadSlots()

    if len(slots) == 0:
      return None
    return random.choice(slots)

  #Selects an open settlement Slot
  def selectOpenSettlementSlot(self, phase, actionPerformed=None):
    slots = self.princ.getPhantomTownSlots()

    if len(slots) == 0:
      return None
    return random.choice(slots)

  #Selects a settlement Slot
  def selectSettlementSlot(self, phase, actionPerformed=None):
    slots = self.princ.getSettlementSlots()
      
    if len(slots) == 0:
      return None
    return random.choice(slots)

  #Selects a card from a "deck" 
  def selectCard(self, phase, deck, actionPerformed=None):
    return random.choice(deck)

class Board:
  """A board contains the methods needed to run a game

  Start a game by initializing the board, and then by calling playGame
  """
  def __init__(self, decks, resourceCards, numberofPiles, principalities, firstTurn):
    self.decks = decks
    self.resourceCards = resourceCards
    self.numberofPiles = numberofPiles

    self.principalities = principalities

    self.knightToken = Tags.KTOKEN
    self.commerceToken = Tags.CTOKEN
    
    self.currentTurn = firstTurn

    self.nextProductionRoll = None
    self.nextActionRoll = None

    self.winner = None

    self.numRoads = 9
    self.numTowns = 5
    self.numCities = 7

    self.actionsTaken = []
    
  ###############
  # Can Perform #
  ###############
  #
  #This block is dedicated to functions that check if actions can be performed

  #Checks if a player can trade
  def canTradeResource(self, princ, resource):
    rescNeeded = self.getTradeRate(resource)

    resourceList = [0 for _ in range(Tags.NUMRESOURCES)]
    resourceList[resource] = rescNeeded
    if princ.checkPlayer.selectResourceSlots(None, resourceList) != None:
      princ.checkPlayer.selectHaveResourceSlot(None, resource)


  #Checks if a road can be built
  def canBuildRoad(self, princ):
    return len(princ.getPhantomRoadSlots()) != 0 and \
      princ.checkPlayer.selectResourceSlots(None, Tags.BUILDROADCOST)\
       and self.numRoads > 0


  #Checks if a settlement can be built
  def canBuildSettlement(self, princ):
    return len(princ.getPhantomTownSlots()) != 0 and \
      princ.checkPlayer.selectResourceSlots(None, Tags.BUILDSETTLEMENTCOST)\
       and self.numTowns > 0

  #Checks if a settlement can be built
  def canBuildCity(self, princ):
    return len(princ.getSettlementSlots()) != 0 and \
      princ.checkPlayer.selectResourceSlots(None, Tags.BUILDCITYCOST)\
       and self.numCities > 0

  #Gets all the valid actions for a principality
  def getValidActions(self, princ):
    validActions = []

    if princ.player == self.getCurrentPlayer():
      #We check to see if we have the resources for building
      if self.canBuildRoad(princ):
        validActions.append(Tags.BUILDROAD)
      if self.canBuildSettlement(princ):
        validActions.append(Tags.BUILDSETTLEMENT)
      if self.canBuildCity(princ):
        validActions.append(Tags.BUILDCITY)

      #We check if we can trade
      for rescNum in range(Tags.NUMRESOURCES):
        if self.canTradeResource(princ, rescNum) == True:
          validActions.append(Tags.TRADETYPES[rescNum])


    return validActions

  ###########
  # Perform #
  ###########
  #
  #This block is dedicated to functions that perform various actions

  #Builds a road at the desired location
  def buildRoad(self, princ, roadSlot):
    road = Road(princ)
    roadSlot.setItem(road)
    self.numRoads -= 1

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

    self.numTowns -= 1

  #Builds a city at the desired location
  def buildCity(self, princ, townSlot):
    townSlot.item.upgradeSettlement()
    self.numCities -= 1

  #Builds an expantion at the desired location
  def buildExpansion(self, princ, expansion, expansionSlot):
    expansionSlot.setItem(expansion)

  def perform(self, actionToTake, playerResponses):
    """This function sends players info given their responses

    TODO: Impliment actions

    Given the actions and player responses, all steps and responses
    are sent to the player and carried out. The usual steps are given an action

    Ask for resources from the player
    Get the respective slots from the player, then create the thing
    Spend the resources

    Args:
        actionToTake (string): The action the currrent player seeks to perform
        playerResponses (List): The list in order of priority of player's responses to the action

    """

    self.actionsTaken.append(actionToTake)

    currentPlayer = self.getCurrentPlayer()
    #For now we ignore the player responses

    if actionToTake == Tags.BUILDROAD:
      resourcesToGive = currentPlayer.selectResourceSlots(Tags.BUILDROAD, Tags.BUILDROADCOST)
      slotToBuild = currentPlayer.selectOpenRoadSlot(Tags.BUILDROAD)
      self.buildRoad(currentPlayer.princ, slotToBuild)
      currentPlayer.princ.spendResources(resourcesToGive)

    elif actionToTake == Tags.BUILDSETTLEMENT:
      resourcesToGive = currentPlayer.selectResourceSlots(Tags.BUILDSETTLEMENT, Tags.BUILDSETTLEMENTCOST)
      slotToBuild = currentPlayer.selectOpenSettlementSlot(Tags.BUILDSETTLEMENT)
      self.buildSettlement(currentPlayer.princ, slotToBuild)
      currentPlayer.princ.spendResources(resourcesToGive)

    elif actionToTake == Tags.BUILDCITY:
      resourcesToGive = currentPlayer.selectResourceSlots(Tags.BUILDCITY, Tags.BUILDCITYCOST)
      slotToBuild = currentPlayer.selectSettlementSlot(Tags.BUILDCITY)
      self.buildCity(currentPlayer.princ, slotToBuild)
      currentPlayer.princ.spendResources(resourcesToGive)

    elif actionToTake in Tags.TRADETYPES:
      tradeamount = [0 for _ in Tags.NUMRESOURCES]
      tradeamount[actionToTake] = self.getTradeRate(currentPlayer.princ, Tags.RESCOURCELIST[actionToTake])
      resourcesToTrade = currentPlayer.selectResourceSlots(actionToTake, tradeamount)
      currentPlayer.princ.spendResources(resourcesToTade)
      slotToRecieve = currentPlayer.selectOpenResourceSlot(curentPlayer.princ)
      currentPlayer.princ.giveResources(slotToRecieve)

      
  

  #############
  # Play Game #
  #############
  #
  #
  #This block has functions for playing the game
  def playGame(self):
    #First we would want our players to search through the decks, skip for now
    
    #Now we start our mainphase loop
    while True:
      self.takeTurn()

      if self.checkWin() == True:
        return self.winner

      self.getNextPlayer()

  def takeTurn(self):
    #Should be implimented
    self.rollActionDice()

    #Should also be implimented, not implimented completely
    self.rollProductionDice()

    #We now get to the player's main phase
    self.mainPhase()

    #We do anything after the main phase has ended. 


  #The actions as tag strings are given

  def mainPhase(self):

    #We want to loop through getting actions
    while True:
      #We want to get the action of the player 
      playerAction = self.getCurrentPlayer().getAction(phase=Tags.MAINPHASE)

      #We check if the player action is valid, and isn't None, if it is we continue
      if playerAction == None:
        #If it's nothing, we don't need to do anything and can safetly return
        return

      #We will impliment the get player response actions later, for now we just get the player action
      #playerResponses = getPlayerResponseActions(actionToTake,phase=Tags.MAINPHSE)
      playerResponses = None

      #Now we perform said action
      self.perform(playerAction, playerResponses)

      #set the winner if there is one
      self.setWin()

      if self.checkWin() == True:
        return

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

  #Incriments who's turn it is. 
  def getNextPlayer(self):
    self.currentTurn += 1
    if len(self.principalities) == self.currentTurn:
      self.currentTurn = 0

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
  def rollActionDice(self):
    roll = None
    if self.nextActionRoll == None:
      roll = random.randint(1,6)
    else:
      roll = self.nextActionRoll
      self.nextActionRoll = None

    #We will only impliment the tournament roll for now, and impliment the other elements later. 
    #Tournament Roll
    #if roll == 1:
    #  #Check to see who has the highest tournament value. 
    #  winner = self.getHighestTournament()

    #  if winner != None:
    #    #We give them the phase to choose a resource from winning
        
    #    #Winner then selects slots to win for the tournament
    #    resourceSlots = winner.selectOpenResourceSlot(Tags.WINTOURNAMENT, Tags.RESOURCELIST)

    #    #Now you want to assign those resources
    #    for slot in resourceSlots:
    #      slot.item.giveResc()

    #Commerce Roll
    #elif roll == 2:
    #  #Check to see who has the highest commerce value.
    #  winner = self.getHighestCommerce()

    #  if winner != None:
    #    victim = winner.selectPlayer(Tags.WINCOMMERCE, self.getOtherPlayers(winner))

        

    #    winSlot = winner.selectOpenResourceSlot(Tags.WINCOMMERCE, victom.getOpenResources())
    #    #selectResourceSlot(self, phase, resourceTypes)

    #    loseSlot = victim.selectResourceSlot(Tags.LOSECOMMERCE, set(slot.item.resource))

    #Year of Plenty
    if roll == 4:
      #Give each player the ability to select a resource
      for player in self.getPriorityOrder():
        slot = player.selectOpenResourceSlot(Tags.YEAROFPLENTY)

        if slot != None:
          slot.item.giveResc()


  #Given a function, uses that to get the highest attribute from all the players
  
  ################
  # Misc Methods #
  ################
  #
  #
  # These methods are general helper functions for the board

  def getTradeRate(self, princ, resource):
    if resource == Tags.BRICK:
      return 3
    if resource == Tags.GOLD:
      return 3
    if resource == Tags.ORE:
      return 3
    if resource == Tags.WOOD:
      return 3
    if resource == Tags.SHEEP:
      return 3
    if resource == Tags.WHEAT:
      return 3

  def getHighest(self, highestThing):
    """This gets the highest of some value, given that value

    Args:
      highestThing (string): The attribute we want to get the highest of
    """
    highestPlayer = None
    highestAmount = 0
    for player in self.getPriorityOrder():
      amount = player.princ.highestThing()
      if amount > highestAmount:
        highestAmount = amount
        highestPlayer = player
      elif amount == highestAmount:
        highestPlayer = None

    return highestPlayer
        
  #Returns the player with the highest Tournament Value
  def getHighestTournament(self):
    return self.getHighest(Principality.getTourney)

  def getPlayerResponseActions(self, incAction, phaseType):
    return [i.getAction(incAction, phaseType) for i in self.getPriorityOrder()]

  #Returns the player with the highest Strength value
  def getHighestStrength(self):
    return self.getHighest(Principality.getStrength)

  #Returns the player with the highest Commerce Value
  def getHighestCommerce(self):
    return self.getHighest(Principality.getCommerce)
  
  def getCurrentPlayer(self):
    return self.principalities[self.currentTurn].player

  def getOtherPlayers(self, currentPlayer):
    return [i.player for i in self.principalities if i.player != currentPlayer]

  #get the order in which the players act, based upon the current turn
  def getPriorityOrder(self):
    order = [i.player for i in self.principalities[self.currentTurn:]]

    for princ in self.principalities[:self.currentTurn]:
      order.append(princ.player)

    return order

  #Given the resources, we covnert it into a resource Array
  def processResourceSlots(self, resourceSlots):
    rescArray = [[] for _ in range(Tags.NUMRESOURCES)]
    for slot in resourceSlots:
      for i in range(Tags.NUMRESOURCES):
        if slot.item.resource == Tags.RESCOURCELIST[i]:
          rescArray[i].append(slot)

    return rescArray

class Principality:
  #Takes in the player, board, the list of starting resources clockwise
  #Actions is a dictionary of actions, keys as the action, and it's phases
  def __init__(self, board, player, checkPlayer, resourceList):

    self.board = board
    self.townSlots = deque()
    self.tokens = []
    self.handCards = []
    self.player = player
    self.checkPlayer = checkPlayer

    player.princ = self
    player.board = board

    checkPlayer.princ = self
    checkPlayer.board = board

    

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

  def getTownexpansionSlots(self):
    return [i for i in self.getAllExpansionSlots() if i.item != None and i.townSlot.item.townType == Tags.SETTLEMENT]

  def getCityexpansionSlots(self):
    return [i for i in self.getAllExpansionSlots() if i.item != None and i.townSlot.item.townType == Tags.CITY]

  def getResourceSlots(self):
    rescList = set()
    for town in self.getTownSlots():
      for rescSlot in town.getTownResourceSlots():
        rescList.add(rescSlot)
    return list(rescList)

  def getResourceSlotsOf(self, rescType):
    return [i for i in getResourceSlots() if i.item.resource == rescType]

  #This returns a list of all resource slots with resource that's greater than zero 
  def getHaveResources(self):
    return set([i.item.resource for i in getResourceSlots() if i.item.amount > 0])

  #This returns a list of all resources that you can actively take on more of
  def getOpenResources(self):
    return set([i.item.resource for i in getResourceSlots() if i.item.amount < 0])

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
    return sum([i.getStrength() for i in self.getTownexpansionSlots()])

  #Gets the tournament score of the principality
  def getTourney(self):
    return sum([i.getTourney() for i in self.getTownexpansionSlots()])

  #Get the commerce of the principality
  def getCommerce(self):
    return sum([i.getCommerce() for i in self.getTownexpansionSlots()])

  def getPoints(self):
    return len(self.getSettlementSlots()) + (3 * len(self.getCitySlots()))

  #Given a list of list of resource slots, we spend them
  def spendResources(self, rescList):
    for rescType in rescList:
      for rescSlot in rescType:
        rescSlot.item.spendResc()

  def giveResources(self, rescList):
    for rescType in rescList:
      for rescSlot in rescType:
        rescSlot.item.giveResc()


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
  def __init__(self, princ, phases=None, slot=None):
    self.princ = princ

    self.phases = phases
    self.slot = slot

    self.strengthPoints = 0
    self.tourneyPoints = 0
    self.commercePoints = 0

  def getStrength(self):
    return self.strengthPoints

  def getTourney(self):
    return self.tourneyPoints

  def getCommerce(self):
    return self.commercePoints

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
      return "EmptySlot {0}".format(self.name)
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

  #We have our block where we initiate all of our actions
  #buildset = Action(Tags.BUILDSETTLEMENT, lambda x, y, z : len(x.getPhantomTownSlots) != 0 \
  #  and len(x.getResourceCombos(Tags.BUILDSETTLEMENTCOST)) != 0 and y == Tags.MAINPHASE)

  #buildcit = Action(Tags.BUILDCITY, lambda x, y, z: len(x.getSettlementSlots) != 0 \
  #  and len(x.getResourceCombos(Tags.BUILDCITYCOST)) != 0 and y == Tags.MAINPHASE)

  #buildroad = Action(Tags.BUILDROAD, lambda x, y, z: len(x.getPhantomRoadSlots) != 0 \
  #  and len(x.getResourceCombos(Tags.BUILDROADCOST)) != 0 and y == Tags.MAINPHASE)

  #action1 = [buildset, buildcit, buildroad]
  #action2 = [buildset, buildcit, buildroad]

  checkPlayer1 = RandomPlayer(None, None)
  checkPlayer2 = RandomPlayer(None, None)

  decks = []

  numberofPiles = 0

  firstTurn = 0

  actions = Tags.SIMPLEACTIONS

  #(self, decks, resourceCards, numberofPiles, principalities, firstTurn, actions)
  board = Board(decks, Tags.EXTRARESOURCES, numberofPiles, [None, None], firstTurn)

  princ1 = Principality(board, player1, checkPlayer1, Tags.DOMAIN1RESOURCES)
  princ2 = Principality(board, player2, checkPlayer2, Tags.DOMAIN1RESOURCES)

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

