# Client-compatible press-the-button
import threading
import time
import random

from game import Game
from states import States

class Player:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.name}"
    
#TODO: Register game on serverside & commands on clientside
class PressTheButton(Game):
    def __init__(self, players, room_name):
        points = 3 # can modify this based on the size of game you want
        super().__init__(2, players, "pressthebutton", room_name)

        self.players = [Player(f"Player {i+1}") for i in range(len(players))]
        
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
                
            if not self.game_over:
                try:  # used try so that if user pressed other than the given key error will not be shown
                    with self.lock:
                    if keyboard.is_pressed('b'):  # if key 'b' is pressed 
                            print(f'{player.name} - Button pressed!')
                            if not self.game_over:
                                self.round_winner = player
                        return
                except:
                    time.sleep(.05)  
                    continue
            else: return

    def play(self, server, players):
        state = States.PRESSTHEBUTTON
        
        for p in players:
            server.cast(p, state["server commands"]["printing"] +
            f"Welcome to Press the Button! Whoever gets {self.points}" 
                " points first wins! Press 'b' to press the button first!")
        time.sleep(2)

        # TODO: IMPLEMENT
        # each thread should send separate players prompt to press button under
        # a certain amount of time and should be able to recieve & store client
        # response time. Randomize key to press per player to make game 'fun'
        round = 1
        # play until a winner is found
        while self.total_winner is None:
            for p in players:
                server.cast(p, state["server commands"]["printing"] + f"======================= \n \
                ROUND {round}\n =======================")
            for p in players:
                server.cast(p, state["server commands"]["countdown"] + str(random.randint(1, 6)))  
            
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
    