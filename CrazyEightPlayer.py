from CrazyEightHand import Hand
from BJCard import Card
class Player:
    def __init__(self):
        self.hand = Hand()
        self.name = ""
    
    # create a player with a hand, money,
    def set_name(self, name: str):
        self.name = name
    def get_name(self):
        return self.name
    def get_hand(self):
        return self.hand
    
    def draw_card(self, card: Card):
        self.hand.add_card(card)

    def show_hand(self):
        return str(self.hand)

    def clear_hand(self):
        self.hand = Hand()

    def remove_card(self, card: Card):
        self.hand.remove_card(card)

    def play_card(self, card: Card, top_card: Card):
        """Play a card from the hand if it's valid."""
        if card not in self.hand.cards:
            print(f"{self.name} does not have the card {card}.")
            return False

        playable_cards = self.hand.get_playable_cards(top_card)

        if card in playable_cards:
            self.hand.remove_card(card)
            return True
        else:
            print(f"{card} is not a valid play on top of {top_card}.")
            return False
        
    def has_won(self):
        return len(self.hand.cards) == 0
    
    def draw_until_playable(self, deck, top_card: Card):
        while not self.hand.get_playable_cards(top_card) and not deck.is_empty():
            self.hand.draw_from_deck(deck)
     



   
    