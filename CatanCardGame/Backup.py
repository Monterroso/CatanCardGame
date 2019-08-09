from __future__ import annotations

import unittest

import Tags

from collections import deque

import random

import pdb

import json

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


  def __repr__(self) -> str:
    return "{0}".format(self.name)

  def getAction(self, phase, actionPerformed=None) -> str:
    """Given the current phase and the action taken by the main player, return the action string

    Args:
      phase (string) phase this is occuring in
      actionPerformed (string) action that the main player (if present) took

    Returns:
      string action this player chooses to perform, none if can't or chooses not to
    """

    return None

  def selectPlayer(self, phase, actionPerformed=None) -> Player:
    """Given the current phase and the action taken by the main player, return the chosen player

    Args:
      phase (string) phase this is occuring in
      actionPerformed (string) action that the main player (if present) took

    Returns:
      player player who should be chosen, or none if not possible
    """

    return None

  def selectResourceSlots(self, phase, resourceTypes, actionPerformed=None) -> list:
    """Given the current phase and the action taken by the main player, selects resource slots

    The slots that are selected can be selected multiple times, though it must have
    the number of resources to support being selected for that many times. 

    Args:
      phase (string) phase this is occuring in
      resourceTypes(list) list of resources that need to be chosen
      actionPerformed (string) action that the main player (if present) took

    Returns:
      list list of slot resources to be chosen
    """

    return None

  def selectOpenResourceSlots(self, phase, resourceType=None, actionPerformed=None) -> list:
    """Given the current phase and the action taken by the main player, selects resource slots

    All resource slots chosen must have less than 3 resources in them. Returns None
    if this action is not possible. Can select a slot multiple times, it can be added as 
    long as selecting it multiple times would not cause the slot to have 3 resources. If 
    resourceType array is None, you select any single OpenResource

    Args:
      phase (string) phase this is occuring in
      resourceTypes(list) list of resources that need to be chosen
      actionPerformed (string) action that the main player (if present) took

    Returns:
      list list of slot resources to be chosen
    """

    return None

  def selectHaveResourceSlot(self, phase, resourceType=None, actionPerformed=None) -> list:
    """Given the current phase and the action taken by the main player, selects resource slots

    All resource slots chosen must have more than 0 resources in them. Returns None
    if this action is not possible. Can select the same slot multiple times, as long as 
    selecting a slot multiple times would not reduce a slot to 0 resources. If no resource
    type array is given, then select any Have resource slot. 

    Args:
      phase (string) phase this is occuring in
      resourceTypes(list) list of resources that need to be chosen
      actionPerformed (string) action that the main player (if present) took

    Returns:
      list list of slot resources to be chosen
    """

    return None

  def selectOpenRoadSlot(self, phase, actionPerformed=None) -> RoadSlot:
    """Selects a valid slot to build a road

    Args:
      phase (string) phase this is occuring in
      actionPerformed (string) action that the main player (if present) took

    Returns:
      RoadSlot road slot that is empty, None if there is none
    """

    return None

  def selectOpenSettlementSlot(self, phase, actionPerformed=None) -> TownSlot:
    """Selects a valid slot to build a settlement

    Args:
      phase (string) phase this is occuring in
      actionPerformed (string) action that the main player (if present) took

    Returns:
      TownSlot town slot that is empty, None if there is none
    """
    return None

  def selectSettlementSlot(self, phase, actionPerformed=None) -> TownSlot:
    """Selects a valid slot to build a city

    Args:
      phase (string) phase this is occuring in
      actionPerformed (string) action that the main player (if present) took

    Returns:
      TownSlot town slot that has a settlement, None if there is none
    """

    return None

  def selectCard(self, phase, deck, actionPerformed=None) -> str:
    """Selects a valid slot to build a city

    Args:
      phase (string) phase this is occuring in
      deck (list) list of strings where one is to be chosen
      actionPerformed (string) action that the main player (if present) took

    Returns:
      string card from the deck that is intended to be selected. 
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
  def __init__(self, decks, resourceCards, numberofPiles, principalities, firstTurn, mode):
    self.decks = decks
    self.resourceCards = [i for i in resourceCards]
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

    #StoredInfo is a list of turn infos
    self.storedInfo = {}
    self.currentTurnInfo = None

    self.turnNum = 0
    
  ###############
  # Can Perform #
  ###############
  #
  #This block is dedicated to functions that check if actions can be performed

  #Checks if a player can trade
  def canTradeResource(self, princ, resource) -> bool:
    """Checks if the player can trade a specific resource

    Given the type of resource, will the player be able
    to instigate a trade with the bank. 

    Args:
      princ (Princiaplity) principality asking to trade
      resource (int) resource we are trying to trade

    Returns:
      bool or not the trade can be completed
    """

    rescNeeded = self.getTradeRate(princ, resource)

    resourceList = [0 for _ in range(Tags.NUMRESOURCES)]
    resourceList[resource] = rescNeeded
    if princ.checkPlayer.selectResourceSlots(None, resourceList) != None:
      #princ.checkPlayer.selectHaveResourceSlot(None, resource)
      return True
    return False


  #Checks if a road can be built
  def canBuildRoad(self, princ) -> bool:
    """Checks if a road can be built by the principality

    Args:
      princ (Pricipality) principality seeking to check 

    Returns:
      bool or not a road can be built
    """

    return len(princ.getPhantomRoadSlots()) != 0 and \
      princ.checkPlayer.selectResourceSlots(None, Tags.BUILDROADCOST)\
       and self.numRoads > 0


  #Checks if a settlement can be built
  def canBuildSettlement(self, princ) -> bool:
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

    #Check the sides and update them if need be. 
    if roadSlot.location[1] < princ.leftMostSlotNumber:
      princ.leftMostSlotNumber -= 1 
    if roadSlot.location[1] > princ.rightMostSlotNumber:
      princ.rightMostSlotNumber += 1 


  #Builds a settlement at the desired location
  def buildSettlement(self, princ, townSlot):
    #pop the two resources
    topRaw = self.resourceCards.pop()

    bottomRaw = self.resourceCards.pop()

    townSlot.expand(princ, topRaw, bottomRaw)

    self.numTowns -= 1

    #Check the sides and update them if need be. 
    if townSlot.location[1] < princ.leftMostSlotNumber:
      princ.leftMostSlotNumber -= 1 
    if townSlot.location[1] > princ.rightMostSlotNumber:
      princ.rightMostSlotNumber += 1 

  #Builds a city at the desired location
  def buildCity(self, princ, townSlot):
    townSlot.item.upgradeSettlement()
    self.numCities -= 1

  #Builds an expantion at the desired location
  def buildExpansion(self, princ, expansion, expansionSlot):
    expansionSlot.setItem(expansion)

  def perform(self, actionToTake, playerResponses):
    """This function sends players info given their responses

    TODO actions

    Given the actions and player responses, all steps and responses
    are sent to the player and carried out. The usual steps are given an action

    Ask for resources from the player
    Get the respective slots from the player, then create the thing
    Spend the resources

    Args:
        actionToTake (string) action the currrent player seeks to perform
        playerResponses (List) list in order of priority of player's responses to the action

    """

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
    while self.turnNum < 200:
      self.currentTurnInfo = {"Actions":[], "Player":self.getCurrentPlayer().name, "Princ":[]}
      self.takeTurn()
      self.storedInfo[self.turnNum] = self.currentTurnInfo

      if self.checkWin() == True:
        return self.winner

      self.turnNum += 1
      self.getNextPlayer()

     

    #In case we hit the turn limit
    return None

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

      self.currentTurnInfo["Actions"] = playerAction
      self.currentTurnInfo["Princ"] = self.getCurrentPlayer().princ.getInfo()

      #We check if the player action is valid, and isn't None, if it is we continue
      if playerAction == None:
        #If it's nothing, we don't need to do anything and can safetly return
        return
      
      #Add the action to our list of what is happening, won't get to this if action is none
      #We will impliment the get player response actions later, for now we just get the player action
      #playerResponses = getPlayerResponseActions(actionToTake,phase=Tags.MAINPHSE)
      playerResponses = None

      #Now we perform said action
      self.perform(playerAction, playerResponses)

      #set the winner if there is one
      self.setWin()

      if self.checkWin() == True:
        return

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
      roll = random.randint(0, 5)
      self.currentTurnInfo["ProductionRoll"] = roll
    else:
      roll = self.nextProductionRoll
      self.nextProductionRoll = None

    #Now we go through each player and tag their principalities
    for princ in self.principalities:
      princ.rollResources(roll)


  #Only either a year of plenty or "Null", impliment this later
  def rollActionDice(self):
    roll = None
    if self.nextActionRoll == None:
      roll = random.randint(0,5)
      self.currentTurnInfo["ActionRoll"] = roll
    else:
      roll = self.nextActionRoll
      self.nextActionRoll = None
 
    #Tournament Roll
    if roll == 1:
      #Check to see who has the highest tournament value. 
      winner = self.getHighestTournament()

      if winner != None:
        #We give them the phase to choose a resource from winning
        
        #Winner then selects slots to win for the tournament
        resourceSlot = winner.selectOpenResourceSlot(Tags.WINTOURNAMENT, Tags.RESOURCELIST)

        #Now you want to assign those resources
        if resourceSlot != None:
          resourceSlot.item.giveResc()

    #Commerce Roll
    elif roll == 2:
      #Check to see who has the highest commerce value.
      winner = self.getHighestCommerce()

      if winner != None:
        victim = winner.selectPlayer(Tags.WINCOMMERCE, self.getOtherPlayers(winner))

        

        winSlot = winner.selectOpenResourceSlot(Tags.WINCOMMERCE, victom.getOpenResources())
        #selectResourceSlot(self, phase, resourceTypes)

        loseSlot = victim.selectResourceSlot(Tags.LOSECOMMERCE, set(slot.item.resource))



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
      highestThing (string) attribute we want to get the highest of
    """
    highestPlayer = None
    highestAmount = 0
    for player in self.getPriorityOrder():
      amount = getattr(player.princ, highestThing)()
      if amount > highestAmount:
        highestAmount = amount
        highestPlayer = player
      elif amount == highestAmount:
        highestPlayer = None

    return highestPlayer

  def getPlayerResponseActions(self, incAction, phaseType):
    return [i.getAction(incAction, phaseType) for i in self.getPriorityOrder()]

  #Returns the player with the highest Tournament Value
  def getHighestTournament(self):
    return self.getHighest("getTourney")

  #Returns the player with the highest Strength value
  def getHighestStrength(self):
    return self.getHighest("getStrength")

  #Returns the player with the highest Commerce Value
  def getHighestCommerce(self):
    return self.getHighest("getCommerce")
  
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
    """This is a player's own personal board

    The principality starts out by having the coordinates initiated and the 
    empty slots placed in the correct places. 

    Args:
      board (Board) board that contains the game
      player (Player) Player agent that makes decisions
      checkPlayer (Player) agent that is able to determine what actions are possible
      resourceList (list) list of resources
    """

    self.board = board

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
    player.board = board

    checkPlayer.princ = self
    checkPlayer.board = board

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

  def getStrength(self) -> int:
    """Gets the tourney points of this piece

    Returns:
      int value of this piece
    """

    return self.strengthPoints

  def getTourney(self) -> int:
    """Gets the tourney points of this piece

    Returns:
      int value of this piece
    """

    return self.tourneyPoints

  def getCommerce(self) -> int:
    """Gets the commerce points of this piece

    Returns:
      int value of this piece
    """

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
      princ (Principality) principality that will be expanding
      Top (Resource) resource we want to add to the top slot
      Bottom (Resource) resource we want to add to the bottom slot
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



#######################################################################################
################################### Board Functions ###################################
#######################################################################################

#Creates a standardBoard
#
#returns the created board
def initSimpleBoard(player1, player2):

  checkPlayer1 = RandomPlayer(None, None)
  checkPlayer2 = RandomPlayer(None, None)

  decks = []

  numberofPiles = 0

  firstTurn = 0

  #(self, decks, resourceCards, numberofPiles, principalities, firstTurn, actions)
  board = Board(decks, Tags.EXTRARESOURCES, numberofPiles, [None, None], firstTurn, Tags.POST)

  princ1 = Principality(board, player1, checkPlayer1, Tags.DOMAIN1RESOURCES)
  princ2 = Principality(board, player2, checkPlayer2, Tags.DOMAIN1RESOURCES)

  board.principalities[0] = princ1
  board.principalities[1] = princ2

  return board

def playSimpleGame():
  player1 = RandomPlayer(None, None)
  player2 = RandomPlayer(None, None)
  board = initSimpleBoard(player1, player2)    
  winner = board.playGame()

  #Here we want to write to a JSON file
  return board.storedInfo

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
    info = playSimpleGame()

    with open('templates/test.json', 'w') as outfile 
      json.dump(info, outfile)

if __name__ == '__main__':
    unittest.main()

