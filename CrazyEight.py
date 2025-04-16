from CrazyEightHand import Hand
from BJCard import Card
from BJDeck import Deck
from game import Game
from states import States
from CrazyEightPlayer import Player
class CrazyEight(Deck):
    def __init__(self, players, room_name):
        super().__init__(2, players, "crazy8", room_name)
        self.deck = Deck()
        self.deck.shuffle()
        # Player and Dealer
        self.players_logic = [Player(), Player()]
