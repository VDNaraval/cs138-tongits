import random

def rankOrdinal(card):
    rankOrder = 0
    for rank in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
        rankOrder += 1
        if card[0] == rank:
            return rankOrder
        
def deckDraw(player, deck):
    player[0].append(deck.pop())
    return

def discard(player, risk, discardPile):
    if random.random() >= risk:
        discardPile.append(player[0].pop())
        return
    
    else:
        inAlmostBahays = []
        for i in range(len(player[1])):
            for j in range(len(player[1][i])):
                inAlmostBahays.append(player[1][i][j])

        for i in range(len(player[0]) - 1):
            if player[0][-1 - i] in inAlmostBahays:
                continue

            discardPile.append(player[0].pop(-1-i))
            return
        
        discardPile.append(player[0].pop()) # ! BUG APPEARS HERE (IndexError, Pop from Empty List)
        return

            

def discardDraw(player, i, discardPile, shownBahay):
    bahay = [discardPile.pop()]

    k = -1
    l = -1
    for j in range(len(player[0])):
        if player[1][i][0] == player[0][j]:
            k = j
        if player[1][i][1] == player[0][j]:
            l = j

    bahay.append(player[0].pop(max(k, l)))
    bahay.append(player[0].pop(min(k, l)))

    shownBahay.append(bahay)

    return
        
def extendShownBahay(player, shownBahay):
    for i in range(len(player[0])):
        for bahay in shownBahay:
            if isBahay3(player[0][i], bahay[0], bahay[1]):
                bahay.append(player[0].pop(i))
                bahay.sort(key=rankOrdinal)
                return True
            if isBahay3(player[0][i], bahay[-1], bahay[-2]):
                bahay.append(player[0].pop(i))
                bahay.sort(key=rankOrdinal)
                return True
            
    return False

def isBahay3(card1, card2, card3):
    if card1[0] == card2[0] and card2[0] == card3[0]:
        return True
        
    if card1[1] == card2[1] and card2[1] == card3[1]:
        rankOrders = [rankOrdinal(card1), rankOrdinal(card2), rankOrdinal(card3)]
        rankOrders.sort()
        if rankOrders[1] - rankOrders[0] == 1 and rankOrders[2] - rankOrders[1] == 1:
            return True
            
    return False

def isAlmostBahay(card1, card2):
    if card1[0] == card2[0]:
        return True
        
    if card1[1] == card2[1]:
        if abs(rankOrdinal(card1) - rankOrdinal(card2)) <= 2:
            return True
    
    return False

def segBahay(hand):
    bahay = []

    if len(hand) >= 3:
        for i in range(len(hand)):
            for j in range(i + 1, len(hand)):
                for k in range(j + 1, len(hand)):
                    if isBahay3(hand[i], hand[j], hand[k]):
                        bahay = [hand[i], hand[j], hand[k]]
                        bahay.sort(key=rankOrdinal)
                        hand.pop(k)
                        hand.pop(j)
                        hand.pop(i)
                        return bahay, hand
                    
    return bahay, hand

def segBahay2(bahayInHand, hand):
    for bahay in bahayInHand:
        for i in range(len(hand)):
            card = hand[i]
            if bahay[0][0] == card[0] and bahay[1][0] == card[0]:
                bahay.append(card)
                hand.pop(i)
                return bahayInHand, hand
                
            if bahay[0][1] == card[1]:
                if rankOrdinal(card) == rankOrdinal(bahay[0]) - 1 or rankOrdinal(card) == rankOrdinal(bahay[-1]) + 1:
                    bahay.append(card)
                    bahay.sort(key=rankOrdinal)
                    hand.pop(i)
                    return bahayInHand, hand
                
    return bahayInHand, hand

def segAlmostBahay(hand):
    almostBahayInHand = []
    for i in range(len(hand)):
        for j in range(i + 1, len(hand)):
            if isAlmostBahay(hand[i], hand[j]):
                almostBahayInHand.append([hand[i], hand[j]])

    return almostBahayInHand

