import util
import players

playersList = []
for i in range(4):
    playersList.append(players.AIPlayer())

# playersList.append(players.AIPlayer())
#creates a game with 4 random players

bids0 = []
bids1 = []
bids2 = []
bids3 = []
game = util.Game(util.Spades, playersList)
# print(game.state["bids"])
# game.playTurn()