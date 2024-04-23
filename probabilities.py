import json
import util
from math import comb
from enum import Enum

def evolve(pTable, iterations = 10000):
    # Assuming that hands[0] is the player, hands[1] is the partner, and hands[2] and hands[3] are opponents
    
    for iteration in range(1, iterations+1):
        hands = util.Spades.generateHands(4)
        for suit in util.Suit:
            # For each suit, sort all 4 players' cards by value
            suitHands = [sorted(util.subsetOfSuit(hands[i], suit), key=lambda x: util.Spades.offsetValue(x.asTuple()[0])) for i in range(4)]
            untrimmedLength = len(suitHands[0])

            # Skip iteration if suit is void
            if untrimmedLength == 0: continue

            # Only consider 3 lowest player cards
            trimmedHand = suitHands[0][:3]
            playerCount = len(trimmedHand)

            partnerCount = len(suitHands[1])
            opponentCount1 = len(suitHands[2])
            opponentCount2 = len(suitHands[3])

            numLarger = partnerCount
            numSmaller1 = 0
            numSmaller2 = 0

            valueIndex = util.Spades.binaryFromHandSubset(suitHands[0])

            isNilImpossible = False
            # Only consider more than 3 cards if these are spades
            if suit == util.Suit.Spades and len(suitHands[0]) >= 4:
                isNilImpossible = True
                
            for i in range(1, playerCount+1):
                # Break early if nil has already been found to be impossible.
                if isNilImpossible: break

                # Calculate the number of smaller cards both opponents have than the player's ith card
                while numSmaller1 < opponentCount1 and util.Spades.offsetValue(suitHands[2][numSmaller1].value) < util.Spades.offsetValue(trimmedHand[i-1].value):
                    numSmaller1 += 1
                while numSmaller2 < opponentCount2 and util.Spades.offsetValue(suitHands[3][numSmaller2].value) < util.Spades.offsetValue(trimmedHand[i-1].value):
                    numSmaller2 += 1

                # Calculate the number of larger cards the partner has than the player's ith card
                while numLarger > 0 and util.Spades.offsetValue(suitHands[1][-numLarger].value) < util.Spades.offsetValue(trimmedHand[-i].value):
                    numLarger -= 1

                # Use these values to calculate whether nil is viable for a given case.
                if suit == util.Suit.Spades:
                    isNilImpossible = isNilImpossible or (((opponentCount1 < i) or (numSmaller1 >= i)) and ((opponentCount2 < i) or (numSmaller2 >= i)) and ((numLarger < i)))
                else:
                    isNilImpossible = isNilImpossible or (((opponentCount1 < i) or (numSmaller1 >= i)) and ((opponentCount2 < i) or (numSmaller2 >= i)) and ((partnerCount >= i) and (numLarger < i)))
            isNilPossible = not isNilImpossible

            # Used for testing based on suit and values held.
            # if isNilPossible and valueIndex == 4099 and suit == util.Suit.Spades:
            #     print("A:", suitHands[0])
            #     print("A:", suitHands[1])
            #     print("B:", suitHands[2])
            #     print("B:", suitHands[3])
            #     print("-----")

            # Update the probability table
            pTable[str(suit)][str(valueIndex)]["successes"] += isNilPossible
            pTable[str(suit)][str(valueIndex)]["occurrences"] += 1
        if iteration % (iterations/100) == 0:
            print("Progress: " + str(float(iteration/iterations)*100) + "%")

def generate(iterations = 10000): 
    pTable = {str(suit): {str(i): {key: 0 for key in ["successes", "occurrences"]} for i in range(8192)} for suit in util.Suit}
    print(pTable)
    evolve(pTable, iterations)
    return pTable

def generateToFile(iterations = 10000, filepath = "probabilities.json", replace = False):
    pTable = generate(iterations)

    mode = "w" if replace else "x"
    file = open(filepath, mode)
    json.dump(pTable, file)
    file.close()

def evolveToFile(iterations = 10000, filepath = "probabilities.json"):
    pTable = readFromFile(filepath, False)
    evolve(pTable, iterations)

    file = open(filepath,"w")
    json.dump(pTable, file)
    file.close()

def readFromFile(filepath = "probabilities.json", asDecimal = True):
    file = open(filepath,"r")
    pTable = json.load(file)
    file.close()

    if asDecimal: normalize(pTable)
    return pTable

def normalize(pTable):
    for suitIndex, suitDict in pTable.items():
        for valueIndex, valueDict in suitDict.items():
            probability = valueDict["successes"] / valueDict["occurrences"] if valueDict["occurrences"] != 0 else 0
            pTable[suitIndex][valueIndex] = probability



# class cardCount(Enum):
#     Void = (0, 0)
#     Singleton = (1, 1)
#     Doubleton = (2, 2)
#     DoubletonPlus = (2, 13)
#     TripletonPlus = (3, 13)

# def binom(n, p, x):
#     return comb(n, x) * (p**x) * ((1-p)**(n-x))

# def cbinom(n, p, x1, x2):
#     sum = 0
#     for x in range(x1, x2+1):
#         sum += binom(n, p, x)
#     return sum

# def partnerState(targetState, cardsHeld, cumulative=False):
#     n = 13-cardsHeld
#     p = 1/3
#     xMin, xMax = targetState.value

#     return cbinom(n, p, (not cumulative)*xMin, xMax)

# def partnerHasLarger(targetCount, maxHeld):
#     n = 13-trueValue(maxHeld)
#     p = 1/3
#     x = targetCount

#     if x == 0: return 1.0
#     else: return 1 - cbinom(n, p, 0, targetCount-1)

# def opponentState(targetState, cardsHeld, cumulative=False):
#     n = 13-cardsHeld
#     p1 = 1/3
#     p2 = 1/2
#     xMin, xMax = targetState.value

#     sum = 0
#     for a in range((not cumulative)*xMin, xMax+1):
#         for b in range(0, min(a, n-a+1)):
#             sum += (binom(n, p1, a) * binom(n-a, p2, b))
#             sum += (binom(n, p1, b) * binom(n-b, p2, a))
#         if 2*a <= n: sum += (binom(n, p1, a) * binom(n-a, p2, a))

#     return sum

# def opponentHasSmaller(targetCount, minHeld):
#     n = trueValue(minHeld)-1
#     p = 2/3
#     x = targetCount

#     if x == 0: return 1.0
#     else: return 1 - cbinom(n, p, 0, targetCount-1)

# Uncomment to further evolve the probability table.
print("Mooching off of your computer a little to evolve the probability table. :)")
evolveToFile(100000, "probabilities.json")