def sortHand(player):
    bahayInHand = player[2]
    almostBahayInHand = player[1]
    nonBahayInHand = player[0]

    # Segregate Bahays of 3 in Hand
    while True:
        newBahay, nonBahayInHand = segBahay(nonBahayInHand)
        if newBahay == []:
            break
        
        bahayInHand.append(newBahay)

    # Extend Bahays in Hand 
    while True:
        oldBahayInHand = bahayInHand.copy()
        bahayInHand, nonBahayInHand = segBahay2(bahayInHand, nonBahayInHand)
        if bahayInHand == oldBahayInHand:
            break

    # List possible Almost Bahays
    almostBahayInHand = segAlmostBahay(nonBahayInHand)

    nonBahayInHand.sort(key=rankOrdinal)

    player[0] = nonBahayInHand
    player[1] = almostBahayInHand
    player[2] = bahayInHand
    

    return


def AI(player, risk, deck, discardPile, shownBahay, isTurnOne = False, isPlayersFirstTurn = False):
    

    # Sort Hand on Player's First Turn
    if isPlayersFirstTurn:
        sortHand(player)
        

    # Turn One of the Game (Player can only draw from deck)
    if isTurnOne:
        printHand(player) ###############################################
        print("draw", deck[-1]) #######################################
        deckDraw(player, deck)
        sortHand(player)
        discard(player, risk, discardPile)
        print("discard", discardPile[-1]) #############################
        sortHand(player)
        printHand(player) #############################################
        return
    
    ### Standard Gameplay ####

    discarded = discardPile[-1] # last discarded card
    # print("discarded", discarded)
    printHand(player) #############################################

    # See if discarded card can be used
    for i in range(len(player[1])):
        if isBahay3(player[1][i][0], player[1][i][1], discarded): # discarded card can be used
            print("discarded draw", discarded) #######################
            discardDraw(player, i, discardPile, shownBahay)
            print("shown bahay", shownBahay) #########################
            sortHand(player)
            discard(player, risk, discardPile)
            print("discard", discardPile[-1]) #############################
            sortHand(player)
            printHand(player) ########################################
            return
        
    # Discarded card cannot be used; draw from deck
    print("draw", deck[-1])
    deckDraw(player, deck)
    sortHand(player)
    while extendShownBahay(player, shownBahay):
        continue
    print("shown bahay", shownBahay) #################################
    sortHand(player)
    discard(player, risk, discardPile)
    print("discard", discardPile[-1]) #############################
    sortHand(player)
    printHand(player) ################################################
    return
            

def printHand(player):
    for i in range(len(player[2])):
        for j in range(len(player[2][i])):
            print('{}\t{}'.format(player[2][i][j][0], player[2][i][j][1]))

    for i in range(len(player[0])):
        print('{}\t{}'.format(player[0][i][0], player[0][i][1]))

    return

    
    
# yung may mga mahahabang "######", nagpriprint lang sa terminal for verification kung tama ba hahaha        



###########################################################################

deck = []

for rank in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
    for suit in ['Club', 'Diamond', 'Heart', 'Spade']:
        deck.append([rank,suit])
        
random.shuffle(deck)

player1 = [[], [], []]
player2 = [[], [], []]
player3 = [[], [], []]

for i in range(12):
    player1[0].append(deck.pop())
    player2[0].append(deck.pop())
    player3[0].append(deck.pop())
player1[0].append(deck.pop())


players = [player1, player2, player3]

discardPile = []
shownBahay = []
turn = 0

### Initialize risk ###
risk = 1.01 # 0, 0.5, 1.01

while len(deck) != 0:
    print('remaining cards in deck:', len(deck)) ##################################
    turn += 1
    
    player = players[(turn - 1) % 3]

    
    
    print("=== Player {} ===".format((turn - 1) % 3 + 1)) #########################
    print("turn", turn) ###########################################################
    

    AI(player, risk, deck, discardPile, shownBahay, isTurnOne = (turn == 1), isPlayersFirstTurn = (turn < 4))
    
    if player[0] == []:
        break

scores = [0, 0, 0] # player 1, 2, 3
misc1 = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10']
misc2 = ['J', 'Q', 'K']

for i in range(3):
    for card in players[i][0]:
        rank = card[0]
        for j in range(len(misc1)):
            if rank == misc1[j]:
                scores[i] += j + 1
        if rank in misc2:
            scores[i] += 10

if min(scores[0], scores[1], scores[2]) == scores[0]:
    print("player 1 wins")

elif min(scores[0], scores[1], scores[2]) == scores[1]:
    print("player 2 wins")

else:
    print("player 3 wins")
        