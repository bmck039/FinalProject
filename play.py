import util
import players

import random

playersList = []
for i in range(4):
    playersList.append(players.AIPlayer(players.RandomPlay))

#creates a game with 4 AI players

game = util.Game(util.Spades, playersList)
print(game.state["bids"])
# game.playTurn()