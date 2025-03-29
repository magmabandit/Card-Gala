from BJPlayer import Player
from BJCard import Card

class Dealer(Player):
    def __init__(self):
  
        super().__init__()  
        self.name = "Dealer"  
        self.money = None  

    def Show_first_card(self):
        if self.hand.cards:
            return str(self.hand.cards[0]) + ", [Hidden Card]"
        return "[No Cards]"

    def Play_turn(self, deck):
      
        while self.hand.get_value() < 17:
            self.Hit(deck.deal_card())  
