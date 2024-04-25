import util
from util import Spades
from util import Game
from util import Suit

from players import ActionPlayer

import gymnasium as gym
from gymnasium import spaces
import numpy as np

# Returns an index [0, 51] that corresponds to the card's index in a binary vector.
def getIndexFromCard(card: util.Card) -> int: 
    value, suit = card.asTuple()
    return ((suit.value-1)*13)+value-1

# Returns a card that corresponds to the given index [0, 51].
def getCardFromIndex(index: int) -> util.Card: 
    value = (index % 13) + 1
    suitValue = (index // 13) + 1
    return util.Card(value, Suit(suitValue)) 

# Returns an encoded list of 52 ints, where each digit represents whether a card was passed as the argument (0 = no, 1 = yes)
def encodeCardBinary(card: util.Card) -> list[int]: 
    result = [0] * 52 

    result[getIndexFromCard(card)] = 1
    return result

# Returns an encoded list of 52 ints, where each digit represents whether a card was present in the given list (0 = no, 1 = yes)
def encodeCardsBinary(cards: list[util.Card]) -> list[int]: 
    result = [0] * 52 

    for card in cards:
        result[getIndexFromCard(card)] = 1
    return result

# Returns the first card decoded from the given binary list, or None if no cards are found.
def decodeCardBinary(binary: list[int]) -> util.Card | None:
    result = None

    for i in range(52):
        if binary[i] == 1:
            result = getCardFromIndex(i)
            break
    return result

# Returns a list of all cards decoded from the given binary list.
def decodeCardsBinary(binary: list[int]) -> list[util.Card]:
    result = []

    for i in range(52):
        if binary[i] == 1:
            result.append(getCardFromIndex(i))
    return result

class SpadesGym(gym.Env):
    def __init__(self, game) -> None:
        super(SpadesGym, self).__init__()

        self.game = game
        #the agent can play any of the 7 cards in its hand. the action returned will be a representation of the card to play
        self.action_space = spaces.Discrete(53)
        #observation space is a binary list of length 52 representing the cards in current hand. a binary list of length 52 for the cards currently in the discard pile (same card representation as for the current hand), a list of 52 bits for cards seen, an int for the number your team bid, an int for the number of tricks you currently have, and an int for the number of bags your team has
        self.observation_space = spaces.Tuple(spaces.MultiBinary(52), spaces.MultiBinary(52), spaces.MultiBinary(52), spaces.Discrete(14), spaces.Discrete(14), spaces.Discrete(14))
        self.n_players = 4
        self.current_player_num = 0
    
    @property
    def observation(self):
        p = self.current_player
        handEncoding = encodeCardsBinary(p.hand)
        discardEncoding = encodeCardsBinary(self.game.state["discardPile"])
        seenEncoding = encodeCardsBinary(self.game.state["seenCards"])
        teamIndex = self.current_player_num % 2
        bagsScaled = self.game.state["bags"][teamIndex] / 13
        tricksScaled = self.game.state["tricks"][teamIndex] / 13
        bidScaled = self.game.state["bid"][self.current_player_num] / 13
        obs = [handEncoding, discardEncoding, seenEncoding, bidScaled, tricksScaled, bagsScaled]
        return np.array(obs)
    
    @property
    def current_player(self):
        return self.game.players[self.current_player_num]

    @property
    def legal_actions(self):
        legalActions = []
        if Spades.isTurnOver(self.game.state):
            legalActions = [0] * 52 + [1] # have an ending action so that individual moves aren't assigned a score, just the play for that round
        else: 
            legalMoves = Spades.validMoves(self.current_player)
            legalActions = encodeCardsBinary(legalMoves) + [0] #not allowed to have ending action while game is ongoing
        return np.array(legalActions)

        

    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)

        # new game is created
        players = self.game.players
        self.game.state = self.game.rules.setupGame(players)
        self.current_player_num = 0

        observation = self.observation
        info = {}
        return observation, info

    def step(self, action: int) -> tuple[dict, float, bool, bool, dict[str]]:
        playerIndex = self.current_player_num
        truncated = False
        terminated = False
        info = {}
        reward = [0] * 4
        if action == 52: # ending action
            reward[playerIndex] = Spades.scoreFromState(self.game.state, playerIndex)
            terminated = True
        else: 
            card = getCardFromIndex(action)

            if not Spades.isValidMove(card):
                reward[playerIndex] = -1
            else:
                dummyPlayer = ActionPlayer(card)
                _, self.game.state = Spades.playerTurnTransition(dummyPlayer, self.game.state)
                self.game.players[self.current_player_num].hand.remove(card)
                self.current_player_num = self.game.state["start"] if len(self.game.state["discardPile"]) > 0 else len(self.game.state["discardPile"])
        
        return self.observation, reward, terminated, truncated, info

    def close(self):
        pass

    def render(self):
        pass
