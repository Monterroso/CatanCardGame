#This keep information about the game. 

WINPOINTS = 11

CTOKEN = "Commerce"
KTOKEN = "Knight"

TOURNEY = "Tourney"
COMMERCE = "Commerce"
STRENGTH = "Strength"

UNIT = "Unit"
FLEET = "Fleet"
KNIGHT = "Knight"
ACTION = "Action"
DEFENSE = "Defense"
OFFENSE = "Offense"

SETEXPANSION = "SettlementSlot"
CITYEXPANSION = "CitySlot"
ROADSLOT = "RoadSlot"
SETTLEMENTSLOT = "TownSlot"
CITYSLOT = "CitySlot"
UNBUILDABLE = "Unbuildable"

NUMRESOURCES = 6
RESOURCE = "Resource"
GOLD = 0
ORE = 1
BRICK = 2
WOOD = 3
WHEAT = 4
SHEEP = 5

RESCOURCELIST = [GOLD, ORE, BRICK, WOOD, WHEAT, SHEEP]

DOMAIN1RESOURCES = [(3, SHEEP), (6, GOLD), (5, BRICK),\
    (1, WHEAT), (4, WOOD), (2, ORE)]

DOMAIN2RESOURCES = [(5, WOOD), (2, WHEAT), (4, SHEEP),\
    (6, BRICK), (1, GOLD), (3, ORE)]

EXTRARESOURCES = [(2, WHEAT), (4, SHEEP), (6, BRICK),\
 (3, WHEAT), (3, GOLD), (6, SHEEP), (1, WOOD), (1, BRICK),\
 (5, ORE), (4, WHEAT), (2, BRICK), (6, WOOD), (4, ORE), (5, SHEEP)]

ROAD = "Road"
SETTLEMENT = "Settlement"
CITY =  "City"
TOWN = "Town"

#UP = "Up"
#UP2 = "Up2"
#DOWN = "Down"
#DOWN2 = "Down2"
#LEFT = "Left"
#RIGHT = "Right"

###########
# Actions #
###########

BUILDROAD = "BuildRoad"
BUILDSETTLEMENT = "BuildSettlement"
BUILDCITY = "BuildCity"
BUILDEXPANSION = "BuildExpansion"

CONSTRUCT = set([BUILDROAD, BUILDSETTLEMENT, BUILDCITY, BUILDEXPANSION])

TRADEGOLD = 0
TRADEORE = 1
TRADEBRICK = 2
TRADEWOOD = 3
TRADEWHEAT = 4
TRADESHEEP = 5

TRADETYPES = [TRADEGOLD, TRADEORE, TRADEBRICK, TRADEWOOD, TRADEWHEAT, TRADESHEEP]



################
# Action Costs #
################

BUILDROADCOST = [0,0,2,1,0,0]
BUILDSETTLEMENTCOST = [0,0,1,1,1,1]
BUILDCITYCOST = [0,3,0,0,2,0]

SIMPLEACTIONS = set([BUILDROAD, BUILDSETTLEMENT, BUILDCITY])

####################################
# Tags for all possible conditions #
####################################

MAINPHASE = "MainPhase"


#Now we have all of the individual tags for the cards