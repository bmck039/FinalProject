from util import Spades
from util import Game
import gymnasium as gym
from gymnasium import spaces

class SpadesGym(Game, gym.Env):
    def __init__(self) -> None:
        super(SpadesGym, self).__init__()
        #the agent can play any of the 7 cards in its hand. the action returned will be a representation of the card to play
        self.action_space = spaces.MultiBinary(52, start=0)
        #observation space is a binary list of length 52 representing the cards in current hand. a binary list of length 52 for the cards currently in the discard pile (same card representation as for the current hand), a list of 52 bits for cards seen, an int for the number your team bid, an int for the number of tricks you currently have, and an int for the number of bags your team has
        self.observation_space = spaces.Tuple(spaces.MultiBinary(52), spaces.MultiBinary(52), spaces.MultiBinary(52), spaces.Discrete(3), spaces.MultiBinary(1))

    def step(self, action: int) -> tuple[dict, float, bool, bool, dict[str]]:
        card = getCardFromIndex(action)
        if( not Spades.isValidMove()): return 