import unittest

import Tags

#This is a board for python. 

###################################################################################
################################### Game Pieces ###################################
###################################################################################

class Player:
  def __init__(self, board, princ):
    self.board = board

    self.princ = princ

  #Takes in a string of the action to be taken, along with the possible actions
  def getAction(self, actString, validActions):
    #returns the actionpair, along with an object of additional information. 
    pass

class Board:
  def __init__(self, decks, resourceCards, numberofPiles, princ1, princ2, firstTurn, actions):
    self.decks = decks
    self.resourceCards = resourceCards
    self.numberofPiles = numberofPiles
    self.princ1 = princ1
    self.princ2 = princ2

    self.actions = actions

    self.knightToken = Tags.KTOKEN
    self.commerceToken = Tags.CTOKEN
    
    self.currentTurn = firstTurn

    self.winner = None

  def getValidActions(self, princ):
    return None

class Town:
    def __init__(self, princ, townType, slot=None):
      self.princ = princ

      self.townType = townType

      self.slot = slot

    def upgradeSettlement(self):
      self.townType = Tags.CITY


class Resource:
  def __init__(self, princ, number, amount, resc, slot=None):
    self.princ = princ

    self.number = number
    self.amount = amount
    self.resource = resc

    self.slot = slot
  
  def rollResc(self, rolledNumber):
    if rolledNumber == self.number and self.amount < 3:
      self.amount += 1

  def giveResc(self):
    if self.amount < 3:
      self.amount += 1

class Expansion:
  def __init__(self, princ, name, tags, slot=None):
    self.princ = princ

    self.name = name
    self.tags = tags

    self.slot = slot

class Road:
  def __init__(self, princ, slot=None):
    self.princ = princ

    self.slot = slot

class Principality:
  def __init__(self, board, player, resourceList):

    self.board = board
    self.townSlots = set() 
    self.tokens = set()
    self.handCards = []
    self.player = player

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
      leftTown = Town(self, Tags.SETTLEMENT),
      leftTownSlot = TownSlot(self, rescSlots[0], rescSlots[1], rescSlots[4],\
        rescSlots[5], None, initialRoadSlot, [], [])

      leftTownSlot.setItem(leftTown)

      #Create the right settlement
      rightTown = Town(self, Tags.SETTLEMENT)
      rightTownSlot = TownSlot(self, rescSlots[1], rescSlots[2], rescSlots[3],\
      rescSlots[4], initialRoadSlot, None, [], []) 

    rightTownSlot.setItem(rightTown)

  def getRoadSlots(self):
    roadSlots = set()
    for town in self.getTownSlots():
      for road in town.getTownRoadSlots():
        roadSlots.add(road)
    return roadSlots

  def getTownSlots(self):
    return self.townSlots

  def getSettlementSlots(self):
    return set([i for i in self.townSlots if i.item.townType == Tags.SETTLEMENT])

  def getCitySlots(self):
    return set([i for i in self.townSlots if i.item.townType == Tags.CITY])

  def getExpansionSlots(self):
    expansionSlots = set()
    for town in self.getTownSlots():
      for section in town.getTownExpansionSlots():
        for slot in section:
          expansionSlots.add(slot)
    return expansionSlots

  def getRoadBuildLocations(self):
    return set([i for i in self.getRoadSlots() if i.item == None])

  def getSettlementBuildLocations(self):
    return set([i for i in self.getTownSlots() if i.item == None])

  def getTownExpansionBuildLocations(self):
    return set([i for i in self.getExpansionSlots() if i.item == None])

  def getCityExpansionBuildLocations(self):
    return set([i for i in self.getExpansionSlots() if i.item == None and i.townSlot.item.townType == Tags.CITY])

  def getResourceCombos(self, resourceList):
    return None

  def getSingleResourceCombos(self, resourceAmount, resourceType):
    return None
  
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
  def __init__(self, princ, TL, TR, BR, BL, ups, downs, leftRoad, rightRoad):
    super().__init__(princ, None)

    #Link the resources
    self.topLeftSlot = TL
    self.topRightSlot = TR  
    self.bottomRightSlot = BR
    self.bottomLeftSlot = BL

    #Links the expantions
    self.upSlots = ups
    self.downSlots = downs

    #Sets the roads
    self.leftRoadSlot = leftRoad
    self.rightRoad = rightRoad

    #Pair the slots to this town
    TL.rightTown = self
    BL.rightTown = self

    TR.leftTown = self
    TL.leftTown = self


    #sets the left Road Slot
    if leftRoad != None:
      leftRoad.rightTown = self
    else:
      slot = RoadSlot(princ, None, self)
      self.leftRoadSlot = slot

    #sets the right Road Slot
    if rightRoad != None:
      rightRoad.leftTown = self
    else:
      slot = RoadSlot(princ, self, None)
      self.rightRoadSlot = slot

    #sets the up Slots
    if len(ups) == 0:
      self.upSlots.append(ExpansionSlot(princ, self))
      self.upSlots.append(ExpansionSlot(princ, self))

    #sets the down Slots
    if len(downs) == 0: 
      self.downSlots.append(ExpansionSlot(princ, self))
      self.downSlots.append(ExpansionSlot(princ, self))


    #Adds the slot to our list of town slots
    princ.townSlots.add(self)

  def getRoadSlots(self):
    return [self.leftRoadSlot, self.leftRoadSlot]

  def getTownExpansionSlots(self):
    return [self.upSlots, self.downSlots]

