import random
import hand
import game

def TallyScores(players):
    # Scoring
    scores = [0, 0, 0] # player 1, 2, 3
    misc1 = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    misc2 = ['J', 'Q', 'K']

    for i in range(3):
        for card in players[i].nonBahay:
            rank = card[0]
            for j in range(len(misc1)):
                if rank == misc1[j]:
                    scores[i] += j + 1
            if rank in misc2:
                scores[i] += 10

    if min(scores[0], scores[1], scores[2]) == scores[0]:
        return 1
        # print("player 1 wins")
    elif min(scores[0], scores[1], scores[2]) == scores[1]:
        return 2
        # print("player 2 wins")
    else:
        return 3
        # print("player 3 wins")

def ExtendShownBahay(player, shownBahay):
    for i in range(len(player.nonBahay)):
        for bahay in shownBahay:
            if hand.isBahay3(player.nonBahay[i], bahay[0], bahay[1]):
                bahay.append(player.nonBahay.pop(i))
                bahay.sort(key=hand.rankOrdinal)
                return True
            if hand.isBahay3(player.nonBahay[i], bahay[-1], bahay[-2]):
                bahay.append(player.nonBahay.pop(i))
                bahay.sort(key=hand.rankOrdinal)
                return True
            
    return False

def DiscardOrKeep(player: hand.Hand, discardPile: game.Stack):
    player.SortHand()

    if len(player.nonBahay) <= 0: return # Okay, im not sure if adding this guard clause will cause problems

    if random.random() < player.riskLevel:
        discardPile.AddCard(player.nonBahay.pop())
    else:
        inAlmostBahays = []
        for i in range(len(player.almostBahay)):
            for j in range(len(player.almostBahay[i])):
                inAlmostBahays.append(player.almostBahay[i][j])

        for i in range(len(player.nonBahay) - 1):
            if player.nonBahay[-1 - i] in inAlmostBahays:
                continue

            discardPile.AddCard(player.nonBahay.pop(-1-i))
            break
        
        discardPile.AddCard(player.nonBahay.pop()) # ! BUG APPEARS HERE (IndexError, Pop from Empty List)         

    # print("discard", discardPile.PeekTopCard()) #############################
    player.SortHand()

def DrawFromDiscardPile(player, game, i):
    if len(player.nonBahay) <= 1: return # Okay, im not sure if adding this guard clause will cause problems

    bahay = [game.discardPile.Draw()]

    k = -1
    l = -1
    for j in range(len(player.nonBahay)):
        if player.almostBahay[i][0] == player.nonBahay[j]:
            k = j
        if player.almostBahay[i][1] == player.nonBahay[j]:
            l = j

    # print(player.nonBahay)
    bahay.append(player.nonBahay.pop(max(k, l)))
    bahay.append(player.nonBahay.pop(min(k, l))) # ! BUG HERE (IndexError, Pop from Empty List)
                                                 # This happens when there is only 1 element left in nonBahay

    game.shownBahay.append(bahay)
    return 

def DoTurnOne(player, game):
    # player.PrintHand() ###############################################
    # print("draw", game.deck.PeekTopCard()) #######################################

    game.deck.Draw()
    DiscardOrKeep(player, game.discardPile)
    # player.PrintHand() #############################################

def DoRegularTurn(player, game):
    ### Standard Gameplay ####
    discarded = game.discardPile.PeekTopCard() # last discarded card
    # player.PrintHand() #############################################

    # See if discarded card can be used
    for i in range(len(player.almostBahay)):
        if hand.isBahay3(player.almostBahay[i][0], player.almostBahay[i][1], discarded): # discarded card can be used
            # print("discarded draw", discarded) #######################
            DrawFromDiscardPile(player, game, i)
            # print("shown bahay", game.shownBahay) #########################
            DiscardOrKeep(player, game.discardPile)
            # player.PrintHand() ########################################
            return
        
    # Discarded card cannot be used; draw from deck
    # print("draw", game.deck.PeekTopCard())
    game.deck.Draw()
    player.SortHand()
    while ExtendShownBahay(player, game.shownBahay):
        continue
    # print("shown bahay", game.shownBahay) #################################
    DiscardOrKeep(player, game.discardPile)
    # player.PrintHand() ################################################


def RunTongitsSim(riskLevel1, riskLevel2, riskLevel3, seed):
    random.seed = seed

    ### Initialization of Game & Decks ###
    tongits = game.Game(seed)
    tongits.deck.Shuffle()

    ### Initialization of Player Hands and turn orders ###
    player1 = hand.Hand(riskLevel1) 
    player2 = hand.Hand(riskLevel2)
    player3 = hand.Hand(riskLevel3)

    players = [player1, player2, player3]
    turnOrder = [1,2,3]
    random.shuffle(turnOrder)

    for i in range(12):
        for j in range(3):
            players[turnOrder[j] - 1].nonBahay.append(tongits.deck.Draw())
    players[0].nonBahay.append(tongits.deck.Draw())

    ### Main Game Loop ###
    while tongits.deck.get_cardCount() != 0:
        # print('remaining cards in deck:', tongits.deck.get_cardCount()) ##################################
        
        ## Change Turn ##
        tongits.turn += 1
        player = players[turnOrder[(tongits.turn - 1) % 3] - 1]
        # player = players[(tongits.turn - 1) % 3]

        # print("=== Player {} ===".format((tongits.turn - 1) % 3 + 1)) #########################
        # print("turn", tongits.turn) ###########################################################
        
        # Sort each player's hand for the first time on first turn
        if tongits.turn < 4:
            player.SortHand()
        
        if tongits.turn == 1:
            ### On turn one the player can only draw from the deck ###
            DoTurnOne(player, tongits)
        else:
            DoRegularTurn(player, tongits)

        if player.nonBahay == []:
            break
    return TallyScores(players)

if __name__ == "__main__":
    RunTongitsSim(1.01, 1.01, 1.01, 10000)