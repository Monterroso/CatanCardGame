
#This keeps all of the tags

WINPOINTS = 10

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
GOLD = "Gold"
ORE = "Ore"
BRICK = "Brick"
WOOD = "Wood"
WHEAT = "Wheat"
SHEEP = "Sheep"

RESCOURCELIST = [GOLD, ORE, BRICK, WOOD, WHEAT, SHEEP]

ROAD = "Road"
SETTLEMENT = "Settlement"
CITY =  "City"
TOWN = "Town"

UP = "Up"
UP2 = "Up2"
DOWN = "Down"
DOWN2 = "Down2"
LEFT = "Left"
RIGHT = "Right"

DRAWFROMDECK = "DrawFromDeck"
BUILDROAD = "BuildRoad"
BUILDSETTLEMENT = "BuildSettlement"
BUILDCITY = "BuildCity"

TURNCONTINUE = "TurnContinue"
TURNEND = "TurnEnd"
GAMEEND = "GameEnd"

SIMPLEACTIONS = [[BUILDROAD, [0,0,2,1,0,0], True], [BUILDSETTLEMENT, [0,0,1,1,1,1], True],\
     [BUILDCITY, [0,3,0,0,2,0], True]]

ACTIONS = set([DRAWFROMDECK, BUILDROAD, BUILDSETTLEMENT, BUILDCITY])


SCOUT = "Scout"

MAINPHASE = "MainPhase"

TRADE = "Trade"

#Now we have all of the individual tags for the cards