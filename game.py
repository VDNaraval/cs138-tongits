import random
import hand

# Stack Class
class Stack:
    def __init__(self, isEmpty):
        self.stack = []

        if not isEmpty:    
            for rank in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
                for suit in ['Club', 'Diamond', 'Heart', 'Spade']:
                    self.stack.append([rank,suit])
    
    def get_cardCount(self):
        return len(self.stack)

    def Shuffle(self):
        random.shuffle(self.stack)

    def Draw(self):
        if self.get_cardCount() > 0:
            return self.stack.pop()
        else:
            Exception("Deck is empty. Cannot Draw Card")
        
    def AddCard(self, card):
        self.stack.append(card)

    def PeekTopCard(self):
        if self.get_cardCount() > 0:
            return self.stack[-1]
    
# Game Class
class Game:
    def __init__(self):
        self.deck = Stack(isEmpty = False)
        self.discardPile = Stack(isEmpty = True)
        self.shownBahay = []
        self.turn = 0
    
    def DrawFromDeck(self):
        return self.deck.Draw()
    
    def DrawFromDiscard(self):
        return self.discardPile.Draw()
    
    def Discard(self, card):
        self.discardPile.AddCard(card)

def discard(player, risk, discardPile: Stack):
    if random.random() >= risk:
        discardPile.AddCard(player[0].pop())
        return
    
    else:
        inAlmostBahays = []
        for i in range(len(player[1])):
            for j in range(len(player[1][i])):
                inAlmostBahays.append(player[1][i][j])

        for i in range(len(player[0]) - 1):
            if player[0][-1 - i] in inAlmostBahays:
                continue

            discardPile.AddCard(player[0].pop(-1-i))
            return
        
        discardPile.AddCard(player[0].pop()) # ! BUG APPEARS HERE (IndexError, Pop from Empty List)
        return         


def discardDraw(player, i, discardPile: Stack, shownBahay):
    bahay = [discardPile.Draw()]

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
            if hand.isBahay3(player[0][i], bahay[0], bahay[1]):
                bahay.append(player[0].pop(i))
                bahay.sort(key=hand.rankOrdinal)
                return True
            if hand.isBahay3(player[0][i], bahay[-1], bahay[-2]):
                bahay.append(player[0].pop(i))
                bahay.sort(key=hand.rankOrdinal)
                return True
            
    return False

def AI(player: hand.Hand, risk, deck, discardPile, shownBahay, isTurnOne = False, isPlayersFirstTurn = False):
    # Sort Hand on Player's First Turn
    if isPlayersFirstTurn:
        player.SortHand()
        
    # Turn One of the Game (Player can only draw from deck)
    if isTurnOne:
        player.PrintHand() ###############################################
        print("draw", deck.PeekTopCard()) #######################################
        deck.Draw()
        player.SortHand()
        discard(player.get_fullHand(), risk, discardPile)
        print("discard", discardPile.PeekTopCard()) #############################
        player.SortHand()
        player.PrintHand() #############################################
        return
    
    ### Standard Gameplay ####

    discarded = discardPile.PeekTopCard() # last discarded card
    # print("discarded", discarded)
    player.PrintHand() #############################################

    # See if discarded card can be used
    for i in range(len(player.almostBahay)):
        if hand.isBahay3(player.almostBahay[i][0], player.almostBahay[i][1], discarded): # discarded card can be used
            print("discarded draw", discarded) #######################
            discardDraw(player.get_fullHand(), i, discardPile, shownBahay)
            print("shown bahay", shownBahay) #########################
            player.SortHand()
            discard(player.get_fullHand(), risk, discardPile)
            print("discard", discardPile.PeekTopCard()) #############################
            player.SortHand()
            player.PrintHand() ########################################
            return
        
    # Discarded card cannot be used; draw from deck
    print("draw", deck.PeekTopCard())
    deck.Draw()
    player.SortHand()
    while extendShownBahay(player.get_fullHand(), shownBahay):
        continue
    print("shown bahay", shownBahay) #################################
    player.SortHand()
    discard(player.get_fullHand(), risk, discardPile)
    print("discard", discardPile.PeekTopCard()) #############################
    player.SortHand()
    player.PrintHand() ################################################
    return