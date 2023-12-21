import random
import hand
import game

def main():
    # Initialization of Deck
    tongits = game.Game()

    tongits.deck.Shuffle()

    # Initialization of Player Hands
    player1 = hand.Hand()
    player2 = hand.Hand()
    player3 = hand.Hand()

    for i in range(12):
        player1.nonBahay.append(tongits.DrawFromDeck())
        player2.nonBahay.append(tongits.DrawFromDeck())
        player3.nonBahay.append(tongits.DrawFromDeck())
    player1.nonBahay.append(tongits.DrawFromDeck())

    players = [player1, player2, player3]

    ### Initialize risk ###
    risk = 1.01 # 0, 0.5, 1.01

    # Main Game Loop
    while tongits.deck.get_cardCount() != 0:
        print('remaining cards in deck:', tongits.deck.get_cardCount()) ##################################
        tongits.turn += 1
        
        player = players[(tongits.turn - 1) % 3]

        print("=== Player {} ===".format((tongits.turn - 1) % 3 + 1)) #########################
        print("turn", tongits.turn) ###########################################################
        
        game.AI(player, risk, tongits.deck, tongits.discardPile, tongits.shownBahay, isTurnOne = (tongits.turn == 1), isPlayersFirstTurn = (tongits.turn < 4))
        
        if player.nonBahay == []:
            break

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
        print("player 1 wins")

    elif min(scores[0], scores[1], scores[2]) == scores[1]:
        print("player 2 wins")

    else:
        print("player 3 wins")

if __name__ == "__main__":
    main()