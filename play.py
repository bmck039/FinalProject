import util
import players
import MCTS

import random

playersList = []
for i in range(3):
    playersList.append(players.AIPlayer(players.RandomPlay))
playersList.append(players.AIPlayer(MCTS.MCTSPlay))

#creates a game with 4 AI players

game = util.Game(util.Spades, playersList)
print(game.state["bids"])
game.playTurn()