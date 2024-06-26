from enum import Enum

import random

import numpy as np

from abc import ABC, abstractmethod



class Suit(Enum):

    Spades = 4

    Hearts = 3

    Clubs = 2

    Diamonds = 1



def subsetOfSuit(hand      , suit      ):

    return list(filter(lambda x: x.suit == suit, hand))



def listDiff(l1      , l2      )        :

    result = []

    for item in l1:

        if item not in l2: result.append(item)

    for item in l2:

        if item not in l1: result.append(item)

    return result



class Card: #representation of a card

    def __init__(self, value, suit      ):

        self.value = value

        self.suit = suit



    def __str__(self)       : #toString method

        return "(" + str(self.value) + ", " + str(self.suit) + ")"

    

    def __repr__(self)       : #allows for the toString method to be called when Card is embedded within a collection of objects (like a List)

        return self.__str__()

    

    def __eq__(self, __value        )        :

        if not isinstance(__value, self.__class__): return False

        return self.value == __value.value and self.suit == __value.suit

    

    def asTuple(self):

        return (self.value, self.suit)





class Player(ABC): #interface describing the basic requirements of a player

    @abstractmethod

    def play(state      )        :

        pass



    @abstractmethod

    def getBid(self)       :

        pass



class Rules(ABC): #interface for an object that controls the evolution of a game

    @abstractmethod

    def validMoves(hand            , state      )              :

        pass



    @abstractmethod

    def isValidMove(hand            , gameState      , move      )        :

        pass



    @abstractmethod

    def generateHands(n     )        :

        pass



    @abstractmethod

    def playTurn(players              , start)       :

        pass



    @abstractmethod

    def setupGame(n     )        :

        pass



    @abstractmethod

    def compareCards(c1      , c2      )       :

        pass



    @abstractmethod

    def isWon(state      )        :

        pass



class basePlayer: #handles the basic operations of creating a player

    def __init__(self)        :

        self.hand = []

        self.rules = None



    def dealHand(self, hand            ):

        self.hand = hand



    def setRules(self, rules       ):

        self.rules = rules



    def returnCard(self, card      ):

        self.hand.append(card)



    def update(self, score     ):

        pass



