from BJDeck import Deck
from BJHand import Hand
from BJPlayer import Player
def main():
        deck = Deck()
        hand = Hand()
        hand.add_card(deck.deal_card())
        hand.add_card(deck.deal_card())
        print(hand)
        hand.calculate_value()
        print(hand.get_value())
        hand.add_card(deck.deal_card())
        print(hand)
        hand.calculate_value()
        print(hand.get_value())

        player = Player()
        player.Make_name("Alice")
        print(player.name)
        player.Make_bet(100)
        print(player.Get_money())
        player.Hit(deck.deal_card())
        print(player.Show_hand())
        player.Hit(deck.deal_card())
        print(player.Show_hand())
        print(player.Get_hand().get_value())
        

   

if __name__ == '__main__':
        main()