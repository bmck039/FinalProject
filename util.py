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

class Card: #representation of a card
    def __init__(self, value, suit: Suit):
        self.value = value
        self.suit = suit

    def __str__(self) -> str: #toString method
        return "(" + str(self.value) + ", " + str(self.suit) + ")"
    
    def __repr__(self) -> str: #allows for the toString method to be called when Card is embedded within a collection of objects (like a List)
        return self.__str__()

class Player(ABC): #interface describing the basic requirements of a player
    @abstractmethod
    def play(state: dict) -> Card:
        pass

    @abstractmethod
    def getBid(self) -> int:
        pass

class Rules(ABC): #interface for an object that controls the evolution of a game
    @abstractmethod
    def validMoves(hand: list[Card], state: dict) -> list[Card]:
        pass

    @abstractmethod
    def isValidMove(hand: list[Card], gameState: dict, move: Card) -> bool:
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

    #TODO: isWon(state[]) -> bool

class basePlayer: #handles the basic operations of creating a player
    def __init__(self) -> None:
        self.hand = []
        self.rules = None

    def dealHand(self, hand: list[Card]):
        self.hand = hand

    def setRules(self, rules: Rules):
        self.rules = rules

class Game(): #class representing a game. Written generally so all of the game-playing details are contained in a Rules object
    def __init__(self, rules: Rules, players: list[Player]):
        self.rules = rules
        self.players = []
        for p in players:
            self.players.append(p)
        self.state = self.rules.setupGame(players)
    
    def playTurn(self):
        self.state = self.rules.playTurn(self.players, self.state)

    
class Spades(Rules): #implementation of Rules for the game Spades

    def validMoves(hand: list[Card], state: dict) -> list:
        discardPile = state["discardPile"]
        if(len(discardPile) > 0):
            leadSuit = discardPile[-1].suit #suit of last card in the discard pile
            leadSuitCards = subsetOfSuit(hand, leadSuit)
            if(len(leadSuitCards) > 0):
                #must follow suit if you can
                return leadSuitCards
            else:
                #you cannot follow suit so any move is valid
                return hand
        else: #your lead
            moves = []
            if(state["spadesBroken"]):
                moves += subsetOfSuit(hand, Suit.Spades) #if spades are broken, then playing one at the start is allowed
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
    
    def setupGame(players: list[Player]) -> dict: #initializes the state of the game when it's the start
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
            #TODO: if the move is not valid, make the player choose a different move

        print(state)
