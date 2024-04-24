from util import Spades
from util import Game
from util import Suit
import gymnasium as gym
from gymnasium import spaces

import math

def getCardFromIndex(action: int):
    suit = Suit(math.floor(action / 13))
    print(suit)


class SpadesGym(gym.Env):
    def __init__(self, game) -> None:
        super(SpadesGym, self).__init__()

        self.game = game
        self.hand = hand
        #the agent can play any of the 7 cards in its hand. the action returned will be a representation of the card to play
        self.action_space = spaces.Discrete(52)
        #observation space is a binary list of length 52 representing the cards in current hand. a binary list of length 52 for the cards currently in the discard pile (same card representation as for the current hand), a list of 52 bits for cards seen, an int for the number your team bid, an int for the number of tricks you currently have, and an int for the number of bags your team has
        self.observation_space = spaces.Tuple(spaces.MultiBinary(52), spaces.MultiBinary(52), spaces.MultiBinary(52), spaces.Discrete(3), spaces.MultiBinary(1))
        self.n_players = 4
        self.current_player_num = 0
    
    def stateToObs(self, state):
        obs = None
        return obs
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)

        # new game is created
        players = self.game.players
        state = self.game.rules.setupGame(players)
        self.current_player_num = 0

        observation = self.stateToObs(state)
        info = {}
        return observation, info


    def close(self):
        pass

    def render(self):
        pass

    def step(self, action: int) -> tuple[dict, float, bool, bool, dict[str]]:
        card = getCardFromIndex(action)
        truncated = False
        info = {}

        if not Spades.isValidMove(card):
            reward = -1
        
        return observation, reward, terminated, truncated, info