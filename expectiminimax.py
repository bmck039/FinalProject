from util import Card
import util
from util import Suit
import random
import math
from players import PlayingClass

class ExpectiMiniMax(PlayingClass):
    def __init__(self) -> None:
        super()



    def play(rules, hand, state,plaerIndex) -> Card: #returns a valid move
       bestMoves= list()
       moves= list()
       for card in hand:
            moves.append((card,ExpectiMiniMax.evaluateMove(card,rules,state,plaerIndex)))
       maxScore = max(moves)
       for (card,score) in moves:
            if(maxScore == score):
                 bestMoves.append(card)
            return bestMoves       

            
    def probility(self,card,state):
        return 1/(52-(len(state['seenCards'])-len(self.hand)))
    def isTerminal(state):
         return len(state["seenCards"])== 52
    def play(rules, hand, state): #returns a valid move
        pass

def expectedMiniMax(state, depth,rule):