class RoadSlot(Slot):
  def __init__(self, princ, lefttown, righttown):
    super().__init__(princ, None)

    self.leftTownSlot = lefttown
    self.rightTownSlot = righttown

class ExpansionSlot(Slot):
  def __init__(self, princ, town):
    super().__init__(princ, None)

    self.townSlot = town

class ResourceSlot(Slot):
  def __init__(self, princ, leftTown, rightTown):
    super().__init__(princ, None)

    self.leftTownSlot = leftTown
    self.rightTownSlot = rightTown


######################################################################################
################################### Slot Functions ###################################
######################################################################################

#Adds the item to the slot
#
#Does not return


#Removes the item from the slot
#
#Returns the removed item



######################################################################################
################################### Town Functions ###################################
######################################################################################

#Places a Town within a Town Slot
#
#Does not return


#Builds a Town Slot given the parameters, and links all the items to this town
#
#Returns the created Slot


#Gets all the Expansions from a Town
#
#Returns a pair of expansions, ups and downs



######################################################################################
################################### City Functions ###################################
######################################################################################

#Upgrades the settlement into a City
#
#Does not return

##########################################################################################
################################### Resource Functions ###################################
##########################################################################################

#Places a Resource within a Resource Slot
#
#Does not return


#Builds a Resource given the Resource parameters
#
#Returns the created Resource

#Builds a Resource Slot given the parameters
# 
#Returns the created Resource Slot


#Increments the Resource from the production Roll if roll matches
#
#Does not return


#Increments the Resource from another source
#
#Does not return


######################################################################################
################################### Road Functions ###################################
######################################################################################

#Places the Road within a Road Slot
#
#Does not return

#Builds a Road given the Road parameters
#
#Returns the created Road

#Builds a Road Slot given the parameters
#
#Returns the created Resource Slot

###########################################################################################
################################### Expansion Functions ###################################
###########################################################################################

#Places the Expansion within a Expansion Slot
#
#Does not return


#Removes the expansion from within a Expansion Slot
#
#Returns the removed expansion


#Builds a Expansion given the Expansion parameters
#
#Returns the created Expansion

#Builds a Expansion Slot given the parameters
#
#Returns the Created Expansion Slot


##############################################################################################
################################### Principality Functions ###################################
##############################################################################################

#Creates an initial principality
#
#Returns the created Principality


#Gets all the Roads from a Principality
#
#Returns a set of all the Roads


#Gets all the Towns from a Principality
#
#Returns a set of all the Towns


#Gets all the Settlements from a Principality
#
#Returns a set of all the Settlements


#Gets all the Towns from a Principality
#
#Returns a set of all the Cities


