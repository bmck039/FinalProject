from util import Card
from util import Suit
from players import PlayingClass

class MCTS(PlayingClass):

    def play(rules, hand, state) -> Card: #returns a valid move
        discardPile = state["discardPile"]
        playerIndex = len(discardPile)
