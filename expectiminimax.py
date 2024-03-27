from util import Card
from util import Suit
from players import PlayingClass

class ExpectiMiniMax(PlayingClass):
    def __init__(self) -> None:
        super()

    def evaluateMove(discardPile: list[Card], move: Card):
        discardPile += [move]
        # TODO

    def play(rules, hand, state) -> Card: #returns a valid move
        discardPile = state["discardPile"]
        playerIndex = len(discardPile)
