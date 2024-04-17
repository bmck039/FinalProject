import util
import players
import MCTS
# import expectiminimax
# import RL

import time

def play(rules, playerList):
    start = time.time()
    game = util.Game(rules, playerList)
    game.playUntilWin()
    # game.playTurn()
    score = game.state["scores"]
    end = time.time()
    print(f"round finished in {end - start:.6f} seconds")
    filename = playerList[0].playingClass.__name__ + "And" + playerList[2].playingClass.__name__ + "VS" + playerList[1].playingClass.__name__ + "And" + playerList[3].playingClass.__name__
    with open(filename + ".csv", "a+") as file:
        if(score[1] > score[0]):
            winner = 1
        else: winner = 0
        scoreDifference = score[1] - score[0]
        file.write(str(winner) + "," + str(scoreDifference) + "\n")

def tournament(rules, playerList, rounds):
    for i in range(rounds):
        print("running round", i)
        play(rules, playerList)

playersList = []
playersList.append(players.AIPlayer(players.RandomPlay))
playersList.append(players.AIPlayer(MCTS.MCTSPlay))
playersList.append(players.AIPlayer(players.RandomPlay))
playersList.append(players.AIPlayer(MCTS.MCTSPlay))
#creates a game with 4 AI players

tournament(util.Spades, playersList, 600)
# play(util.Spades, playersList)