class Game(): #class representing a game. Written generally so all of the game-playing details are contained in a Rules object

    def __init__(self, rules       , players              , seed      = None):

        if(seed != None): random.seed(seed)

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



    def validMoves(hand            , state      )        :

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

            # print(subsetSpades)

            if(state["spadesBroken"] or (len(hand) - len(subsetSpades)) == 0):

                moves += subsetSpades #if spades are broken or you cannot play a different card, then playing one at the start is allowed

            moves += subsetOfSuit(hand, Suit.Hearts)

            # print(moves)

            moves += subsetOfSuit(hand, Suit.Clubs)

            # print(moves)

            moves += subsetOfSuit(hand, Suit.Diamonds)

            # print(moves)

            return moves

    

    def isValidMove(hand            , gameState      , move      )        :

        return move in Spades.validMoves(hand, gameState)



    def generateDeck():

        return [Card(i, suit) for i in range(1, 14) for suit in list(Suit)]



    def generateHands(n     )              :

        deck = Spades.generateDeck()

        random.shuffle(deck)



        return np.array_split(deck, n)

    

    def compareCards(c1      , c2      )       : #1 if c1 > c2, -1 if c1 < c2, 0 if indeterminate

        if(c1.value == 0): return -1 #allows for null cards to be represented

        if(c2.value == 0): return 1

        if(c1.suit == c2.suit): return 1 if c1.value > c2.value or c1.value == 1 else -1

        #if the suits aren't the same and one is a spade, the spade wins

        if(c1.suit == Suit.Spades): return 1

        if(c2.suit == Suit.Spades): return -1

        #indeterminate

        return 0



    def offsetValue(cardValue): #13 if cardValue = 1, cardValue-1 otherwise

        return ((cardValue-2) % 13) + 1



    def binaryFromHandSubset(hand):

        result = 0

        for card in hand:

            result += 2 ** (Spades.offsetValue(card.value) - 1)

        return result

    

    def dealCards(players              , state      )        :

        numPlayers = len(players)

        hands = Spades.generateHands(numPlayers)

        for i in range(numPlayers):

            players[i].dealHand(list(hands[i]))

            players[i].setRules(Spades)

            state["bids"].append(players[i].getBid(state))

        return state



    def setupRound(players              , state      )        :

        numPlayers = len(players)

        state["discardPile"] = []

        state["spadesBroken"] = False

        state["bids"] = []

        state["tricks"] = [0 for n in range(numPlayers)]

        state["seenCards"] = []

        state = Spades.dealCards(players, state)

        return state



    def setupGame(players              )        : #initializes the state of the game when it's the start

        numPlayers = len(players)

        state = {}

        state["start"] = 0

        state["isWon"] = False

        state["scores"] = [0 for n in range(numPlayers // 2)]

        state["bags"] = [0 for n in range(numPlayers // 2)]

        state["startRound"] = True

        state = Spades.setupRound(players, state)

        return state

    

    def scoreFromState(state      , i     )       :

        scoreChange = 0

        numTricks = state["tricks"][i]

        numBid = state["bids"][i]

        teamIndex = i % 2

        scoreWeight = 10

        scoreSign = 1

        if numBid == 0: 

            scoreWeight = 100

            scoreSign = -1 if numTricks != 0 else 1

            scoreChange += scoreWeight * scoreSign

        else:

            scoreSign = -1 if numTricks < numBid else 1

            scoreChange += scoreWeight * numBid * scoreSign

        if(scoreSign > 0 or numBid == 0): #if you made your bid or bid nil

            state["bags"][teamIndex] += numTricks - numBid

        if(state["bags"][teamIndex] >= 5):

            while(state["bags"][teamIndex] >= 5):

                scoreChange -= 50

                state["bags"][teamIndex] -= 5

        return scoreChange

    

    def updateScores(state      )        :

        for i in range(len(state["scores"])):

            score = Spades.scoreFromState(state, i)

            partnerScore = Spades.scoreFromState(state, i + 2)

            state["scores"][i] += score + partnerScore

        return state

    

    def playRound(players              , state      )        :

        numPlayers = len(players)

        orderedPlayers = players[state["start"] : numPlayers] + players[0 : state["start"]]

        state["highestCard"] = Card(0, Suit.Hearts)

        for p in orderedPlayers:

            card, state = Spades.playerTurnTransition(p, state)

        return state

    

    def playerTurnTransition(p, state):

        card = p.play(state)

        if state["startRound"]: state["startRound"] = False

        while not (Spades.isValidMove(p.hand, state, card)):

            print("invalid move ", card, " for hand ", p.hand)

            card = p.play(state)

        state = Spades.playerMove(state, p, card)

        highestCard = state["highestCard"]

        if(Spades.compareCards(card, highestCard) > 0):

            state["highestCard"] = card

        if(len(state["discardPile"]) == 4):

            playerIndex = state["discardPile"].index(state["highestCard"])

            state = Spades.roundEnd(state, playerIndex)

        return card, state



    def roundEnd(state, playerIndex):

        state["start"] = playerIndex

        state["tricks"][playerIndex] += 1

        state["discardPile"] = []

        state["highestCard"] = Card(0, Suit.Hearts)

        return state



    def playerMove(state, p, card):

        state["discardPile"].append(card)

        state["seenCards"].append(card)

        if(card.suit == Suit.Spades and not state["spadesBroken"]): state["spadesBroken"] = True

        p.hand.remove(card)

        return state

    

    def playTurn(players              , state      )        : #returns the state after the current turn

        while(not Spades.isTurnOver(state)):

            state = Spades.playRound(players, state)

        state = Spades.updateScores(state)

        if(Spades.isWon(state)): 

            for i in range(len(players)):

                players[i].update(state["scores"])

        return state

    

    def isTurnOver(state      )        :

        numTurns = 0

        for tricks in state["tricks"]:

            numTurns += tricks

        return numTurns == 13

    

    def isWon(state      )        :

        for score in state["scores"]:

            if score >= 500 or score <= -200: return True

        return False