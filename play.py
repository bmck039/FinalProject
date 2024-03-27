import util
import players

import random

def randomMove(rules, hand, state):
    moves = rules.validMoves(hand, state)
    return random.choice(moves)

playersList = []
for i in range(4):
    playersList.append(players.AIPlayer(randomMove))

#creates a game with 4 AI players

game = util.Game(util.Spades, playersList)
print(game.state["bids"])
# game.playTurn()