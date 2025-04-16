from typing import List
from BJDeck import Deck
from BJCard import Card
class Hand:
    def __init__(self):
        self.cards = []  

    def add_card(self, card: Card):
        self.cards.append(card)

    
    def __str__(self):
        if self.cards:
            return " ".join(str(card) for card in self.cards)
        else:
            return "No cards in hand"
        
    def remove_card(self, card: Card):
        if card in self.cards:
            self.cards.remove(card)
        else:
            raise ValueError(f"Card {card} not found in hand.")

    def get_playable_cards(self, top_card: Card):
        playable_cards = [
            card for card in self.cards
            if card.get_suit() == top_card.get_suit() 
            or card.get_rank() == top_card.get_rank() 
            or card.get_rank() == "8"
        ]
        return playable_cards

    
    def draw_from_deck(self, deck: Deck, num: int = 1):
        if deck.is_empty():
            return
        for _ in range(num):
            self.add_card(deck.deal_card())
            

