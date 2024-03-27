import random

from util import Card
from util import Suit
from players import PlayingClass

import stable_baselines3

class ExpectiMiniMax(PlayingClass):
    def __init__(self) -> None:
        super()

    def evaluateMove(discardPile: list[Card], move: Card):
        discardPile += [move]
        # TODO

    def play(rules, hand, state): #returns a valid move
        pass


    # def updateModel(state, action, reward):
