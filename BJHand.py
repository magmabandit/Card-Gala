from BJDeck import Deck
from BJCard import Card
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0

    def add_card(self, card: Card):
        self.cards.append(card)
        self.calculate_value()

    def get_value(self):
        return self.value
    
    def __str__(self):
        Hand_card = ""
        if len(self.cards) > 0:
            for cards in self.cards:
                Hand_card += str(cards) + " "
            return Hand_card
        else:
            return "No cards in hand"
        
    def calculate_value(self):
        total = 0
        num_aces = 0  

        for card in self.cards:
            total += card.check_value() 
            if card.rank == "A":
                num_aces += 1  

        # If total is over 21 and we have Aces, adjust value of Ace to ``
        while total > 21 and num_aces > 0:
            total -= 10  # Convert one Ace from 11 to 1
            num_aces -= 1
        self.value = total 
     
