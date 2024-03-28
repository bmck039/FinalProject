from util import Card
from util import Suit
from players import PlayingClass
import util

import numpy as np
from collections import defaultdict

class MonteCarloPlayer(util.basePlayer):
    def __init__(self, action) -> None:
        super().__init__()
        self.action = action

    def play(self, rules, hand, state):
        return self.action

class MonteCarloTreeSearchNode(): #https://ai-boson.github.io/mcts/
    def __init__(self, state, rules, hand, playerIndex, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self.rules = rules
        self.hand = hand
        self.playerIndex = playerIndex
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return
    
    def untried_actions(self):
        self._untried_actions = self.rules.validMoves(np.setdiff1d(self.rules.generateDeck(), self.hand + self.state["seenCards"]), self.state)
        return self._untried_actions
    
    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):
        
        action = self._untried_actions.pop()
        next_state = self.rules.playerMove(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node 
    
    def is_terminal_node(self):
        return len(self.state["seenCards"]) == 52
    
    def rollout(self):
        current_rollout_state = self.state
        
        while not self.rules.isWon(current_rollout_state):
            
            possible_moves = current_rollout_state.get_legal_actions()
            
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):
    
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]
    
    def rollout_policy(self, possible_moves):
        
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():
            
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 100
        
        
        for i in range(simulation_no):
            
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        
        return self.best_child(c_param=0.)







class MCTS(PlayingClass):

    def play(rules, hand, state) -> Card: #returns a valid move
        discardPile = state["discardPile"]
        playerIndex = len(discardPile)

        root = MonteCarloTreeSearchNode(state = state)
        selected_node = root.best_action()
