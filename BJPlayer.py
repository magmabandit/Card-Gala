### ABDI do this

from BJHand import Hand
from BJCard import Card
class Player:
    def __init__(self):
        self.hand = Hand()
        self.money = 0
        self.name = ""
    
    # create a player with a hand, money, and name
    def Make_name(self, name: str):
        self.name = name
    def get_username(self):
        return self.name
    def Make_bet(self, bet: int):
        self.money -= bet

    def Get_hand(self):
        return self.hand
    
    def Hit(self, card: Card):
        self.hand.add_card(card)

    def Show_hand(self):
        return str(self.hand)
    
    def Get_money(self):
        return self.money
    
    def add_money(self, money: int):
        self.money += money
        
    def clear_hand(self):
        self.hand = Hand()
    