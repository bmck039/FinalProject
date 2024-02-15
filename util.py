from enum import Enum
import random
import numpy as np
from abc import ABC, abstractmethod

class Suit(Enum):
    Spades = 4
    Hearts = 3
    Clubs = 2
    Diamonds = 1

def subsetOfSuit(hand: list, suit: Suit):
    return list(filter(lambda x: x.suit == suit, hand))

class Card:
    def __init__(self, value, suit: Suit):
        self.value = value
        self.suit = suit

    def __str__(self) -> str:
        return "(" + str(self.value) + ", " + str(self.suit) + ")"
    
    def __repr__(self) -> str:
        return self.__str__()

class Player(ABC):
    @abstractmethod
    def play(state: dict) -> Card:
        pass

    @abstractmethod
    def getBid(self) -> int:
        pass

class Rules(ABC):
    @abstractmethod
    def validMoves(hand: list[Card], discardPile: list[Card]) -> list[Card]:
        pass

    @abstractmethod
    def isValidMove(gameState: dict, move: Card) -> bool:
        pass

    @abstractmethod
    def generateHands(n: int) -> list:
        pass

    @abstractmethod
    def playTurn(players: list[Player], start) -> int:
        pass

    @abstractmethod
    def setupGame(n: int) -> dict:
        pass

class basePlayer:
    def __init__(self) -> None:
        self.hand = []
        self.rules = None

    def dealHand(self, hand: list[Card]):
        self.hand = hand

    def setRules(self, rules: Rules):
        self.rules = rules

class Game():
    def __init__(self, rules: Rules, players: list[Player]):
        self.rules = rules
        self.players = []
        for p in players:
            self.players.append(p)
        self.state = self.rules.setupGame(players)
    
    def playTurn(self):
        self.state = self.rules.playTurn(self.players, self.state)

    
class Spades(Rules):

    def validMoves(hand: list[Card], state: dict) -> list:
        discardPile = state["discardPile"]
        if(len(discardPile) > 0):
            leadSuit = discardPile[-1].suit
            leadSuitCards = subsetOfSuit(hand, leadSuit)
            if(len(leadSuitCards) > 0):
                #must follow suit
                return leadSuitCards
            else:
                #you cannot follow suit so any move is valid
                return hand
        else: #your lead
            moves = []
            if(state["spadesBroken"]):
                moves += subsetOfSuit(hand, Suit.Spades)
            moves += subsetOfSuit(hand, Suit.Hearts)
            moves += subsetOfSuit(hand, Suit.Clubs)
            moves += subsetOfSuit(hand, Suit.Diamonds)
            return moves
    
    def isValidMove(hand: list[Card], gameState: dict, move: Card) -> bool:
        return move in Spades.validMoves(hand, gameState)

    def generateHands(n: int) -> list[Card]:
        deck = [Card(i + 1, suit) for i in range(13) for suit in list(Suit)]
        random.shuffle(deck)

        return np.array_split(deck, n)
    
    def setupGame(players: list[Player]) -> dict:
        numPlayers = len(players)
        hands = Spades.generateHands(numPlayers)
        state = {}
        state["start"] = 0
        state["discardPile"] = []
        state["spadesBroken"] = False
        state["previousBids"] = []
        state["scores"] = [0 for n in range(numPlayers)]
        for i in range(numPlayers):
            players[i].dealHand(hands[i])
            players[i].setRules(Spades)
            state["previousBids"].append(players[i].getBid(state))
            print(state["previousBids"])
            print(players[i].hand)
        return state
    
    def playTurn(players: list[Player], state: dict) -> int:
        orderedPlayers = players[state["start"] : -1] + players[0 : state["start"]]
        for p in orderedPlayers:
            card = p.play(state)
            if(Spades.isValidMove(p.hand, state, card)):
                state["discardPile"] += [card]

        print(state)
