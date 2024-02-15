import util
import players

playersList = []
for i in range(4):
    playersList.append(players.RandomPlayer())

game = util.Game(util.Spades, playersList)

game.playTurn()