import random

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
    def __init__(self, seed):
        self.deck = Stack(isEmpty = False)
        self.discardPile = Stack(isEmpty = True)
        self.shownBahay = []
        self.turn = 0
        random.seed = seed