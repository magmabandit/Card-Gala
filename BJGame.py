### ETHAN do this

from BJDeck import Deck
from BJPlayer import Player
from BJDealer import Dealer

from game import Game
from states import States

from colorama import Fore, Back, Style
from ascii_art import art

class BJGame(Game):
    def __init__(self, players, room_name):
        # Sets max_players to 1 and game_type to blackjack
        super().__init__(1, players, "blackjack", room_name)
        # Game Deck
        self.deck = Deck()
        # Player and Dealer
        self.player = Player()
        self.dealer = Dealer()
     
    # Method to create a new deck if the current deck is running low
    def new_deck(self):
        if self.deck.size() < 10:
            self.deck = Deck()
            self.deck.shuffle()

    # asks the player to place a bet
    def place_bet(self, server, state, player):
        """Handles betting before the round starts."""
       
        bet = server.call(player, state["server commands"]["place bet"] +
                  str(self.player.Get_money()))
        if bet == None:
            exit(0)
        self.player.Make_bet(int(bet))
        return bet
            
    
    # deals the initial cards to the player and the dealer: Keeps dealers
    # second card hidden
    def deal_initial_cards(self, server, state, player):
        """Deals two cards to the player and the dealer."""
        self.player.Hit(self.deck.deal_card())
        self.player.Hit(self.deck.deal_card())
        self.dealer.Hit(self.deck.deal_card())
        self.dealer.Hit(self.deck.deal_card())

        server.cast(player, state["server commands"]["intial hand"] + 
                            self.player.Show_hand() + "," + 
                            str(self.player.Get_hand().get_value()) + "," +
                            self.dealer.Show_first_card() + "," + 
                            str(self.dealer.Value_first_card()))

    def player_turn(self, server, state, player):
        """Handles the player's hitting or standing."""

        while True:
            theHand = self.player.Show_hand().split()
            string_hand = ""
            for h in theHand[:-1]:
                string_hand += art[h] + ", "

            string_hand += art[theHand[-1]]
            
            # print("here", theHand)
            server.cast(player, state["server commands"]["printing"] + 
                                "\n-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-\n\nYOUR HAND: " + string_hand)
            # print(art[theHand[0]], art[theHand[1]])
            server.cast(player, state["server commands"]["printing"] + 
                                "YOUR HAND VALUE: " + 
                                str(self.player.Get_hand().get_value()))

        
            if self.player.Get_hand().get_value() > 21:
                server.cast(player, state["server commands"]["printing"] + 
                                    f"\n{Fore.RED}YOU BUSTED{Fore.WHITE}")
                return False
            move = server.call(player, 
                               state["server commands"]["Player-choice"])
            if move == None:
                exit(0)
            if move == "h":
                self.player.Hit(self.deck.deal_card())
            elif move == "s":
                break
            else:
                server.cast(player, state["server commands"]["printing"] + 
                            "Invalid choice. Enter H to hit or S to stand.")

        return True

    def dealer_turn(self, server, state, player):
        """Dealer plays according to the rules (hit until 17+)."""
        server.cast(player, state["server commands"]["printing"] + 
                            "\nDealer's Turn...")
        server.cast(player, state["server commands"]["printing"] + 
                            self.dealer.Show_hand())

        self.dealer.Play_turn(self.deck)

        server.cast(player, state["server commands"]["printing"] + 
                            self.dealer.Show_hand())
        server.cast(player, state["server commands"]["printing"] + 
                            str(self.dealer.Get_hand().get_value()))
    
    def determine_winner(self, bet, server, state, player):
        """Compares hands and determines who wins the round."""

        player_value = self.player.Get_hand().get_value()
        dealer_value = self.dealer.Get_hand().get_value()


        if dealer_value > 21 or player_value > dealer_value:
            server.cast(player, state["server commands"]["printing"] + 
                                "You win!")
            self.player.add_money(bet * 1.5)

        elif player_value == dealer_value:
            server.cast(player, state["server commands"]["printing"] + 
                                "It's a tie! You get your money back.")
            self.player.add_money(bet)  
        else:
            server.cast(player, state["server commands"]["printing"] + 
                                "Dealer wins!")

    def play_round(self, server, state, player):
        """Runs a full round of Blackjack."""

        if self.player.Get_money() <= 0:
            server.cast(player, state["server commands"]["printing"] + 
                                "You're out of money! Game over :(.")
            return False
        
        self.deck.shuffle()
        bet = self.place_bet(server, state, player)
        self.deal_initial_cards(server, state, player) #TODO

        if self.player_turn(server, state, player):
            self.dealer_turn(server, state, player)
            self.determine_winner(bet, server, state, player)

        server.cast(player, state["server commands"]["printing"] + 
                            "Ammount of money left: " + 
                            str(self.player.Get_money()))
        Game_check = server.call(player, 
                                 state["server commands"]["Player-choice2"])
        if Game_check == None:
            exit(0)
        if Game_check == "y":
            self.player.clear_hand()
            self.dealer.clear_hand()
            self.new_deck()
            self.play_round(server, state, player)
        else:
            return False
    

    def run(self, server, players):
        """Runs the game loop."""
        state = States.BLACKJACK
        pl1 = players[0]

        # send welcome message(cast printing)
        welcome = f"""{Fore.BLUE}\n-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-
                                                                             
                 {Fore.BLUE}W E L C O M E   T O   B L A C K J A C K                     
                                                                             
{Fore.BLUE}-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-\n{Fore.WHITE}"""
        server.cast(pl1, state["server commands"]["printing"] + welcome)
        
        name = pl1.get_username()
        self.player.Make_name(name)

        # call(needs something to return)
        money = server.call(pl1, state["server commands"]["enter money"])
        if money == None:
            exit(0)
        self.player.add_money(int(money))

        self.play_round(server, state, pl1)
        server.cast(pl1, state["server commands"]["printing"] + 
                         "Thanks for playing Blackjack! Goodbye!!")
