import probabilities
import util
from util import Card
from util import Suit

# import expectiminimax
from abc import ABC, abstractmethod
import random

class RandomPlayer(util.basePlayer): #plays randomly

    def __init__(self)        :
        super()

    def play(self, state      )        :
        validMoves = self.rules.validMoves(self.hand, state)
        move = random.choice(validMoves)
        return move
    
    def getBid(self, state      )       :
        return random.randint(0, len(self.hand))
    
class ActionPlayer(util.basePlayer): # only plays a given action, useful for simulating potential opponent moves
    def __init__(self, action)        :
        super().__init__()
        self.action = action
        self.hand = [action]

    def play(self, state):
        return self.action

# 0 (0.997) (0.966) (0.817)
# 1 0.994 (0.942) *** (0.733) **
# 2 0.990 0.907 (0.624)
# 3 0.983 0.855 0.489
# 4 0.970 0.779 0.350
# 5 0.948 0.678 * 0.212
# 6 0.915 0.544 0.095
# 7 0.857 0.381 0.025
# 8 0.774 0.214 0
# 9 0.646 0.074 0
# 10 0.462 0 0
# 11 0.227 0 0

probabilityTable = [
    [0.997, 0.996, 0.817],
    [0.994, 0.942, 0.733],
    [0.990, 0.907, 0.624],
    [0.983, 0.855, 0.489],
    [0.970, 0.779, 0.350],
    [0.948, 0.678, 0.212],
    [0.915, 0.544, 0.095],
    [0.875, 0.318, 0.025],
    [0.744, 0.214, 0],
    [0.646, 0.074, 0],
    [0.462, 0, 0],
    [0.227, 0, 0],
]

# def onePlyEval(rules: util.Rules, hand: list[Card], state: dict) -> Card:
#     validMoves = rules.validMoves(hand, state)
#     model = expectiminimax.CardPlayingAgent()

#     evaluations = []
#     for move in validMoves:
#         evaluations.append(model.evaluateMove(state["discardPile"], move))
    
#     maxEval = max(evaluations)
#     maxEvalIndex = evaluations.index(maxEval)

#     return validMoves[maxEvalIndex]

class PlayingClass(ABC): #interface for different methods of play

    @abstractmethod
    def play(rules, hand, state):
        pass

class RandomPlay(PlayingClass):
    def play(rules, hand, state):
        moves = rules.validMoves(hand, state)
        return random.choice(moves)

class AIPlayer(util.basePlayer):

    def __init__(self, playingClass              )        :
        super()
        self.playingClass = playingClass
    
    def getPrecomputedData(self, state      )                                      :
        learnedFunction = lambda x, y: x 
        return probabilityTable, learnedFunction
    
    def play(self, state      )        :
        return self.playingClass.play(self.rules, self.hand, state)
    
    def update(self, score     ):
        pass

    def calcNilThreshold(self, regularTakes):
        return 25
    
    def getTakesProb(self, suit, PT, numCards, cardIndex)         :
        if suit == Suit.Spades:
            return 1
        return PT[numCards][cardIndex]
        
    def getTricksFromSuit(self, PT, hand, suit, highSuitCards):
        tricks = 0
        subsetSuit = util.subsetOfSuit(hand, suit)
        numCards = len(subsetSuit)
        numProtectors = 0

        for cardValue in highSuitCards:
            card = Card(cardValue, suit)
            numProtectorsNeeded = 14 - card.value
            if(card.value == 1):
                numProtectorsNeeded = 0
            if card in hand and numProtectorsNeeded <= numProtectors:
                cardIndex = 0 if cardValue == 1 else (14 - card.value)
                tricks += self.getTakesProb(suit, PT, numCards, cardIndex)
                numProtectors -= numProtectorsNeeded #remove the number of protectors needed from the number of protectors
        # print(suit, tricks)
        return tricks

    def calcRegularTakes(self, PT, hand, previousBids)       :
        tricks = 0

        normalSpadeValue = 0
        suits = [Suit.Spades, Suit.Clubs, Suit.Diamonds, Suit.Hearts]
        for suit in suits:
            if suit == Suit.Spades:
                highSuitCards = [1, 13, 12, 11]
            else:
                highSuitCards = [1, 13, 12]
            numTricks = self.getTricksFromSuit(PT, hand, suit, highSuitCards)
            if suit == Suit.Spades: normalSpadeValue += numTricks
            else: tricks += numTricks

        subsetSpades = util.subsetOfSuit(hand, Suit.Spades)
        
        #considers whether you have a high number of spades
        if len(subsetSpades) > 4:
            normalSpadeValue += len(subsetSpades) - 4
        #each additional spade is likely to be a trick
            
        #short suit set values:
        totalReconsideredValue = self.reconsiderSpades(PT, hand, suits, subsetSpades)
        tricks += max(normalSpadeValue, totalReconsideredValue)

        diffFromAverage = 13/4 - tricks
        totalDistFromEqual = 13 - (tricks + sum(previousBids))
        weight1 = 1/2
        weight2 = 1/((4 - len(previousBids)) * 5)
        tricks += weight1 * diffFromAverage + weight2 * totalDistFromEqual

        return max(0, round(tricks))
    
    def calcNilValue(self, PT, hand):
        # Kind of hacky -- replaces probability table with big dictionary of precomputed values
        PT = probabilities.readFromFile()

        probNilForHand = 1
        voidSuitPresent = False
        for suit in util.Suit:
            # Create a sorted list of suit cards
            suitCards = sorted(util.subsetOfSuit(hand, suit), key=lambda x: util.Spades.offsetValue(x.asTuple()[0]))

            # If void, update the flag. Else, multiply in nil probability for suit cards
            if len(suitCards) >= 1: probNilForHand *= PT[str(suit)][str(util.Spades.binaryFromHandSubset(suitCards))]
            else: voidSuitPresent = True

        # Apply bonus if the player has a void suit
        if voidSuitPresent: 
            probNilForHand *= 1.15
        return probNilForHand

    def reconsiderSpades(self, PT, hand, suits, subsetSpades):
        totalReconsideredValue = 0
        for suit in suits:
            suitSubset = util.subsetOfSuit(hand, suit)
            numberSubset = len(suitSubset)
            if(numberSubset < 3): #if the player is short a suit, then reconsider trump
                reconsideredSpades = 0
                for i in range(len(suitSubset), 3):
                    if(len(subsetSpades) > 0):
                        totalReconsideredValue += self.getTakesProb(suit, PT, numberSubset, i)
                        reconsideredSpades += 1
                del subsetSpades[:reconsideredSpades]
        return totalReconsideredValue


    def getBid(self, state      )       :
        previousBids = state["bids"]
        #TODO: implement nil part of the algorithm

        PT, SC = self.getPrecomputedData(state)

        regularTakes = self.calcRegularTakes(PT, self.hand, previousBids)
        nilValue = self.calcNilValue(PT, self.hand)
        #nilProb = SC(previousBids, nilValue) Impossible without learning from real games
        nilProb = nilValue
        expNilScore = (nilProb - (1 - nilProb)) * 50
        nilThreshold = self.calcNilThreshold(regularTakes)

        return 0 if expNilScore > nilThreshold else regularTakes
        # return regularTakes

