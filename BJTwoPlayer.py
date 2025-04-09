from BJDeck import Deck
from BJPlayer import Player
from BJDealer import Dealer
from game import Game
from states import States

class BJ2Player(Game):
    def __init__(self, players, room_name):
        super().__init__(2, players, "blackjack2player", room_name)
        # Game Deck
        self.deck = Deck()
        self.deck.shuffle()
        # Player and Dealer
        self.players_logic = [Player(), Player()]
        self.dealer = Dealer()

    # Method to create a new deck if the current deck is running low
    def new_deck(self):
        if self.deck.size() < 10:
            self.deck = Deck()
            self.deck.shuffle()

    # Asks the player to place a bet
    def place_bet(self, server, state, player):
        """Handles betting before the round starts."""
        bet = int(server.call(player, state["server commands"]["place bet"] + str(player.Get_money())))
        player.Make_bet(bet)
        return bet

    # Deals the initial cards to the player and the dealer: Keeps dealer's second card hidden
    def deal_initial_cards(self, server, state, pl1, pl2):
        """Deals two cards to the player and the dealer."""
        player1 = self.players_logic[0]
        player2 = self.players_logic[1]
        player1.Hit(self.deck.deal_card())
        player1.Hit(self.deck.deal_card())
        player2.Hit(self.deck.deal_card())
        player2.Hit(self.deck.deal_card())

        server.cast(pl1, state["server commands"]["intial hand"] +
        player1.Show_hand() + "," + str(player1.Get_hand().get_value()) + "," + 
        player2.Show_first_card() + "," + str(self.dealer.Value_first_card()))

        server.cast(pl2, state["server commands"]["intial hand"] +
        player1.Show_hand() + "," + str(player1.Get_hand().get_value()) + "," + 
        player2.Show_first_card() + "," + str(self.dealer.Value_first_card()))

    def player_turn(self, server, state, current_player, other_player):
        """Handles the player's hitting or standing, alternating turns."""
        
        while True:
            server.cast(current_player, state["server commands"]["printing"] + "\nYour Hand: " + current_player.Show_hand())
            server.cast(current_player, state["server commands"]["printing"] + "\nHand Value: " + str(current_player.Get_hand().get_value()))

            if current_player.Get_hand().get_value() > 21:
                server.cast(current_player, state["server commands"]["printing"] + "You busted!")
                return False

            move = server.call(current_player, state["server commands"]["Player-choice"])
            if move == "h":  # Hit
                current_player.Hit(self.deck.deal_card())
                server.cast(current_player, state["server commands"]["printing"] + "\nYour new hand: " + current_player.Show_hand())
            elif move == "s":  # Stand
                break
            else:
                server.cast(current_player, state["server commands"]["printing"] + 
                            "Invalid choice. Enter H to hit or S to stand.")

            # Show the other player's current hand for visibility
            server.cast(other_player, state["server commands"]["printing"] + 
                        "\n" + current_player.get_username() + "'s Hand: " + current_player.Show_hand())
            server.cast(other_player, state["server commands"]["printing"] + 
                        "\n" + current_player.get_username() + "'s Hand Value: " + str(current_player.Get_hand().get_value()))

        return True

    def dealer_turn(self, server, state, pl1, pl2):
        """Dealer plays according to the rules (hit until 17+)."""

        server.cast(pl1, state["server commands"]["printing"] + "\nDealer's Turn...")
        server.cast(pl2, state["server commands"]["printing"] + "\nDealer's Turn...")
        server.cast(pl1, state["server commands"]["printing"] + self.dealer.Show_hand())
        server.cast(pl2, state["server commands"]["printing"] + self.dealer.Show_hand())

        self.dealer.Play_turn(self.deck)

        server.cast(pl1, state["server commands"]["printing"] + self.dealer.Show_hand())
        server.cast(pl2, state["server commands"]["printing"] + self.dealer.Show_hand())
        server.cast(pl1, state["server commands"]["printing"] + str(self.dealer.Get_hand().get_value()))
        server.cast(pl2, state["server commands"]["printing"] + str(self.dealer.Get_hand().get_value()))

    def determine_winner(self, bet, server, state, player):
        """Compares hands and determines who wins the round."""

        player_value = player.Get_hand().get_value()
        dealer_value = self.dealer.Get_hand().get_value()

        if dealer_value > 21 or player_value > dealer_value:
            server.cast(player, state["server commands"]["printing"] + "You win!")
            player.add_money(bet * 1.5)
        elif player_value == dealer_value:
            server.cast(player, state["server commands"]["printing"] + "It's a tie! You get your money back.")
            player.add_money(bet)  
        else:
            server.cast(player, state["server commands"]["printing"] + "Dealer wins!")

    def play_round(self, server, state, pl1, pl2):
        """Runs a full round of Blackjack."""
        player1 = self.players_logic[0]
        player2 = self.players_logic[1]

        if player1.Get_money() <= 0 or player2.Get_money() <= 0:
            server.cast(pl1, state["server commands"]["printing"] + "You're out of money! Game over :(.")
            server.cast(pl2, state["server commands"]["printing"] + "You're out of money! Game over :(.")
            return False

        self.deck.shuffle()
        bet1 = self.place_bet(server, state, pl1)
        bet2 = self.place_bet(server, state, pl2)

        self.deal_initial_cards(server, state, pl1, pl2)  # Deal to both players at the start

        # Player 1's and Player 2's turns (alternating hits)
        self.player_turn(server, state, pl1, pl2)  # Player 1's turn
        self.player_turn(server, state, pl1, pl2)  # Player 2's turn

        # After both players are done, dealer plays
        self.dealer_turn(server, state, pl1, pl2)

        self.determine_winner(bet1, server, state, pl1)
        self.determine_winner(bet2, server, state, pl2)

        server.cast(pl1, state["server commands"]["printing"] + "Amount of money left: " + str(player1.Get_money()))
        server.cast(pl2, state["server commands"]["printing"] + "Amount of money left: " + str(player2.Get_money()))

        Game_check1 = server.call(pl1, state["server commands"]["Player-choice2"])
        Game_check2 = server.call(pl2, state["server commands"]["Player-choice2"])

        if Game_check1 == "y" and Game_check2 == "y":
            self.players_logic[0].clear_hand()
            self.players_logic[1].clear_hand()
            self.dealer.clear_hand()
            self.new_deck()
            self.play_round(server, state, pl1, pl2)
        else:
            return False

    def run(self, server, players):
        """Runs the game loop."""
        # make a state for blackjack 2
        state = States.BLACKJACK
        # the client player
        pl1 = players[0]
        pl2 = players[1]
        
        # game state players
        player1 = self.players_logic[0]
        player2 = self.players_logic[1]
        # send welcome message(cast printing)
        server.cast(pl1, state["server commands"]["printing"] + "Welcome to blackjack, " + pl1.get_username() + "!!")
        server.cast(pl2, state["server commands"]["printing"] + "Welcome to blackjack, " + pl2.get_username() + "!!")
        name = pl1.get_username()
        player1.Make_name(name)
        name = pl2.get_username()
        player2.Make_name(name)

        # call(needs something to return)
        money = server.call(pl1, state["server commands"]["enter money"])
        player1.add_money(int(money))

        money = server.call(pl2, state["server commands"]["enter money"])
        player2.add_money(int(money))

        self.play_round(server, state, pl1,pl2)

        server.cast(pl1, state["server commands"]["printing"] + "Thanks for playing Blackjack! Goodbye!!")
        server.cast(pl2, state["server commands"]["printing"] + "Thanks for playing Blackjack! Goodbye!!")