#Gets all the Expansions from a Principality
#
#Returns a set of all the Expansions


#Gets all the Road Slots that can be build from a Principality
#
#Returns a set of all the empty Road Slots


#Gets all the Town Slots that can be built from a Principality
#
#Returns a list of all the emtpy Town Slots


#Gets all the Town ExpansionSlots that can be built
#
#Returns a set of all empty Town Expansion Slots


#Gets all the City Expansion Slots that can be built
#
#Returns a set of all empty City Expansion Slots

#Gets all the valid actions of the principality
#
#Returns a set of all valid actions


#Gets a set of lists of possible ways to get a number of required Resources
#
#Returns a set of lists of the resource Slots


#Gets a set of lists of possible ways to get a number of a single Resource



#######################################################################################
################################### Board Functions ###################################
#######################################################################################

#Creates a standardBoard
#
#returns the created board
def initSimpleBoard(player1, player2):
    decks = []

    rescList1 = [(3,Tags.SHEEP), (6, Tags.GOLD), (5, Tags.BRICK),\
      (2, Tags.ORE), (4, Tags.WOOD), (1, Tags.WHEAT)]

    rescList2 = [(5, Tags.WOOD), (2, Tags.WHEAT), (4, Tags.SHEEP),\
      (3, Tags.ORE), (1, Tags.GOLD), (6, Tags.BRICK)]

    resourceCards = [(1, Tags.BRICK), (1, Tags.WOOD), (2, Tags.WHEAT), (2, Tags.ORE)]

    numberofPiles = 0

    firstTurn = player1

    actions = set([Tags.BUILDROAD, Tags.BUILDSETTLEMENT, Tags.BUILDCITY])

    board = Board(decks, resourceCards, numberofPiles, None, None, firstTurn, actions)

    princ1 = Principality(board, player1, rescList1)
    princ2 = Principality(board, player2, rescList2)

    board.princ1 = princ1
    board.princ2 = princ2

    return board

############################################################################################
################################### Visualizer Functions ###################################
############################################################################################  

#This will, given a board, visualize it in text
#
#does not return
def visualizeTown(townSlot):
  pass

"""
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
  
def getRescCombinations(princ, rescList):
  #We first get all of our resource tiles
  tiles = getObjects(getRescTiles(princ))

  listings = [[],[],[],[],[],[]]
  
  for resource in tiles:
    for i in range(6):
      if resource.type == Tags.RESCOURCELIST[i]:
        listings[i].append(resource)

  for i in range(6):
    listings[i] = _getSingleResourceCombination(rescList[i], listings[i])

  #We return all possibilities now. 
  return _getCombos(listings)


#Gets all possible combintations of the elements. 
def _getCombos(listings):
  total = []

  cur = listings.pop()
  for rescs in cur:

    if len(listings) != 0:
      recurse = _getCombos(listings)
      
      for item in recurse:
        item.append(rescs)
        total.append(item)

    else:
      total.append(rescs)

  return total




def _getSingleResourceCombination(amount, resources):
  #Take a single resource out of the list, return either zero, one, two, three

  #Base is when it turns out of tiles and there aren't enough resources
  #Or when the resource cap is reached. 

  tilesUsed = []

  tile = resources.pop()

  amountLeft = sum([i.amount for i in resources])

  for tileResc in range(tile.amount + 1):
    #We append the amount of resources to the list of used.
     if amount - tileResc > 0 and amountLeft + tileResc >= amount:
        
        recurse = []
        if len(resources) != 0:
          recurse = _getSingleResourceCombination(amount - tileResc, resources)
        else:
          return [[i for i in range(tileResc)]]     
        
        for _ in range(tileResc):
          for element in recurse:
            element.append(tile)
            tilesUsed.append(element)

  return tilesUsed
        



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
    board = initSimpleBoard("player1", "player2")

    #Build a settlement for player1
    princ1 = board.princ1

    roadCons = princ1.getRoadBuildLocations()

    roadCon = roadCons.pop()

    self.assertTrue(len(roadCons) == 1)

    road = Road(princ1)

    roadCon.setItem(road)



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