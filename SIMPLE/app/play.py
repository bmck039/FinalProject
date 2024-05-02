import util

import players

import MCTS

# import expectiminimax

import RL



import os.path

import argparse

import time



def play(rules, playerList):

    start = time.time()

    game = util.Game(rules, playerList)

    game.playUntilWin()

    # game.playTurn()

    score = game.state["scores"]

    end = time.time()

    print(f"round finished in {end - start:.6f} seconds")

    filePath = "./output/"

    filename = playerList[0].playingClass.__name__ + "VS" + playerList[1].playingClass.__name__

    filename = filename + ".csv"

    filePath = os.path.join(filePath, filename)

    with open(filePath, "a+") as file:

        if(score[1] > score[0]):

            winner = 1

        else: winner = 0

        scoreDifference = score[1] - score[0]

        file.write(str(winner) + "," + str(scoreDifference) + "\n")



def tournament(rules, playerList, rounds):

    for i in range(rounds):

        print("running round", i)

        play(rules, playerList)



# playersList = []

# playersList.append(players.AIPlayer(players.RandomPlay))

# playersList.append(players.AIPlayer(RL.RLPlay))

# playersList.append(players.AIPlayer(players.RandomPlay))

# playersList.append(players.AIPlayer(RL.RLPlay))

#creates a game with 4 AI players

def parseAgent(agent):
    if(agent == "random"):
        return players.AIPlayer(players.RandomPlay)
    if(agent == "mcts"):
        return players.AIPlayer(MCTS.MCTSPlay)
    if(agent == "rl"):
        return players.AIPlayer(RL.RLPlay)
    raise NotImplementedError("We were unable to find the model {model}")

def playGames(args):
    playerList = []

    if(len(args.agents) != 4 or len(args.agents) != 2):
        raise ValueError("Incorrect number of models specified, must be 2 or 4")

    for agent in args.agents:
        playerList.append(parseAgent(agent))

    if(len(playerList) == 2):
        for agent in args.agents:
            playerList.append(parseAgent(agent))

    tournament(util.Spades, playerList, args.games)

def cli():
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=formatter_class)

    parser.add_argument("--agents","-a", nargs = '+', type=str, default = ['random', 'random', 'random', 'random']
                , help="Player Agents (random, mcts, rl)")
    
    parser.add_argument("--games", "-g", type = int, default = 1
                , help="Number of games to play)")
    
    args = parser.parse_args()

    # Enter main
    playGames(args)
    return



cli()