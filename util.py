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
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, self.__class__): return False
        return self.value == __value.value and self.suit == __value.suit


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

    @abstractmethod
    def compareCards(c1: Card, c2: Card) -> int:
        pass

    @abstractmethod
    def isWon(state: dict) -> bool:
        pass

class basePlayer: #handles the basic operations of creating a player
    def __init__(self) -> None:
        self.hand = []
        self.rules = None

    def dealHand(self, hand: list[Card]):
        self.hand = hand

    def setRules(self, rules: Rules):
        self.rules = rules

    def returnCard(self, card: Card):
        self.hand.append(card)

    def update(score: int):
        pass

class Game(): #class representing a game. Written generally so all of the game-playing details are contained in a Rules object
    def __init__(self, rules: Rules, players: list[Player]):
        self.rules = rules
        self.players = []
        for p in players:
            self.players.append(p)
        self.state = self.rules.setupGame(players)
    
    def playTurn(self):
        self.state = self.rules.playTurn(self.players, self.state)
        self.state = self.rules.setupRound(self.players, self.state)

    def playUntilWin(self):
        while(not self.rules.isWon(self.state)):
            self.playTurn()


    
class Spades(Rules): #implementation of Rules for the game Spades

    def validMoves(hand: list[Card], state: dict) -> list:
        discardPile = state["discardPile"]
        if(len(discardPile) > 0):
            leadSuit = discardPile[0].suit #suit of first card in the discard pile
            leadSuitCards = subsetOfSuit(hand, leadSuit)
            if(len(leadSuitCards) > 0):
                #must follow suit if you can
                return leadSuitCards
            else:
                #you cannot follow suit so any move is valid
                return hand
        else: #your lead
            moves = []
            subsetSpades = subsetOfSuit(hand, Suit.Spades)
            if(state["spadesBroken"] or (len(hand) - len(subsetSpades)) == 0):
                moves += subsetSpades #if spades are broken or you cannot play a different card, then playing one at the start is allowed
            moves += subsetOfSuit(hand, Suit.Hearts)
            moves += subsetOfSuit(hand, Suit.Clubs)
            moves += subsetOfSuit(hand, Suit.Diamonds)
            return moves
    
    def isValidMove(hand: list[Card], gameState: dict, move: Card) -> bool:
        return move in Spades.validMoves(hand, gameState)

    def generateHands(n: int) -> list[Card]:
        deck = [Card(i, suit) for i in range(1, 13) for suit in list(Suit)]
        random.shuffle(deck)

        return np.array_split(deck, n)
    
    def compareCards(c1: Card, c2: Card) -> int: #1 if c1 > c2, -1 if c1 < c2, 0 if indeterminant
        if(c1.value == 0): return -1
        if(c2.value == 0): return 1
        if(c1.suit == c2.suit): return 1 if c1.value < c2.value else -1
        #if the suits aren't the same and one is a spade, the spade wins
        if(c1.suit == Suit.Spades): return 1
        if(c2.suit == Suit.Spades): return -1
        #indeterminant
        return 0
    
    def dealCards(players: list[Player], state: dict) -> dict:
        numPlayers = len(players)
        hands = Spades.generateHands(numPlayers)
        for i in range(numPlayers):
            players[i].dealHand(list(hands[i]))
            players[i].setRules(Spades)
            state["bids"].append(players[i].getBid(state))
        return state

    def setupRound(players: list[Player], state: dict) -> dict:
        numPlayers = len(players)
        state["discardPile"] = []
        state["spadesBroken"] = False
        state["bids"] = []
        state["tricks"] = [0 for n in range(numPlayers)]
        state = Spades.dealCards(players, state)
        return state

    def setupGame(players: list[Player]) -> dict: #initializes the state of the game when it's the start
        numPlayers = len(players)
        state = {}
        state["start"] = 0
        state["isWon"] = False
        state["scores"] = [0 for n in range(numPlayers)]
        state["bags"] = [0 for n in range(numPlayers)]
        state = Spades.setupRound(players, state)
        return state
    
    def updateScores(state: dict) -> dict:
        for i in range(len(state["tricks"])):
            numTricks = state["tricks"][i]
            numBid = state["bids"][i]
            scoreWeight = 10
            scoreSign = 1
            if numBid == 0: 
                scoreWeight = 100
                scoreSign = -1 if numTricks != 0 else 1
                state["scores"][i] += scoreWeight * scoreSign
            else:
                scoreSign = -1 if numTricks < numBid else 1
                state["scores"][i] += scoreWeight * numBid * scoreSign
            if(scoreSign > 0 or numBid == 0): #if you made your bid or bid nil
                state["bags"][i] += numTricks - numBid
            if(state["bags"][i] >= 5):
                while(state["bags"][i] >= 5):
                    state["scores"][i] -= 50
                    state["bags"][i] -= 5
        return state
    
    def playRound(players: list[Player], state: dict) -> dict:
        orderedPlayers = players[state["start"] : -1] + players[0 : state["start"]]
        highestCard = Card(0, Suit.Hearts)
        for p in orderedPlayers:
            card = p.play(state)
            while not (Spades.isValidMove(p.hand, state, card)):
                p.returnCard(card)
                card = p.play(state)
            state["discardPile"].append(card)
            if(card.suit == Suit.Spades and not state["spadesBroken"]): state["spadesBroken"] = True
            p.hand.remove(card)
            if(Spades.compareCards(card, highestCard) > 0):
                highestCard = card
        playerIndex = state["discardPile"].index(highestCard)
        state["tricks"][playerIndex] += 1
        state["discardPile"] = []
        return state
    
    def playTurn(players: list[Player], state: dict) -> dict: #returns the state after the current turn
        while(not Spades.isTurnOver(state)):
            state = Spades.playRound(players, state)
        state = Spades.updateScores(state)
        if(Spades.isWon(state)): 
            for i in range(len(players)):
                players[i].update(state["score"])
        print(state)
        return state
    
    def isTurnOver(state: dict) -> bool:
        numTurns = 0
        for tricks in state["tricks"]:
            numTurns += tricks
        return numTurns == 12
    
    def isWon(state: dict) -> bool:
        for score in state["scores"]:
            if score >= 500: return True
        return False
    
