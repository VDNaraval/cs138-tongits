import random

def rankOrdinal(card):
    rankOrder = 0
    for rank in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
        rankOrder += 1
        if card[0] == rank:
            return rankOrder

def isAlmostBahay(card1, card2):
    if card1[0] == card2[0]:
        return True
        
    if card1[1] == card2[1]:
        if abs(rankOrdinal(card1) - rankOrdinal(card2)) <= 2:
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
            
def isBahayExt(bahay, card):
    if bahay[0][0] == card[0]:
        return True
        
    if bahay[0][1] == card[1]:
        rankOrders = [rankOrdinal(i) for i in bahay]
        rankOrders.sort()
        if rankOrdinal(card) == rankOrders[0] - 1 or rankOrdinal(card) == rankOrders[-1] + 1:
            return True
            
    return False
    
def printHand(player):
    for i in range(len(player)):
        print('{}:\t{}\t{}'.format(i, player[i][0], player[i][1]))
        
    return

def printShownBahay(shownBahay):
    for i in range(len(shownBahay)):
        print('{}:'.format(i))
        for card in shownBahay[i]:
            print('\t{}\t{}'.format(card[0], card[1]))
            
    return

def discard(player, discardPile):
    while True:
        cardNumberInput = input('Choose which card to discard: ')
        if cardNumberInput.isdigit():
            cardNumber = int(cardNumberInput)
            if cardNumber < len(player):
                discardPile.append(player.pop(cardNumber))
                print('Discarded Card: {}\t{}'.format(discardPile[-1][0], discardPile[-1][1]))
                return
        print('Please enter a valid card number. ')
        
def deckDraw(player, deck):
    player.append(deck.pop())
    printHand(player)
    return

def discardDraw(player, discardPile, shownBahay):
    bahay = [discardPile.pop()]
    
    while True:
        cardNumberInput = input('Choose which card to form bahay (if none, enter x): ')
        if cardNumberInput == 'x':
            break
        if cardNumberInput.isdigit():
            cardNumber = int(cardNumberInput)
            if cardNumber < len(player):
                bahay.append(player.pop(cardNumber))
                printHand(player)
                continue
        print('Please enter a valid card number. ')
    
    shownBahay.append(bahay)
    
    return

def extendShownBahay(player, shownBahay):
    while True:
        cardNumberInput = input('Choose which card to form bahay (if none, enter x): ')
        if cardNumberInput == 'x':
            break
        if cardNumberInput.isdigit():
            cardNumber = int(cardNumberInput)
            if cardNumber < len(player):
                while True:
                    bahayNumberInput = input('Choose which bahay to extend (if none, enter x): ')
                    if bahayNumberInput == 'x':
                        break
                    if bahayNumberInput.isdigit():
                        bahayNumber = int(bahayNumberInput)
                        if bahayNumber < len(shownBahay):
                            shownBahay[bahayNumber].append(player.pop(cardNumber))
                            break
                    print('Please enter a valid card number. ')
                continue
        print('Please enter a valid card number. ')
        
    return

def action(player, deck, discardPile, shownBahay):
    while True:
        actionNumberInput = input('Choose which action to do.\n0:\tDraw from the deck\n1:\tDraw from the discard pile\n2:\tExtend a shown bahay\n3:\tSee all shown bahay\n4:\tDiscard\n')
        if actionNumberInput == '0':
            deckDraw(player, deck)
        if actionNumberInput == '1':
            discardDraw(player, discardPile, shownBahay)
        if actionNumberInput == '2':
            extendShownBahay(player, shownBahay)
        if actionNumberInput == '3':
            printShownBahay(shownBahay)
        if actionNumberInput == '4':
            discard(player, discardPile)
            return
        else:   
            print('Please enter a valid card number. ')
        

###########################################################################

deck = []

for rank in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
    for suit in ['Club', 'Diamond', 'Heart', 'Spade']:
        deck.append([rank,suit])
        
random.shuffle(deck)
# print(deck)

player1 = []
player2 = []
player3 = []

for i in range(12):
    player1.append(deck.pop())
    player2.append(deck.pop())
    player3.append(deck.pop())
player1.append(deck.pop())

# print(player1)
# print(player2)
# print(player3)
# print(deck)

players = [player1, player2, player3]

discardPile = []
shownBahay = []
turn = 0

# printHand(player1)
# discard(player1, discardPile)

# printHand(player1)
# print(discardPile)

while len(deck) != 0:
    print('remaining cards in deck:', len(deck))
    turn += 1
    
    player = players[(turn - 1) % 3]
    
    print("=== Player {} ===".format((turn - 1) % 3 + 1))
    
    printHand(player)
    
    if turn == 1:
        discard(player, discardPile)
        continue
    
    action(player, deck, discardPile, shownBahay)
    
        
        