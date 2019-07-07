from __future__ import annotations

import unittest

import Tags

import random

import json

from Slot import Slot, TownSlot, RoadSlot, ExpansionSlot, ResourceSlot

from Player import Player, RandomPlayer

from Piece import Piece, Town, Road, Expansion, Resource

from Principality import Principality


class Board:
  """A board contains the methods needed to run a game

  Start a game by initializing the board, and then by calling playGame
  """
  def __init__(self, decks: list, resourceCards: list, numberofPiles: int, principalities: list, firstTurn: int, mode: int):
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
  def canTradeResource(self, princ: Principality, resource: int) -> bool:
    """Checks if the player can trade a specific resource

    Given the type of resource, will the player be able
    to instigate a trade with the bank. 

    Args:
      princ (Princiaplity): The principality asking to trade
      resource (int): The resource we are trying to trade

    Returns:
      bool: Whether or not the trade can be completed
    """

    rescNeeded = self.getTradeRate(princ, resource)

    resourceList = [0 for _ in range(Tags.NUMRESOURCES)]
    resourceList[resource] = rescNeeded
    if princ.checkPlayer.selectResourceSlots(None, resourceList) != None:
      #princ.checkPlayer.selectHaveResourceSlot(None, resource)
      return True
    return False


  #Checks if a road can be built
  def canBuildRoad(self, princ: Principality) -> bool:
    """Checks if a road can be built by the principality

    Args:
      princ (Pricipality): The principality seeking to check 

    Returns:
      bool: Whether or not a road can be built
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

    #elif actionToTake in Tags.TRADETYPES:
    #  tradeamount = [0 for _ in Tags.NUMRESOURCES]
    #  tradeamount[actionToTake] = self.getTradeRate(currentPlayer.princ, Tags.RESCOURCELIST[actionToTake])
    #  resourcesToTrade = currentPlayer.selectResourceSlots(actionToTake, tradeamount)
    #  currentPlayer.princ.spendResources(resourcesToTade)
    #  slotToRecieve = currentPlayer.selectOpenResourceSlot(curentPlayer.princ)
    #  currentPlayer.princ.giveResources(slotToRecieve)

      
  

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
      highestThing (string): The attribute we want to get the highest of
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

    with open('templates/test.json', 'w') as outfile:  
      json.dump(info, outfile)

if __name__ == '__main__':
    unittest.main()