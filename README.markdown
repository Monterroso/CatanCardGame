# Catan Card Game

The goal of this project is to be able to run 
the catan card game with an AI trained with 
reinforcement learning. 

TODO: Finish base game
TODO: Create Web GUI for human players
TODO: Add expansions
TODO: Create AI to play

## Components

#### Board


The board contains all the information needed 
to run the game. It includes the principalities, 
and contains the functionality needed to run a game 
from start to finish 

### Principality

A principality contains all the information of a 
player's personal board and all information there

### Player

A player contains the logic needed to select actions
and choose items within various principalities

A player is assumed to only take an initiate valid 
actions, if a call asking for a resource is required
but the player does not have it, it is assumed they 
did not need it, and return None in that instance

### Slot

A slot is used to hold a game object within a player's 
principality, and links to other slots and an object if 
that object exists

### Piece

A piece is a game object, held within a slot, and contains
any functionality for that specific game object

### Action

An action has a name and function as to whether it can be 
performed. 


## Game Flow

Resource Lists are first created, with a number and resource

Then resource cards are added with the same format

Number of piles, the int for who has the first turn are set

Then create the board, with list of Nones as players

Then initiate the principalities, and set them

