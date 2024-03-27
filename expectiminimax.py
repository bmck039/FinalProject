from util import Card
from util import Suit
from players import PlayingClass

class ExpectiMiniMax(PlayingClass):
    def __init__(self) -> None:
        super()

    def evaluateMove(discardPile: list[Card], move: Card, rules, state, playerIndex):
        for card in discardPile:
          result =   rules.compareCard(move,card) # if card does not win trick it is a bad move
          if result != 1:
              return -1
        if state["bids"][playerIndex]  >= state["tricks"][playerIndex]+1 : # if winning this trick puts the player over the bid number this is a bad move
            return 1 # good move  otherwise
        else:
            return -1

    def play(rules, hand, state) -> Card: #returns a valid move
        discardPile = state["discardPile"]
        playerIndex = len(discardPile)
