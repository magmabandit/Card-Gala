from CrazyEightHand import Hand
from BJCard import Card
from BJDeck import Deck
from game import Game
from states import States
from CrazyEightPlayer import Player
class CrazyEight(Game):
    def __init__(self, players, room_name):
        super().__init__(2, players, "crazy8", room_name)
        self.deck = Deck()
        self.deck.shuffle()
        # Player and Dealer
        self.players_logic = [Player(), Player()]
        self.top_card = self.deck.deal_card()
        self.discard_pile = []


    def deal_initial_cards(self, server, state, pl1, pl2):
        player1 = self.players_logic[0]
        player2 = self.players_logic[1]
        for _ in range(7):
            player1.draw_card(self.deck.deal_card())
            player2.draw_card(self.deck.deal_card())
        server.cast(pl1, state["server commands"]["printing"] +
        "Your Hand: " +
        player1.show_hand() + "\n")
        server.cast(pl2, state["server commands"]["printing"] +
        "Your Hand: " +
        player2.show_hand() + "\n")
    def every_turn(self, server, state, pl1, pl2, player1, player2):
        current_turn = 0
        players = [pl1, pl2]
        logic = [player1, player2]

        while True:
            player_cast = players[current_turn]
            player_game = logic[current_turn]

            server.cast(player_cast, state["server commands"]["printing"] + "\nYour turn! Top card: " + str(self.top_card))
            server.cast(player_cast, state["server commands"]["printing"] + "Your Hand: " + player_game.show_hand())

            playable_cards = player_game.hand.get_playable_cards(self.top_card)

            if not playable_cards:
                if self.deck.is_empty():
                    self.deck.cards = self.discard_pile
                    self.deck.shuffle()
                    self.discard_pile = []
                player_game.draw_until_playable(self.deck, self.top_card)
                server.cast(player_cast, state["server commands"]["printing"] + "No valid cards, drawing until a playable one.\n")
            # Prompt player to choose a card
            playable_cards = player_game.hand.get_playable_cards(self.top_card)
            server.cast(player_cast, state["server commands"]["printing"] + "Playable cards:\n")
            for c in playable_cards:
                server.cast(player_cast, state["server commands"]["printing"] + str(c))

            not_played_card = True
            while not_played_card:
                suit = server.call(player_cast, state["server commands"]["suit"])
                rank = server.call(player_cast, state["server commands"]["rank"])
                card = Card(rank, suit)
                test_card = card.__str__()
                for cards in playable_cards:
                    if test_card == cards.__str__():
                        player_game.play_card(card, self.top_card)
                        self.discard_pile.append(self.top_card)
                        if card.rank == "8":
                            new_suit = server.call(player_cast, state["server commands"]["suit_change"])
                            self.top_card = Card("8", new_suit)
                        else:
                            self.top_card = card
                        not_played_card = False
                        break
                else:
                    server.cast(player_cast, state["server commands"]["printing"] + "Invalid card. Please try again.\n")

        
        # Check win
            if player_game.has_won():
                server.cast(player_cast, state["server commands"]["printing"] + " You win! \n")
                other = players[1 - current_turn]
                server.cast(other, state["server commands"]["printing"] + f"{player_game.get_name()} has won the game.\n")
                break

            current_turn = 1 - current_turn

    def play_round(self, server, state, pl1 , pl2):
        """Plays a round of Crazy Eight."""
        # Deal the initial cards
        self.deal_initial_cards(server, state, pl1, pl2)
        # Set the top card
        self.top_card = self.deck.deal_card()
        server.cast(pl1, state["server commands"]["printing"] +
                                "\nTop Card: " + str(self.top_card))
        server.cast(pl2, state["server commands"]["printing"] +
                                "\nTop Card: " + str(self.top_card))
        
        self.every_turn(server, state, pl1, pl2, self.players_logic[0], self.players_logic[1])

     
    def run(self, server, players):
        """Runs the game loop."""
        # make a state for blackjack 
        state = States.BLACKJACK
        # the client player
        pl1 = players[0]
        pl2 = players[1]
        
        # game state players
        player1 = self.players_logic[0]
        player2 = self.players_logic[1]

        server.cast(pl1, state["server commands"]["printing"] + "Welcome to Crazy Eight, " + pl1.get_username() + "!!")
        name = pl1.get_username()
        player1.set_name(name)
        server.cast(pl2, state["server commands"]["printing"] + "Welcome to Crazy Eight, " + pl2.get_username() + "!!")
        name = pl2.get_username()
        player2.set_name(name)

        self.play_round(server, state, pl1,pl2)

        server.cast(pl1, state["server commands"]["printing"] + "Thanks for playing Crazy Eight! Goodbye!!")
        server.cast(pl2, state["server commands"]["printing"] + "Thanks for playing Crazy Eight! Goodbye!!")
