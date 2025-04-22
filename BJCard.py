### ABDI do this
# BJCard.py
# Card class for blackjack game
# includes methods to check value, get suit, and get rank
# contains a rank and suit

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    # Rank to integer value
    def check_value(self):
        if self.rank == "A":
            return 11
        elif self.rank == "J" or self.rank == "Q" or self.rank == "K":
            return 10 
        else:
            return int(self.rank)
        
    def get_suit(self):
        return self.suit
    
    def get_rank(self):
        return self.rank
        
    def __str__(self):
        return f"{self.rank}{self.suit}"
