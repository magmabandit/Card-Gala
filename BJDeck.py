### ABDI do this
# BJDeck.py
# Deck class for blackjack and crazy eights
# includes methods to shuffle, deal cards, and check if empty
# contains a list of cards where each card is a suit and rank

from BJCard import Card
import random

class Deck:
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self):
        self.cards = []
        for suit in self.suits:
            for rank in self.ranks:
                self.cards.append(Card(rank, suit))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    
    def size(self):
        return len(self.cards)
    
    def is_empty(self):
        return len(self.cards) == 0