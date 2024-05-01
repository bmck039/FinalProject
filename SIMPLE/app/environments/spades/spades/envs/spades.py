import sys

sys.path.append(".....")

import util

from util import Spades

from util import Game

from util import Suit



from players import ActionPlayer

import players



# import gymnasium as gym

# from gymnasium import spaces

import gym

from gym import spaces

import numpy as np



# Returns an index [0, 51] that corresponds to the card's index in a binary vector.

def getIndexFromCard(card           )       : 

    value, suit = card.asTuple()

    return ((suit.value-1)*13)+value-1



# Returns a card that corresponds to the given index [0, 51].

def getCardFromIndex(index     )             : 

    value = (index % 13) + 1

    suitValue = (index // 13) + 1

    return util.Card(value, Suit(suitValue)) 



# Returns an encoded list of 52 ints, where each digit represents whether a card was passed as the argument (0 = no, 1 = yes)

def encodeCardBinary(card           )             : 

    result = [0] * 52 



    result[getIndexFromCard(card)] = 1

    return result



# Returns an encoded list of 52 ints, where each digit represents whether a card was present in the given list (0 = no, 1 = yes)

def encodeCardsBinary(cards                 )             : 

    result = [0] * 52 



    for card in cards:

        result[getIndexFromCard(card)] = 1

    return result



# Returns the first card decoded from the given binary list, or None if no cards are found.

def decodeCardBinary(binary           )                    :

    result = None



    for i in range(52):

        if binary[i] == 1:

            result = getCardFromIndex(i)

            break

    return result



# Returns a list of all cards decoded from the given binary list.

def decodeCardsBinary(binary           )                   :

    result = []



    for i in range(52):

        if binary[i] == 1:

            result.append(getCardFromIndex(i))

    return result



class SpadesGym(gym.Env):

    def __init__(self, verbose = False, manual = False)        :

        super(SpadesGym, self).__init__()



        self.name = 'spades'

        self.manual = manual

        self.verbose = verbose



        playersList = []

        playersList.append(players.AIPlayer(players.RandomPlay))

        playersList.append(players.AIPlayer(players.RandomPlay))

        playersList.append(players.AIPlayer(players.RandomPlay))

        playersList.append(players.AIPlayer(players.RandomPlay))



        self.game = Game(util.Spades, playersList)

        #the agent can play any of the 7 cards in its hand. the action returned will be a representation of the card to play

        self.action_space = spaces.Discrete(53)

        #observation space is a binary list of length 53 representing the legal actions for the current hand. a binary list of length 52 for the cards currently in the discard pile (same card representation as for the current hand), a list of 52 bits for cards seen, a 14 bit one-hot encoding of the number your team bid, one for the number of tricks you currently have, and one for the number of bags your team has

        # self.observation_space = spaces.Tuple([spaces.MultiBinary(52), spaces.MultiBinary(52), spaces.MultiBinary(52), spaces.MultiBinary(14), spaces.MultiBinary(14), spaces.MultiBinary(14)])

        self.observation_space = spaces.MultiBinary(199)

        self.n_players = 4

        self.current_player_num = 0

    

    @property

    def observation(self):

        handEncoding = self.legal_actions

        discardEncoding = encodeCardsBinary(self.game.state["discardPile"])

        seenEncoding = encodeCardsBinary(self.game.state["seenCards"])

        teamIndex = self.current_player_num % 2

        bagsEncoding = [0 for _ in range(14)]

        bags = self.game.state["bags"][teamIndex]

        bagsEncoding[bags] = 1



        tricksEncoding = [0 for _ in range(14)]

        tricks = self.game.state["tricks"][teamIndex]

        tricksEncoding[tricks] = 1



        bidEncoding = [0 for _ in range(14)]

        bid = self.game.state["bids"][self.current_player_num]

        bidEncoding[bid] = 1



        return np.concatenate((handEncoding, discardEncoding, seenEncoding, bidEncoding, tricksEncoding, bagsEncoding))

    

    @property

    def current_player(self):

        return self.game.players[self.current_player_num]



    @property

    def legal_actions(self):

        legalActions = []

        if Spades.isTurnOver(self.game.state):

            legalActions = [0] * 52 + [1] # have an ending action so that individual moves aren't assigned a score, just the play for that round

        else: 

            legalMoves = Spades.validMoves(self.current_player.hand, self.game.state)
            # print("current hand", self.current_player.hand)
            # print("legal moves", legalMoves)

            legalActions = encodeCardsBinary(legalMoves) + [0] #not allowed to have ending action while game is ongoing

        return np.array(legalActions)



    # def rules_move(self):
    #     actions = self.legalActions

    #     return actions * 1 / len(actions)



    def reset(self, seed=None, options=None):

        # super().reset()



        # new game is created

        players = self.game.players

        self.game.state = self.game.rules.setupGame(players)

        self.current_player_num = 0



        observation = self.observation

        info = {}

        return observation, info

    

    def setState(self, state, hand):

        self.game.state = state

        self.current_player_num = len(state["discardPile"])

        self.game.players[self.current_player_num].hand = hand



    def step(self, action     )                                             :

        playerIndex = self.current_player_num

        terminated = False

        info = {}

        reward = [0] * 4

        # print("player:", self.current_player_num, "with action:", action)

        if action == 52: # ending action

            for _ in range(4):
                reward[playerIndex] = Spades.scoreFromState(self.game.state, playerIndex)
                playerIndex = (playerIndex + 1) % 4
            terminated = True

        else: 

            card = getCardFromIndex(action)

            hand = self.game.players[playerIndex].hand



            if self.game.state["startRound"]:

                self.game.state["highestCard"] = util.Card(0, Suit.Hearts)



            if not Spades.isValidMove(hand, self.game.state, card):

                reward[playerIndex] = -1

            else:

                dummyPlayer = ActionPlayer(card)

                _, self.game.state = Spades.playerTurnTransition(dummyPlayer, self.game.state)

                # print(self.game.state)

                self.game.players[self.current_player_num].hand.remove(card)

                self.current_player_num = self.game.state["start"] if len(self.game.state["discardPile"]) == 0 else (self.current_player_num + 1) % 4

        

        return self.observation, reward, terminated, info



    def close(self):

        pass



    def render(self, mode="human"):

        pass

