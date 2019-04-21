from enum import Enum

import Tags

#This is a board for python. 

#Buildable and unbuildable objects are strings, either "UNBUILDABLE" or the type name
#"UNBUILDABLE"
#"TOWNEXPANSION"
#"CITYEXPANSION"
#"ROAD"
#"TOWN"


#We shouldd list all of our tags

#####################
# Buildable Objects #
#####################

class Player:
  def __init__(self, board, princ):
    self.board = board

    self.princ = princ

  #Takes in a string of the action to be taken, along with the possible actions
  def getAction(self, actString, validActions):
    #returns the actionpair, along with an object of additional information. 
    pass

#Cards are a string, input to board is a list of all cards. 

#some function that partitions into decks? 

#We have the object which contains everything
#CardDefs is the tags for a card, the cards is the list of cards. 
#cards is a list of lists of the split decks. 
#
#A board has a list of decks, each deck is a list of cards
#A board contains a dictionary of card and their tags
#A board has both principalities
#A board contains a list of the discard pile
#A board contains the tokens used
#A board contains a variable to determine how many piles to have
#A board has a variable determining who's turn it is
#A board holds the players to the game
#A board has a list of values to be the dice production rolls
#A board has a list of values to be the dice action rolls
#A board has a list of values to be resolve rolls
#A board has a list of valid actions
#Valid actions are build road, settlement, city, action, discard, search randomly or pay search
class Board:
  def __init__(self, decks, resourceCards, cardDefs, numberofPiles, princ1, princ2, firstTurn, productionRolls, actionRolls, resolveRolls, actions):
    self.decks = decks
    self.cardDefs = cardDefs
    self.resourceCards = resourceCards
    self.numberofPiles = numberofPiles
    self.princ1 = princ1
    self.princ2 = princ2

    self.princ1.board = self
    self.princ2.board = self

    self.productionRolls = productionRolls
    self.actionRolls = actionRolls
    self.resolveRolls = resolveRolls
    self.actions = actions

    self.knightToken = Tags.KTOKEN
    self.commerceToken = Tags.CTOKEN
    
    self.currentTurn = firstTurn

    self.winner = None

#Leftness starts at 0 for the initial road, every possible slot to the left increases or decreases

#A town is a settlement or an city
#
#A town has pointers to the four resource tiles
#A town has pointers to four expansion slots
#A town has pointers to the two bordering roads
#A town has a variable for either city or settlement
#A town has a variable for leftness
#
#If a slot isn't filled, it holds a phantom object
#A town has an "unbuildable" object as expansion
class Town:
    def __init__(self, princ, townType):
      self.princ = princ

      self.townType = townType

      


#A resource is one of gold, ore, wheat, sheep, brick, wood
#
#A resource has pointers to two town slots
#A resource has a variable for the type of resource
#A resource has a variable to it's number
#A resource has a variable to how many resources it has
#A resource has a variable to whether or not it's on top
#A resource has a variable to indicate it's leftness
#A resource has a variable to indicate it's principality
#
#A resource linked to an unbuilt town slot has an "unbuildable" object as slot
class Resource:
  def __init__(self, princ, number, amount, resc, slot):
    self.slot = slot

    self.number = number
    self.amount = amount
    self.type = resc

    self.princ = princ

#An expansion is a unit or buliding, as dicated by whatever card is played
#
#An expansion has pointers to a town
#An expansion has a variable to indicate it's principality
class Expansion:
  def __init__(self, princ, name, tags, slot):
    self.princ = princ

    self.name = name
    self.tags = tags

    self.slot = slot

#A road is a road
#
#A road has a pointers to two towns
#A road has a variable indidicating how left it is
#A road has a variable to indicate it's principality
#
#A road next to an unbuilt town has a buildable town as a slot
class Road:
  def __init__(self, princ, slot):
    self.princ = princ

    self.slot = slot

