from __future__ import annotations

import unittest

import Tags

import json

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


