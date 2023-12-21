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

# All Methods here related to sorting player hands
class Hand:
    def __init__(self):
        self.nonBahay = []
        self.almostBahay = []
        self.bahayInHand = []

    def get_fullHand(self):
        return [self.nonBahay, self.almostBahay, self.bahayInHand]
    
    def PrintHand(self):
        for i in range(len(self.bahayInHand)):
            for j in range(len(self.bahayInHand[i])):
                print('{}\t{}'.format(self.bahayInHand[i][j][0], self.bahayInHand[i][j][1]))

        for i in range(len(self.nonBahay)):
            print('{}\t{}'.format(self.nonBahay[i][0], self.nonBahay[i][1]))

        return
    
    # Sorts Hand by segregating and extending bahays in hand
    def SortHand(self):
        # Segregate Bahays of 3 in Hand
        while True:
            newBahay = self.__segBahay()
            if newBahay == []:
                break
            
            self.bahayInHand.append(newBahay)

        # Extend Bahays in Hand 
        while True:
            oldBahayInHand = self.bahayInHand.copy()
            self.__segBahay2()
            if self.bahayInHand == oldBahayInHand:
                break

        # List possible Almost Bahays
        self.__segAlmostBahay()

        self.nonBahay.sort(key=rankOrdinal)

        return
    
    # Segregates Bahay from nonbahay in hand
    def __segBahay(self):
        bahay = []

        if len(self.nonBahay) >= 3:
            for i in range(len(self.nonBahay)):
                for j in range(i + 1, len(self.nonBahay)):
                    for k in range(j + 1, len(self.nonBahay)):
                        if isBahay3(self.nonBahay[i], self.nonBahay[j], self.nonBahay[k]):
                            bahay = [self.nonBahay[i], self.nonBahay[j], self.nonBahay[k]]
                            bahay.sort(key=rankOrdinal)
                            self.nonBahay.pop(k)
                            self.nonBahay.pop(j)
                            self.nonBahay.pop(i)
                            return bahay
                        
        return bahay

    # Insert Description
    def __segBahay2(self):
        for bahay in self.bahayInHand:
            for i in range(len(self.nonBahay)):
                card = self.nonBahay[i]
                if bahay[0][0] == card[0] and bahay[1][0] == card[0]:
                    bahay.append(card)
                    self.nonBahay.pop(i)
                    
                if bahay[0][1] == card[1]:
                    if rankOrdinal(card) == rankOrdinal(bahay[0]) - 1 or rankOrdinal(card) == rankOrdinal(bahay[-1]) + 1:
                        bahay.append(card)
                        bahay.sort(key=rankOrdinal)
                        self.nonBahay.pop(i)
                        return

    # Segregates Almost Bahays           
    def __segAlmostBahay(self):
        for i in range(len(self.nonBahay)):
            for j in range(i + 1, len(self.nonBahay)):
                if isAlmostBahay(self.nonBahay[i], self.nonBahay[j]):
                    self.almostBahay.append([self.nonBahay[i], self.nonBahay[j]])