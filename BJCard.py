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
        
    def __str__(self):
        return f"{self.rank}{self.suit}"
