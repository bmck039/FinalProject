from .util import Card
from .util import Suit
from .players import PlayingClass
from .players import ActionPlayer
from . import util

import copy
import numpy as np
from collections import defaultdict


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
        if len(self.state["discardPile"]) != self.playerIndex:
            possibleCards = util.listDiff(self.rules.generateDeck(), self.hand + self.state["seenCards"])
            self._untried_actions = self.rules.validMoves(possibleCards, self.state)
        else:
            self._untried_actions = self.rules.validMoves(self.hand, self.state)
        return self._untried_actions
    
    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):
        
        action = self._untried_actions.pop()
        player = ActionPlayer(action)
        _, next_state = self.rules.playerTurnTransition(player, self.state)
        child_node = MonteCarloTreeSearchNode(
            next_state, self.rules, self.hand, self.playerIndex, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node 
    
    def is_terminal_node(self):
        return len(self.state["seenCards"]) == 52
    
    def rollout(self):
        current_rollout_state = self.state
        
        while True:
            
            possible_moves = self.rules.validMoves(self.untried_actions(), current_rollout_state)

            if(len(current_rollout_state["seenCards"]) == 52): break
            
            action = self.rollout_policy(possible_moves)
            player = ActionPlayer(action)
            _, current_rollout_state = self.rules.playerTurnTransition(player, self.state)
        currentScore = self.rules.scoreFromState(current_rollout_state, self.playerIndex)
        partnerIndex = (self.playerIndex + 2) % 4
        partnerScore = self.rules.scoreFromState(current_rollout_state, partnerIndex)
        result = currentScore + partnerScore
        result = 1 if result > 0 else -1
        return result

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
        simulation_no = 5000
        
        
        for i in range(simulation_no):
            
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        
        return self.best_child(c_param=0.)







class MCTSPlay(PlayingClass):

    def play(rules, hand, state) -> Card: #returns a valid move
        stateCopy = copy.deepcopy(state)
        discardPile = stateCopy["discardPile"]
        playerIndex = len(discardPile)
        handCopy = copy.deepcopy(hand)

        root = MonteCarloTreeSearchNode(stateCopy, rules, handCopy, playerIndex)
        selected_node = root.best_action()
        action = selected_node.parent_action
        return action
