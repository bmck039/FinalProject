import util
import players

playersList = []
for i in range(4):
    playersList.append(players.RandomPlayer())

#creates a game with 4 random players
game = util.Game(util.Spades, playersList)

game.playTurn()