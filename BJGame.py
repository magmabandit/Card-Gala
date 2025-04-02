from BJDeck import Deck
from BJPlayer import Player
from BJDealer import Dealer

from game import Game

class BJGame(Game):
    def __init__(self, players, room_name):
        super().__init__(3, players, "blackjack", room_name)
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
    def place_bet(self):
        """Handles betting before the round starts."""
       
        while True: 
            print(f"You have ${self.player.Get_money()} ")
            bet = int(input("Enter your bet: "))
            if bet > 0 and bet <= self.player.Get_money():
                self.player.Make_bet(bet)
                return bet
            else:
                print("Invalid bet! You must bet within your available money.")
    
    # deals the initial cards to the player and the dealer: Keeps dealers
    # second card hidden
    def deal_initial_cards(self):
        """Deals two cards to the player and the dealer."""
        self.player.Hit(self.deck.deal_card())
        self.player.Hit(self.deck.deal_card())
        self.dealer.Hit(self.deck.deal_card())
        self.dealer.Hit(self.deck.deal_card())

        print("\nYour Hand:", self.player.Show_hand())
        print("Hand Value:", self.player.Get_hand().get_value())
        print("Dealer's First Card:", self.dealer.Show_first_card())
        print("Dealer's Hand Value:", self.dealer.Value_first_card())
        print("It is your turn.")

    def player_turn(self):
        """Handles the player's hitting or standing."""

        while True:
            print("\nYour Hand:", self.player.Show_hand())
            print("Hand Value:", self.player.Get_hand().get_value())

            if self.player.Get_hand().get_value() > 21:
                print("You busted!")
                return False

            move = input("Do you want to (H)it or (S)tand? ").lower()
            if move == "h":
                self.player.Hit(self.deck.deal_card())
            elif move == "s":
                break
            else:
                print("Invalid choice. Enter H to hit or S to stand.")

        return True

    def dealer_turn(self):
        """Dealer plays according to the rules (hit until 17+)."""

        print("\nDealer's Turn...")
        print("Dealer's Hand:", self.dealer.Show_hand())

        self.dealer.Play_turn(self.deck)

        print("Dealer's Final Hand:", self.dealer.Show_hand())
        print("Dealer's Hand Value:", self.dealer.Get_hand().get_value())
    
    def determine_winner(self, bet):
        """Compares hands and determines who wins the round."""

        player_value = self.player.Get_hand().get_value()
        dealer_value = self.dealer.Get_hand().get_value()


        if dealer_value > 21 or player_value > dealer_value:
            print("You win!")
            self.player.add_money(bet * 1.5)

        elif player_value == dealer_value:
            print("It's a tie! You get your money back.")
            self.player.add_money(bet)  
        else:
            print("Dealer wins!")

    def play_round(self):
        """Runs a full round of Blackjack."""

        if self.player.Get_money() <= 0:
            print("You're out of money! Game over. 😢")
            return False
        
        self.deck.shuffle()
        bet = self.place_bet()
        self.deal_initial_cards()

        if self.player_turn():
            self.dealer_turn()
            self.determine_winner(bet)

        print(f"\nYour Money: ${self.player.Get_money()}")
        Game_check = input("\nPlay again? (Y/N): ").lower() == "y"
        if Game_check:
            self.player.clear_hand()
            self.dealer.clear_hand()
            self.new_deck()
            self.play_round()
        else:
            return False
    

    def run(self):
        """Runs the game loop."""

        print("Welcome to Blackjack!")
        name = input("Enter your name: ")
        self.player.Make_name(name)
        print(f"Welcome to Blackjack, {self.player.name}!")

        Value = input("Enter the amount of money you want to start with: ")
        if Value.isdigit() and int(Value) > 0:
            self.player.add_money(int(Value))
        else:
            print("You did not enter a valid amount of Money. Come "
            "back when you have actual money.")
            return 1

        self.play_round()
        print("Thanks for playing Blackjack!")


# Run the game
# if __name__ == "__main__":
#     game = BJGame()
#     game.play()