#A principality has access of all of the items that the player currently controls and the object types
#
#A principality has a list of all buildables
#A principality has a list of all unbuildables
#A principality has a list of all expansions
#A principality has a list of all roads
#A principality has a list of all towns
#A principality has a list of all resources
#A principality has a list of all tokens
#A principality has a list of all the cards in their hand
#A principality has a variable for its player
#
#roads and towns will be ordered on leftness, since they are either added on the 
#right most or the left most, you either append them to beginning or the end.
#Resources are ordered from top and bottom according to position and leftness
#Expansions just have their leftness, but are not in leftness order. 
class Principality:
  def __init__(self, board, towns, tokens, handCards, player):
    self.board = board
    self.townSlots = towns 
    self.tokens = tokens
    self.handCards = handCards
    self.player = player


#A slot holds info for the type it holds, and a pointer to what it holds. 
class Slot:
  def __init__(self, princ, item):
    self.princ = princ

    self.item = item

  #removes the item and sets it to None
  def pop(self):
    temp = self.item

    self.item = None

    return temp
  
  def push(self, thing):
    temp = self.item

    self.item = thing

    return temp


    

class TownSlot(Slot):
  def __init__(self, princ, TL, TR, BR, BL, ups, downs, leftroad, rightroad):
    super(princ, None)

    #Link the resources
    self.topLeftSlot = TL
    self.topRightSlot = TR  
    self.bottomRightSlot = BR
    self.bottomLeftSlot = BL

    #Links the expantions
    self.upSlots = ups
    self.downSlots = downs

    #Sets the roads
    self.leftRoadSlot = leftroad
    self.rightRoad = rightroad

class RoadSlot(Slot):
  def __init__(self, princ, item, lefttown, righttown):
    super(princ, None)

    self.leftTownSlot = lefttown
    self.rightTownSlot = righttown

class ExpansionSlot(Slot):
  def __init__(self, princ, town):
    super(princ, None)

    self.townSlot = town

class ResourceSlot(Slot):
  def __init__(self, princ, leftTown, rightTown):
    super(princ, None)

    self.leftTownSlot = leftTown
    self.rightTownSlot = rightTown

######################################################################################
################################### Town Functions ###################################
######################################################################################

#Places a Town within a Town Slot
#
#Does not return
def setTown(townSlot, town):
  pass

#Builds a Town Slot given the parameters
#
#Returns the created Slot
def initTownSlot(princ, TLSlot, TRSlot, BRSlot, BLSlot, leftRoadSlot, rightRoadSlot, ups, downs):
  return None

#Builds a Town given the Town parameters.
#
#Returns the created Town
def initTown(princ, townType):
  return None

#Gets all the Expansions from a Town
#
#Returns a set of all Expansions
def getTownExpansions(townSlot):
  return None


######################################################################################
################################### City Functions ###################################
######################################################################################

#Upgrades the settlement into a City
#
#Does not return
def upgradeSettlement(settlement):
  pass

##########################################################################################
################################### Resource Functions ###################################
##########################################################################################

#Places a Resource within a Resource Slot
#
#Does not return
def setResource(resourceSlot, resource):
  pass

#Builds a Resource given the Resource parameters
#
#Returns the created Resource
def initResc(princ, number, amount, resc):
  return None

#Builds a Resource Slot given the parameters
# 
#Returns the created Resource Slot
def initRescSlot(princ, leftTownSlot, righTownSlot):
  return None

#Increments the Resource from the production Roll if roll matches
#
#Does not return
def rollResc(rolledNumber, resource):
  pass

#Increments the Resource from another source
#
#Does not return
def giveResc(resource):
  pass

######################################################################################
################################### Road Functions ###################################
######################################################################################

#Places the Road within a Road Slot
#
#Does not return
def setRoad(roadSlot, road):
  pass

#Builds a Road given the Road parameters
#
#Returns the created Road
def initRoad(princ):
  return None

#Builds a Road Slot given the parameters
#
#Returns the created Resource Slot
def initRoadSlot(princ, leftTownSlot, rightTownSlot):
  return None

###########################################################################################
################################### Expansion Functions ###################################
###########################################################################################

