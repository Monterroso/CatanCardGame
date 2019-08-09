from __future__ import annotations

import unittest

import Tags

import random

import json

from Slot import Slot, TownSlot, RoadSlot, ExpansionSlot, ResourceSlot


from Piece import Piece, Town, Road, Expansion, Resource


##This is a board for python. 

####################################################################################
#################################### Game Parts ###################################
####################################################################################

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



if __name__ == '__main__':
    unittest.main()
