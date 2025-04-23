### ABDI and ETHAN do this
# BJTWOPlayer.py
# A simplified two-player Blackjack game where players play against a dealer.

import threading

from BJDeck import Deck
from BJPlayer import Player
from BJDealer import Dealer
from game import Game
from states import States

from colorama import Fore, Back, Style

class BJ2Player(Game):
    """ Initializes a 2-player Blackjack game. 
        Args:
            players: List of player objects.
            room_name: Name of the game room."""
    def __init__(self, players, room_name):
        super().__init__(2, players, "blackjack2player", room_name)
        # Game Deck
        self.deck = Deck()
        self.deck.shuffle()
        # Player and Dealer
        self.players_logic = [Player(), Player()]
        self.dealer = Dealer()
        self.bet1 = None
        self.bet2 = None

    def new_deck(self):
        """Creates a new deck if the current deck has less than 10 cards."""

        if self.deck.size() < 10:
            self.deck = Deck()
            self.deck.shuffle()

    def deal_initial_cards(self, server, state, pl1, pl2):
        """ Deals two cards each to player 1, player 2, and 
            the dealer (second dealer card is hidden).
            Args:
                server: The server instance to communicate with players.
                state: The game state.
                pl1: Player 1 object.
                pl2: Player 2 object."""
        player1 = self.players_logic[0]
        player2 = self.players_logic[1]
        player1.Hit(self.deck.deal_card())
        player1.Hit(self.deck.deal_card())
        player2.Hit(self.deck.deal_card())
        player2.Hit(self.deck.deal_card())
        self.dealer.Hit(self.deck.deal_card())
        self.dealer.Hit(self.deck.deal_card())

        server.cast(pl1, state["server commands"]["printing"] +
        "Your Hand: " +
        player1.Show_hand() + "\n" +
        "Your Hand Value: " +
        str(player1.Get_hand().get_value()) + "\n")

        server.cast(pl1, state["server commands"]["printing"] +
        f"{pl2.get_username()}'s Hand: " +
        player2.Show_hand() + "\n" +
        f"{pl2.get_username()}'s Hand Value: " +
        str(player2.Get_hand().get_value()) + "\n")

        server.cast(pl1, state["server commands"]["printing"] +
        "Dealers Hand: " +
        self.dealer.Show_first_card() + "\n" +
        "Dealers First Card: " +
        str(self.dealer.Value_first_card()) + "\n")

        server.cast(pl2, state["server commands"]["printing"] +
        "Your Hand: " +
        player2.Show_hand() + "\n" +
        "Your Hand Value: " +
        str(player2.Get_hand().get_value()) + "\n")

        server.cast(pl2, state["server commands"]["printing"] +
        f"{pl1.get_username()}'s Hand: " +
        player1.Show_hand() + "\n" +
        f"{pl1.get_username()}'s Hand Value: " +
        str(player1.Get_hand().get_value()) + "\n")

        server.cast(pl2, state["server commands"]["printing"] +
        "Dealers Hand: " +
        self.dealer.Show_first_card() + "\n" +
        "Dealers First Card: " +
        str(self.dealer.Value_first_card()) + "\n")       

    def player_turn(self, server, state, current_player, other_player,
                         pl1_turn):
        """Handles the player's hitting or standing, alternating turns.
            Args:
                server: The server instance to communicate with players.
                state: The game state.
                current_player: The player whose turn it is.
                other_player: The other player.
                pl1_turn: Boolean indicating if it's player 1's turn."""

        if pl1_turn:
            current_player_game = self.players_logic[0]
        else:
            current_player_game = self.players_logic[1]
        
        while True:
            server.cast(current_player, state["server commands"]["printing"] 
                        + "\nYour Hand: " + current_player_game.Show_hand())
            server.cast(current_player, state["server commands"]["printing"] 
                        + "\nHand Value: " 
                            + str(current_player_game.Get_hand().get_value()))

            if current_player_game.Get_hand().get_value() > 21:
                server.cast(current_player,
                             state["server commands"]["printing"] 
                                 + "You busted!")
                return False

            move = server.call(current_player, 
                               state["server commands"]["Player-choice"])
            if move == None:
                exit(0)
            if move == "h":  # Hit
                current_player_game.Hit(self.deck.deal_card())
                server.cast(current_player, 
                            state["server commands"]["printing"] 
                                + "\nYour new hand: " 
                                    + current_player_game.Show_hand())
            elif move == "s":  # Stand
                break
            else:
                server.cast(current_player, 
                            state["server commands"]["printing"] +
                                "Invalid choice" + 
                                    " Enter H to hit or S to stand.")

            # Show the other player's current hand for visibility
            server.cast(other_player, state["server commands"]["printing"] + 
                        "\n" + current_player.get_username() + "'s Hand: " 
                            + current_player_game.Show_hand())
            server.cast(other_player, state["server commands"]["printing"] + 
                        "\n" + current_player.get_username() 
                            + "'s Hand Value: " + 
                               str(current_player_game.Get_hand().get_value()))

        return True

    def dealer_turn(self, server, state, pl1, pl2):
        """Dealer plays according to the rules (hit until 17+).
            Args:
                server: The server instance to communicate with players.
                state: The game state.
                pl1: Player 1 object.
                pl2: Player 2 object."""

        server.cast(pl1, state["server commands"]["printing"] 
                        + "\nDealer's Turn...")
        server.cast(pl2, state["server commands"]["printing"] 
                        + "\nDealer's Turn...")
        server.cast(pl1, state["server commands"]["printing"] 
                        + self.dealer.Show_hand())
        server.cast(pl2, state["server commands"]["printing"] 
                        + self.dealer.Show_hand())

        self.dealer.Play_turn(self.deck)

        server.cast(pl1, state["server commands"]["printing"] 
                        + self.dealer.Show_hand())
        server.cast(pl2, state["server commands"]["printing"] 
                        + self.dealer.Show_hand())
        server.cast(pl1, state["server commands"]["printing"] 
                        + str(self.dealer.Get_hand().get_value()))
        server.cast(pl2, state["server commands"]["printing"] 
                        + str(self.dealer.Get_hand().get_value()))

    def determine_winner(self, bet, server, state, player, pl1_turn):
        """Compares hands and determines who wins the round.
            Args:
                bet: The bet amount for the current player.
                server: The server instance to communicate with players.
                state: The game state.
                player: The player object.
                pl1_turn: Boolean indicating if it's player 1's turn."""

        if pl1_turn:
            player_game = self.players_logic[0]
        else:
            player_game = self.players_logic[1]

        player_value = player_game.Get_hand().get_value()
        dealer_value = self.dealer.Get_hand().get_value()

        if dealer_value > 21 or player_value > dealer_value:
            server.cast(player, state["server commands"]["printing"] 
                            + "You win!")
            player_game.add_money(bet * 1.5)
        elif player_value == dealer_value:
            server.cast(player, state["server commands"]["printing"] 
                            + "It's a tie! You get your money back.")
            player_game.add_money(bet)  
        else:
            server.cast(player, state["server commands"]["printing"] 
                            + "Dealer wins!")

    def place_player_bet(self, server, pl, state, player):
        bet = server.call(pl, state["server commands"]["place bet"] 
                              + str(player.Get_money()))
        if bet == None:
            exit(0)
        if player == self.players_logic[0]:
            self.bet1 = int(bet)
        else:
            self.bet2 = int(bet)
        player.Make_bet(int(bet))

    def play_round(self, server, state, pl1, pl2):
        """Runs a full round of Blackjack.
            Args:
                server: The server instance to communicate with players.
                state: The game state.
                pl1: Player 1 object.
                pl2: Player 2 object."""
        player1 = self.players_logic[0]
        player2 = self.players_logic[1]

        if player1.Get_money() <= 0 and player2.Get_money() <= 0:
            server.cast(pl1, state["server commands"]["printing"] 
                            + "You're out of money! Game over :(.")
            server.cast(pl2, state["server commands"]["printing"] 
                            + "You're out of money! Game over :(.")
            return False
        elif player1.Get_money() <= 0:
            server.cast(pl1, state["server commands"]["printing"] 
                            + "You're out of money! Game over :(.")
            return False
        elif player2.Get_money() <= 0:
            server.cast(pl2, state["server commands"]["printing"] 
                            + "You're out of money! Game over :(.")
            return False

        self.deck.shuffle()
        player1_thread = threading.Thread(target=self.place_player_bet, 
                                          args=[server, pl1, state, player1])
        player2_thread = threading.Thread(target=self.place_player_bet, 
                                          args=[server, pl2, state, player2])
        player1_thread.start()
        player2_thread.start()
        player1_thread.join()
        player2_thread.join()
        # Deal to both players at the start
        self.deal_initial_cards(server, state, pl1, pl2) 
        # Player 1's and Player 2's turns (alternating hits)
        # Player 1's turn
        pl1_not_busted = self.player_turn(server, state, pl1, pl2, True)  
        # Player 2's turn
        pl2_not_busted = self.player_turn(server, state, pl2, pl1, False)  
        # After both players are done, dealer plays
        if pl1_not_busted or pl2_not_busted:
            self.dealer_turn(server, state, pl1, pl2)

        if pl1_not_busted:
            self.determine_winner(self.bet1, server, state, pl1, True)
        if pl2_not_busted:
            self.determine_winner(self.bet2, server, state, pl2, False)

        server.cast(pl1, state["server commands"]["printing"] 
                        + "AMOUNT OF MONEY LEFT: " 
                            + str(player1.Get_money()))
        server.cast(pl2, state["server commands"]["printing"] 
                        + "AMOUNT OF MONEY LEFT: " 
                            + str(player2.Get_money()))

        Game_check1 = server.call(pl1, 
                                  state["server commands"]["Player-choice2"])
        Game_check2 = server.call(pl2, 
                                  state["server commands"]["Player-choice2"])
        if Game_check1 == None or Game_check2 == None:
            exit(0)

        if Game_check1 == "y" and Game_check2 == "y":
            self.players_logic[0].clear_hand()
            self.players_logic[1].clear_hand()
            self.dealer.clear_hand()
            self.new_deck()
            self.play_round(server, state, pl1, pl2)
        else:
            return False
        
    def welcome_add_money(self, server, pl1, state, player1):
        """Welcomes the player and adds money to their account.
            Args:
                server: The server instance to communicate with players.
                pl1: Player 1 server.
                state: The game state.
                player1: Player 1 game object."""
        # reduces the string to fit 80 lines
        message = f"{Fore.GREEN}Waiting for players to join. {self.get_num_players()}/{self.get_max_players()} joined{Fore.RESET}"
        server.cast(pl1, state["server commands"]["printing"] +
                    message)
        server.cast(pl1, state["server commands"]["printing"] 
                    + "Welcome to blackjack, " + pl1.get_username() + "!!")
        name = pl1.get_username()
        player1.Make_name(name)

        # call(needs something to return)
        money = server.call(pl1, state["server commands"]["enter money"])
        if money == None:
            exit(0)
        player1.add_money(int(money))

    def run(self, server, players):
        """Starts the game loop for 2-player Blackjack.
        Args:
            server: The server instance to communicate with players.
            players: List of player objects.
        """
        # make a state for blackjack 2
        state = States.BLACKJACK
        # the client player
        pl1 = players[0]
        pl2 = players[1]
        
        # game state players
        player1 = self.players_logic[0]
        player2 = self.players_logic[1]

        player1_thread = threading.Thread(target=self.welcome_add_money, 
                                          args=[server, pl1, state, player1])
        player2_thread = threading.Thread(target=self.welcome_add_money,
                                          args=[server, pl2, state, player2])
        server.cast(pl2, state["server commands"]["printing"] 
                    + "This is your opponent, " + pl1.get_username() + "!!")
        server.cast(pl1, state["server commands"]["printing"] 
                    + "This is your opponent, " + pl2.get_username() + "!!")
        player1_thread.start()
        player2_thread.start()
        player1_thread.join()
        player2_thread.join()
        

        self.play_round(server, state, pl1,pl2)

        server.cast(pl1, state["server commands"]["printing"] 
                    + "Thanks for playing Blackjack! Goodbye!!")
        server.cast(pl2, state["server commands"]["printing"] 
                    + "Thanks for playing Blackjack! Goodbye!!")
