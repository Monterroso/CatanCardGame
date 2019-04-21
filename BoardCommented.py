from enum import Enum

#This is a board for python. 

#Buildable and unbuildable objects are strings, either "UNBUILDABLE" or the type name
#"UNBUILDABLE"
#"TOWNEXPANSION"
#"CITYEXPANSION"
#"ROAD"
#"TOWN"


#####################
# Buildable Objects #
#####################

#We have an enum of all of the cards
class Cards(Enum):
  def __init__(self):
    pass

#We have the object which contains everything
#
#A board has a list of decks, each deck is a list of cards
#A board has both principalities
#A board contains a list of the discard pile
#A board contains the tokens used
#A board contains a variable to determine how many piles to have
#A board contains variables to determine which tokens are used
#A board has a variable determining who's turn it is
#A board holds the players to the game
#A board has a list of values to be the dice production rolls
#A board has a list of values to be the dice action rolls
#A board has a list of values to be resolve rolls
#A board has a list of valid actions
#Valid actions are build road, settlement, city, action, discard, search randomly or pay search
class Board:
  def __init__(self):
    pass

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
    def __init__(self):
      pass

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
  def __init__(self):
    pass

#An expansion is a unit or buliding, as dicated by whatever card is played
#
#An expansion has pointers to a town
#An expansion has a variable to indicate it's principality
class Expansion:
  def __init__(self):
    pass

#A road is a road
#
#A road has a pointers to two towns
#A road has a variable indidicating how left it is
#A road has a variable to indicate it's principality
#
#A road next to an unbuilt town has a buildable town as a slot
class Road:
  def __init__(self):
    pass

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
class Principality:
  def __init__(self):
    pass


#################
#Board Functions#
#################
#
#These functions only manipulate the board

#Adds a settlement to a principality
#
#Given a road, it checks whether the left or right slot of the road is filled
#creates settlement, getting the up and down from the resource queue on side of settlement
#call setsettlement, links the road and four resources, and the four expands
#We get leftness from the borderroad
#If road has no settlements at all, defaults to add it to the left
def buildSettlement(borderroad):
  pass

#Initializes a settlement
#
#links the road and the four resources, and the resources to it, and set principality
#Make sure all are added to the principality
#Sets leftness to the resources and roads. 
def initSettlement(topleftresc, toprightresc, bottomleftresc, bottomrightresc, borderroad):
  pass

#Gets the top and bottom resource from the resource list, and links them to the principality
#
#We get the two from the list, just the first two in the list, pop them both, and initiate them
#We then get the new up and bottom resource by some function (just shuffle the list)
#We return the two resources, as up, then bottom
def getResc():
  pass

#Builds a road next to the border town. 
#
#initializes a road object
#sets the town's phantom road as this road, and adds the road as principality. 
def buildRoad(borderTown):
  pass

#Builds a city at the select settlement
#
#Sets the town's variable to city
#set the two phantom expansion slots from unbuildable to buildable expansions
def buildCity(town):
  pass

#Builds an expansion of type card at the phantom location, from the town at location
#
#initiates the expansion with type, links it to the town, links the town to it
def buildExpansion(loc, card, town):
  pass


#Removes an expansion and sends it to the player's hand, then requires them to discard cards
#
#calls housekeeping remove expansion
#sends the card to the player's hand. 
def removeExpansion(exp):
  pass

#Does all the housework to remove an expansion
#
#Sets the expansion to buildable from settlement
#removes it from the principality. 
def _removeExpansion(exp):
  pass

#Given a card, adds it to the player's hand
#
#gets the string, adds it to the list of player cards. 
def giveCard(card, princ):
  pass

#Creates a principality 
#
#List is resources, going clockwise around the board
#creates the road, two towns, links those together and adds their respective phantoms
#Adds respective resources and links them to the settlements
def initPrincipality(listResc):
  pass

#Allows the player to search a deck, and select any card from it
#
#Gives the player the list
#The player then returns a an index of that list for the card they want
#That card is then removed from the deck, and added to their hand
#The deck is then reshuffled. 
def searchDeck(deck):
  pass

#This shuffles the deck randomly
#
#Given this list, shuffles the list
def shuffle(deck):
  pass

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
def playGame():
  pass

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
def turn():
  pass

#When called, allows the player to have a mainphase action
#
#Sends player Board
#Player returns action, string of action, pool of resources, and card
#Call begin that specific action phase. 
#resolve action
#return true if action wasn't empty action, return false if was
def mainphase():
  pass

#A valid function determines when an action can be played
#
#If an action can be played in multiple ways, it should return all of them. 
#The returned actions, include the resources and cards spent on the action. 


#Signals to the players that a settlement is being built
#
#board is sent to players, sending the phantom settlement, along with the current board state
#each card has a valid function to determine if can be played
#Each card is searched with that valid function, list of valid actions are then sent to the player
def onSetBuild():
  pass

#Signals to the players that a road is being built
#
#board is sent to players, sending the phantom road, along with the current board state
#each card has a valid function to determine if it can be played
#Each card is searched with that valid function, list of valid actions are then sent to the player
def onRoadBuild():
  pass

#Signals to the players that a city is being built
#
#board is sent to players, sending the phantom city, along with the current board state
#each card has a valid function to determine if it can be played
#Each card is searched with that valid function, list of valid actions are then sent to the player
def onCityBuild():
  pass

#Signals to the players that an action is being played
#
#Actions cards differ, so board is sent to the player, as is the action card being played
#Each card has a valid function to determine if it can be played
#Each card is searched with that valid function, list of valid actions are then sent to the player
def onActionPlay():
  pass

#Singls to the players that a turn has started
def onTurnStart():
  pass

#Signals to the players that a mainphase turn has begun. 
def onMainPhase():
  pass

#Signals to the players that the endturn is occuring.
def onTurnEnd():
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
  pass

#Determines which player acts first in the case of a tie, based on board state
#
#Returns the player
def detPrior(board):
  pass

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
def rollProductionDice():
  pass

#Rolls the action dice
#
#Dice rolls are pregenerated before, this pops from the dice list
def rollActionDice():
  pass