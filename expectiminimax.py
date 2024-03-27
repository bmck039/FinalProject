import random

from util import Card
from util import Suit
from players import PlayingClass


import stable_baselines3

class ExpectiMiniMax(PlayingClass):
    def __init__(self) -> None:
        super()

    def evaluateMove(discardPile: list[Card], move: Card,rules,state,player):
        for card in discardPile:
          result =   rules.compareCard(move,card) # if card does not win trick it is a bad move
          if result != 1:
              return -1
        if state["bids"][player]  >= state["tricks"][player]+1 : # if winning this trick puts the player over the bid number this is a bad move
            return 1 # good move  otherwise
        else:
            return -1

            
    
        # TODO
    def play(rules, hand, state): #returns a valid move
        pass


    # def updateModel(state, action, reward):