#Places the Expansion within a Expansion Slot
#
#Does not return
def setExpansion(expansionSlot, expansion):
  pass

#Removes the expansion from within a Expansion Slot
#
#Returns the removed expansion
def unsetExpansion(expansionSlot):
  return None

#Builds a Expansion given the Expansion parameters
#
#Returns the created Expansion
def initExpansion(princ, name, tags):
  return None

#Builds a Expansion Slot given the parameters
#
#Returns the Created Expansion Slot
def initExpansionSlot(princ, townSlot):
  return None


##############################################################################################
################################### Principality Functions ###################################
##############################################################################################

#Gets all the Roads from a Principality
#
#Returns a set of all the Roads
def getRoads(princ):
  return None

#Gets all the Towns from a Principality
#
#Returns a set of all the Towns
def getTowns(princ):
  return None

#Gets all the Settlements from a Principality
#
#Returns a set of all the Settlements
def getSettlements(princ):
  return None

#Gets all the Towns from a Principality
#
#Returns a set of all the Cities
def getCities(princ):
  return None

#Gets all the Expansions from a Principality
#
#Returns a set of all the Expansions
def getExpansions(princ):
  return None


#######################################################################################
################################### Board Functions ###################################
#######################################################################################

#Creates an initial principality
#
#Returns the created Principality
def initPrincipality(resourceList):
  return None


def buildSettlement(townSlot, isFirst):
  
  #If this is the first settlement, we want to add four resources
  if isFirst:
    topLeft = getResc(townSlot.princ, 1)
    topRight = getResc(townSlot.princ, 1)
    bottomRight = getResc(townSlot.princ, 1)
    bottomLeft = getResc(townSlot.princ, 1)

    #Given all the resources we initiate our settlement, initiated to left

    leftRoadSlot = Slot(townSlot.princ, Tags.ROAD, None)
    rightRoadSlot = Slot(townSlot.princ, Tags.ROAD, None)

    initSettlement(topLeft, topRight, bottomRight, bottomLeft, leftRoadSlot, rightRoadSlot, townSlot.princ)

    #We are then done
    return

  #Otherwise we get the orientation that we want. 

  #get the resources
  top = getResc(townSlot.princ)
  bottom = getResc(townSlot.princ)

  if townSlot.leftRoadSlot == None:
    leftRoadSlot = Slot(townSlot.princ, Tags.ROAD, None)
    topRight = townSlot.item.rightroad.item.rightTown.item.topRight
    bottomRight = townSlot.item.rightroad.item.rightTown.item.bottomRight
    

    initSettlement(top, topRight, bottomRight, bottom, leftRoad, borderroad, townSlot.princ)

  else:
    rightRoad = None
    initSettlement(borderroad.rightTown.topLeft, top, bottom, borderroad.rightTown.bottomLeft, borderroad, rightRoad, borderroad.princ)

  #We are then done


def initFirstSettlementSlot(princ, tl, tr, br, bl):
  

  #Given all the resources we initiate our settlement, initiated to left

  leftRoadSlot = Slot(townSlot.princ, Tags.ROAD, None)
  rightRoadSlot = Slot(townSlot.princ, Tags.ROAD, None)

  initSettlement(topLeft, topRight, bottomRight, bottomLeft, leftRoadSlot, rightRoadSlot, townSlot.princ)

  #We are then done
  return

def initSettlementSlot(princ, topResc, bottomResc, ):

