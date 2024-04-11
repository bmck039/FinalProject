import util
import players
import MCTS
import expectiminimax
import RL

def play(rules, playerList):
    game = util.Game(rules, playerList)
    print(game.state["bids"])
    game.playUntilWin()
    # game.playTurn()
    print(game.state["scores"])

def tournament(rules, playerList, rounds):
    for i in range(rounds):
        play(rules, playerList)

playersList = []
playersList.append(players.AIPlayer(players.RandomPlay))
playersList.append(players.AIPlayer(MCTS.MCTSPlay))
playersList.append(players.AIPlayer(players.RandomPlay))
playersList.append(players.AIPlayer(MCTS.MCTSPlay))
#creates a game with 4 AI players

play(util.Spades, playersList)