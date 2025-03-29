# press-the-button game
# whoever presses the button first wins

import threading
import time
import random
import keyboard
from tqdm import tqdm


class Player:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.name}"

# TODO: convert to game-specific subclass
# gamestate keeps track of winner, all players, and current gamestate.
class Game:
    def __init__(self, num_players, points):
        self.players = [Player(f"Player {i+1}") for i in range(num_players)]
        
        self.points = points # number of points needed to win
        self.round_winner = None

        self.game_over = False
        self.lock = threading.Lock() # Lock for thread-safe operations
        
        self.winners = {}

        # global winner of game
        self.total_winner = None

    def handle_player_turn(self, player):

        while True: 
            if not self.game_over:
                try:  # used try so that if user pressed other than the given key error will not be shown
                    if keyboard.is_pressed('b'):  # if key 'b' is pressed 
                        with self.lock:
                            print(f'{player.name} - Button pressed!')
                            if not self.game_over:
                                self.round_winner = player
                        return
                except:
                    time.sleep(.05)  
                    continue
            else: return

    # resets round-based game vars for continued use
    # game_over, round_winner
    def reset_game(self):
        self.game_over = False
        self.round_winner = None

    # prints the current score of the game in progress
    def print_curr_score(self):
        print("--------------------------")
        print(f"{self.points} points needed to win!")
        for player in self.players:

            if player in self.winners:
                print(f"{player.name} - {self.winners[player]}")
        print("--------------------------")

    def play(self):
        # TODO broadcast sequential messages to every client in game!
        print(f"Welcome to Press the Button! Whoever gets {self.points}" 
              " points first wins! Press 'b' to press the button first!")
        time.sleep(2)

        round = 1
        # play until a winner is found
        while self.total_winner is None:
            print(f"======================= \n \
            ROUND {round}\n =======================")
            for i in tqdm(range(random.randint(1, 6))):
                time.sleep(0.5)  
            
            threads = []
            for player in self.players:
                thread = threading.Thread(target=self.handle_player_turn, args=(player,))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()
            print(f"End of Round - {self.round_winner.name} wins round {round}!")
            # count score of round winner and determine if game is over
            if self.round_winner not in self.winners:
                self.winners[self.round_winner] = 1
            else:
                self.winners[self.round_winner] += 1
            
            if self.winners[self.round_winner] >= self.points:
                self.total_winner = self.round_winner


            self.reset_game()
            round += 1
            time.sleep(1)
            self.print_curr_score()
            time.sleep(2)
        print(f"End of Game - {self.total_winner.name} wins!!!")
if __name__ == "__main__":
    game = Game(num_players=2, points=3)
    game.play()