#Takes a town slot, initiates a settlement there given the parameters
def _initSettlementSlot(princ, slot, topleft, topright, bottomright, bottomleft, leftroad, rightroad):

  leftRoadSlot = Slot(princ, Tags.ROADSLOT, leftroad)
  rightRoadSlot = Slot(princ, Tags.ROADSLOT, rightroad)

  up1 = Slot(princ, Tags.SETEXPANSION, None) 
  down1 = Slot(princ, Tags.SETEXPANSION, None) 

  up2 = Slot(princ, Tags.UNBUILDABLE, Tags.UNBUILDABLE) 
  down2 = Slot(princ, Tags.UNBUILDABLE, Tags.UNBUILDABLE) 

  TLSlot = Slot(princ, Tags.RESOURCE, topleft)
  TRSlot = Slot(princ, Tags.RESOURCE, topright)
  BRSlot = Slot(princ, Tags.RESOURCE, bottomright)
  BLSlot = Slot(princ, Tags.RESOURCE, bottomleft)

  newSettlement = Town(TLSlot, TRSlot, BRSlot, BLSlot, up1, up2, down1, down2, leftRoadSlot, rightRoadSlot, princ)

  #Set the tags of the resources
  topleft.rightTown = Slot(princ, Tags.SETTLEMENT, newSettlement)
  topright.leftTown = Slot(princ, Tags.SETTLEMENT, newSettlement)
  bottomright.leftTown = Slot(princ, Tags.SETTLEMENT, newSettlement)
  bottomleft.rightTown = Slot(princ, Tags.SETTLEMENT, newSettlement)

  if leftroad != Tags.ROADSLOT:
    leftroad.rightTown = Slot(princ, Tags.SETTLEMENT, newSettlement)
  if rightroad != Tags.ROADSLOT:
    rightroad.leftTown = Slot(princ, Tags.SETTLEMENT, newSettlement)

  #Add the new settlement to the principality. 
  princ.towns.add(Slot(princ, Tags.TOWN, newSettlement))

  return newSettlement

#Creates a resource
def createResc(princ, number, rescType, amount):
  resc = Resource(number, amount, rescType)

#Pops a single resource from the top, assigning it a number and an amount
#
#We get the two from the list, just the first two in the list, pop them both, and initiate them
#We then get the new up and bottom resource by some function (just shuffle the list)
#Initiates them as objects, and sets all of their slots ot unbuildable objects. 
#We return the two resources, as up, then bottom
def getResc(princ, amount=0):
  number = princ.board.resolverolls
  resc = princ.board.resourceCards.pop()

  return Resource(number, amount, resc, Tags.UNBUILDABLE, Tags.UNBUILDABLE, princ)

#Builds a road next to the border town. 
#
#initializes a road object
#sets the town's phantom road as this road, and adds the road as principality. 
def buildRoad(bordertown, orient, princ):

  #Determine orientation and then set the road in that location including its phantom
  if orient == Tags.LEFT:
    phantom = Slot(princ, Tags.SETTLEMENTSLOT, None)
    road = Road(phantom, bordertown, princ)
    bordertown.leftroad = Slot(princ, Tags.ROAD, road)
  else:
    phantom = Slot(princ, Tags.SETTLEMENTSLOT, None)
    road = Road(bordertown, phantom, princ)
    bordertown.leftroad = Slot(princ, Tags.ROAD, road)


#Builds a city at the select settlement
#
#Sets the town's variable to city
#set the two phantom expansion slots from unbuildable to buildable expansions
def buildCity(town):

  #Set towns tag to city, add city slots
  town.type = Tags.CITY
  town.up2.ptype = Tags.CITYEXPANSION
  town.down2.ptype = Tags.CITYEXPANSION

  #Check if there are previously any slots left open
  if town.up1 == Tags.SETEXPANSION:
    town.up1.ptype = Tags.CITYEXPANSION
  if town.down1 == Tags.SETEXPANSION:
    town.down1.ptype = Tags.CITYEXPANSION


#Builds an expansion of type card at the phantom location, from the town at location
#
#initiates the expansion with type, links it to the town, links the town to it
def buildExpansion(slot, card, tags, town, princ):
  #declare the expansion. 

  exp = Expansion(card, tags, town, princ)

  slot.item = exp

#Removes an expansion and sends it to the player's hand, then requires them to discard cards
#
#calls housekeeping remove expansion
#sends the card to the player's hand. 
def removeExpansion(slot):

  item = slot.item

  slot.item = None

  giveCard(item.name, slot.princ)
  
