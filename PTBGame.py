### ALEX do this
# PTBGame.py
# class + game logic for Press The Button

# Client-compatible press-the-button
import threading
import time
import random
import string

from game import Game
from states import States
from player import Player

class PTBPlayer:
    """
    Local player definition for printing + debug purposes
    """
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.name}"
    
# Register game on serverside & commands on clientside
class PressTheButton(Game):
    def __init__(self, players, room_name):
        points = 3 # can modify this based on the size of game you want
        super().__init__(2, players, "pressthebutton", room_name)

        self.ptb_players = [PTBPlayer(p.get_username()) for p in players]
        
        self.points = points # number of points needed to win
        self.round_winner = None

        self.game_over = False
        self.lock = threading.Lock() # Lock for thread-safe operations
        
        self.winners = {}

        # global winner of game
        self.total_winner = None
    
    def handle_player_turn(self, player, server, state, barrier):
        """
        Handles game logic for an individual player during a given round.
        Return: None
        """

        # choose a random key on the keyboard to press
        key_to_press = random.choice(string.ascii_lowercase + string.digits)
        server.cast(player, state["server commands"]["printing"] + f"!!! PRESS [{key_to_press}] !!!")
        # barrier.wait() # rendezous threads before listening for keypresses
        # raise KeyboardInterrupt
        while True: 
            if not self.game_over:
                # checks if client pressed the right key on the keyboard
                res = server.call(player, state["server commands"]["listen-keypress"] + key_to_press)
                if res == None:
                    exit(0)
                    # client presses correct key
                if res == "t":
                    if not self.game_over:
                        self.round_winner = player
                        self.game_over = True
                    return
                time.sleep(0.001)
            else: return


    def reset_game(self):
        """
        resets round-based game vars for continued use
        Note: veriables reset: game_over, round_winner
        """
        self.game_over = False
        self.round_winner = None

    def print_curr_score(self, players:list[Player], server, state):
        """
        Given list of current players, casts a round + scoreboard message to all
        players.
        """
        for p in players:
            server.cast(p, state["server commands"]["printing"] + "--------------------------")
            server.cast(p, state["server commands"]["printing"] + f"{self.points} points needed to win!")
            for p1 in players:
                if p1 in self.winners:
                    server.cast(p, state["server commands"]["printing"] + f"{p1.get_username()} - {self.winners[p1]}")
        for p in players:
            server.cast(p, state["server commands"]["printing"] + "--------------------------")       


    def run(self, server, players):
        """
        Given server object and list of active players,
        executes PTB Game logic.
        """
        state = States.PRESSTHEBUTTON
         
        for p in players:
            server.cast(p, state["server commands"]["printing"] +
            f"Welcome to Press the Button! Whoever gets {self.points}" 
                " points first wins! Press your given button first!")  
        pl1 = players[0]
        pl2 = players[1]        
        server.cast(pl2, state["server commands"]["printing"] 
                    + "This is your opponent, " + pl1.get_username() + "!!")
        server.cast(pl1, state["server commands"]["printing"] 
                    + "This is your opponent, " + pl2.get_username() + "!!")
        time.sleep(2)

        # each thread should send separate players prompt to press button under
        # a certain amount of time and should be able to recieve & store client
        # response time. Randomize key to press per player to make game 'fun'
        round = 1
        # play until a winner is found
        while self.total_winner is None:
            for p in players:
                server.cast(p, state["server commands"]["printing"] + f"======================= \n \
                ROUND {round}\n=======================")
            for p in players:
                server.cast(p, state["server commands"]["countdown"] + str(random.randint(1, 6)))  
            threads = []
            for player in players:
                thread = threading.Thread(target=self.handle_player_turn, args=(player,server,state,threading.Barrier(len(players))))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()
            for p in players:
                server.cast(p, state["server commands"]["printing"] + f"End of Round - {self.round_winner.get_username()} wins round {round}!")
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
            self.print_curr_score(players, server, state)
            time.sleep(2)
        
        for p in players:
            server.cast(p, state["server commands"]["printing"] + f"!!! Game over - Congratulations, {self.total_winner.get_username()} !!!")