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

            
    
    def play(rules, hand, state): #returns a valid move
        pass


    # def updateModel(state, action, reward):


def ExpectimaxAgent(gameState):
 
        value, move = maxValue(gameState, 0, 0)
        return move
        
def maxValue(self, gameState, depth, turn):
        agentIndex = turn % gameState.getNumAgents()
        if (gameState.isWin() or (depth > (self.depth * gameState.getNumAgents()) - 1) or gameState.isLose()):
            return self.evaluationFunction(gameState), None
        v = float("-inf")
        move = None
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            v2, a2 = self.maxOrMin(successor, depth + 1, turn + 1)
            if v2 > v:
                v, move = v2, action
        return v, move
    
def minValue(self, gameState, depth, turn):
        agentIndex = turn % gameState.getNumAgents()
        if (gameState.isWin() or (depth > (self.depth * gameState.getNumAgents()) - 1) or gameState.isLose()):
            return self.evaluationFunction(gameState), None
        v = float("inf")
        move = None
        numSuccessors = 0
        total = 0
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            v2, a2 = self.maxOrMin(successor, depth + 1, turn + 1)
            total += v2
            numSuccessors += 1
        return (1/numSuccessors)*total, move
    
def maxOrMin(self, gameState, depth, turn):
        agentIndex = turn % gameState.getNumAgents()
        if agentIndex == 0:
            return self.maxValue(gameState, depth, turn)
        else:
            return self.minValue(gameState, depth, turn)
        util.raiseNotDefined()