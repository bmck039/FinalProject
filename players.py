import random
import util
from util import Card
from util import Suit

class RandomPlayer(util.basePlayer):

    def __init__(self) -> None:
        super()

    def play(self, state: dict) -> Card:
        validMoves = self.rules.validMoves(self.hand, state)
        move = random.choice(validMoves)
        return move
    
    def getBid(self, state: dict) -> int:
        return random.randint(0, len(self.hand))

class AIPlayer(util.basePlayer):

    def __init__(self) -> None:
        super()

    def calcNilThreshold(regularTakes):
        return 25

    def calcRegularTakes(self, PT, hand, previousBids) -> int:
        tricks = 0

        #k/(13-n)

        highSpades = [Card(1, Suit.Spades), Card(13, Suit.Spades), Card(12, Suit.Spades), Card(11, Suit.Spades)] #ace, king, queen, jack
        subsetSpades = util.subsetOfSuit(hand, Suit.Spades)
        protectors = []
        for card in subsetSpades:
            if card not in highSpades: protectors.append(card)


        for card in highSpades:
            numProtectorsNeeded = 14 - card.value
            if card in hand and numProtectorsNeeded <= len(protectors):
                tricks += 1
                del protectors[:numProtectorsNeeded]
        
        if len(subsetSpades) > 4:
            tricks += len(subsetSpades) - 4
        #each additional spade is likely to be a trick
        
        return tricks


    def getBid(self, state: dict) -> int:
        previousBids = state["previousBids"]

        PT, SC = self.precomputeData(state)

        regularTakes = self.calcRegularTakes(PT, self.hand, previousBids)
        nilValue = self.calcNilValue(PT, self.hand)
        nilProb = SC(previousBids, nilValue)
        expNilScore = (nilProb - (1 - nilProb)) * 50
        nilThreshold = self.calcNilThreshold(regularTakes)

        return 0 if expNilScore > nilThreshold else regularTakes

    