#Given a card, adds it to the player's hand
#
#gets the string, adds it to the list of player cards. 
def giveCard(card, princ):
  princ.cards.Add(card)

#Takes a list of slots, returns a list of the item
def getObjects(slots):
  return [i.item for i in slots]

#We get all of the resources within a principality
def getRescTiles(princ):
  rescs = set()

  #We get all of the resources
  for slot in princ.towns:
    town = slot.item
    rescs.add(town.topLeft)
    rescs.add(town.topRight)
    rescs.add(town.bottomRight)
    rescs.add(town.bottomLeft)

  return rescs

#Returns all the road slots. 
def getRoadSlots(princ):
  roadSlots = set()

  for slot in princ.towns:
    town = slot.item
    roadSlot.add(town.leftRoad)
    roadSlot.add(town.rightRoad)

  return roadSlots

#Returns all of the phantom road slots in a principality
def getRoadPhantoms(princ):
  phantoms = set()

  for slot in princ.towns:
    town = slot.item

    if town.leftRoad.item == None:
      phantoms.add(town.leftRoad)
    if town.rightRoad.item == None:
      phantoms.add(town.rightRoad)

  return phantoms

#Returns all of the phantom town slots in a pricipality
def getTownPhantoms(princ):
  phantoms = set()

  for slot in princ.towns:
    town = slot.item

    #check left and right roads to see if there are phantoms. 
    if town.leftRoad.item != None and town.leftRoad.item.leftTown.item == None:
      phantoms.add(town.leftRoad.item.leftTown)

    if town.rightRoad.item != None and town.rightRoad.item.rightTown.item == None:
      phantoms.add(town.rightRoad.item.rightTown)

#Returns all of the phantom Settlement expansions in s a principality
def getSettlementExpansionPhantoms(princ):
  phantoms = set()

  for slot in princ.towns:
    town = slot.item
    if town.up1.item == None:
      phantoms.add(town.up1)
    if town.up2.item == None:
      phantoms.add(town.up2)
    if town.down1.item == None:
      phantoms.add(town.down1)
    if town.down2.item == None:
      phantoms.add(town.down2)

  return phantoms

def getCityExpansionPhantoms(princ):
  phantoms = set()

  for slot in princ.towns:
    town = slot.item

    #check to make sure we have a city
    if town.type == Tags.CITY:
      if town.up1.item == None:
        phantoms.add(town.up1)
      if town.up2.item == None:
        phantoms.add(town.up2)
      if town.down1.item == None:
        phantoms.add(town.down1)
      if town.down2.item == None:
        phantoms.add(town.down2)    

def getPhantoms(princ, slottype):

  if slottype == Tags.TOWNEXPANSION:
    return getTownPhantoms(princ)

  if slottype == Tags.ROADSLOT:
    return getRoadPhantoms(princ)

  if slottype == Tags.SETTLEMENTSLOT:
    return getSettlementExpansionPhantoms(princ)

  if slottype == Tags.CITYEXPANSION:
    return getCityExpansionPhantoms(princ)



#Creates a principality 
#
#List is resources, going clockwise around the board
#creates the road, two towns, links those together and adds their respective phantoms
#Adds respective resources and links them to the settlements
def initPrincipality(board, listResc, player):
  #Creates initial road
  princ = Principality(board, [], set(), [], player)
  initroad = Road(Tags.SETTLEMENTSLOT, Tags.SETTLEMENTSLOT, princ)

  rescs = []
  for i in range(len(listResc)):
    rescs.append(Resource(listResc[i][1], 1, listResc[i][0],\
      Tags.UNBUILDABLE,Tags.UNBUILDABLE, princ))

  leftTown = initSettlement(rescs[0], rescs[1], rescs[4],\
    rescs[5], Tags.ROADSLOT, initroad, princ)

  rightTown = initSettlement(rescs[1], rescs[2], rescs[3],\
    rescs[4], initroad, Tags.ROADSLOT, princ)

  princ.towns.append(leftTown)
  princ.towns.append(rightTown)

  return princ


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