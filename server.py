#
# server.py
#
# mechanics for the cardgala server

import socket
import select
import threading
import logging
import time
from multiprocessing import Process

from player import Player
from locked_dict import LockedDict
from locked_list import LockedList
from states import States
from game import Game
from BJGame import BJGame
from BJTwoPlayer import BJ2Player
from CrazyEight import CrazyEight

from PTBGame import PressTheButton

from colorama import Fore, Back, Style

PORT = 9998
MAX_GAME_INSTANCES = 4
GAMES = {
            "blackjack": BJGame, 
            "blackjack2player": BJ2Player, 
            "pressthebutton": PressTheButton,
            "crazy8":CrazyEight
        }
ERROR = "e"

class Server:

    def __init__(self):
        """ init all server variables """
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind(('', PORT))
        self.listen_socket.listen(100)

        

        self.login_cache = LockedDict()
        self.idle_players = LockedList()

        self.registered_games = LockedDict()
        # list of names of possible games
        for game in GAMES:
            self.registered_games.update(game, 0)
        self.waiting_game_rooms = LockedDict()

        self.player_threads = []
        logging.basicConfig(
            level=logging.DEBUG, 
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def run_server(self):
        """ runs the server """

        # This thread manages players that are waiting for a 
        # game room that they have joined to start
        waiting_games_thread = threading.Thread(
            target=self.send_waiting_players_update, 
            args = []
        )
        waiting_games_thread.start()

        try:
            while True:
                # When a new client attempts to connect, accept the connection
                # and init the new player
                self.logger.debug("Accepting new connection")

                # this command is blocking by default
                new_conn, addr = self.listen_socket.accept()

                new_player = Player(connection=new_conn)
                self.idle_players.append(new_player)
                self.logger.debug("New connection accepted")

                self.logger.debug("Starting new player")
                player_thread = threading.Thread(
                    target=self.host_player, 
                    args=[new_player]
                )
                self.logger.debug("new player thread created")
                self.player_threads.append(player_thread)
                player_thread.start()
                self.logger.debug("new player started")

                for t in self.player_threads:
                    if not t.is_alive():
                        t.join()
        finally:
            for thread in self.player_threads:
                thread.join()
            waiting_games_thread.join()
    
    def host_player(self, player):
        """ Handle player login and choosing of game """
        if self.handle_login(player) == ERROR:
            return
        if self.handle_choose_game(player) == ERROR:
            return 
    
    def handle_login(self, player):
        """ Handle player login """
        state = States.LOGIN

        logged_in = False
        while not logged_in:
            self.logger.debug("logging in!!")
            # Initiate the login sequence and get 
            # returning/exisiting user, username, password from client
            response = self.call(player, state["server commands"]["login"])
            if response is None: # The client connection closed
                self.logger.debug("Killing thread")
                return ERROR #kill the thread
            login_type = response[0:5]
            user_pass = response[5:].split(",")
            self.logger.debug(f"user_pass: {user_pass}")
            username = user_pass[0]
            self.logger.debug(f"username: {username}")
            password = user_pass[1]
            self.logger.debug(f"password: {password}")

            self.logger.debug(
                f"login type: {login_type}, username: {username}, password: {password}"
            )

            # Log player in
            responses = state["client responses"]["login"]
            if login_type in responses:
                if login_type == "newpl":
                    logged_in = self.new_player(player, username, password)
                else:
                    logged_in = self.existing_player(player, username, password)
            else:
                logged_in = self.login_error(login_type, player)
                return ERROR # If there is an error, kill the thread
        
        self.cast(player, state["server commands"]["set username"] 
                  + player.get_username())
    
    def handle_choose_game(self, player):
        """ Handle player choosing game """
        state = States.CHOOSE_GAME

        chosen_game = False
        while not chosen_game:
            self.logger.debug("Entering choose game state")
            response = self.call(
                player, state["server commands"]["choose game"] 
                    + self.waiting_game_rooms.format_waiting_games_for_send()
            )
            if response is None: # The client connection closed
                self.logger.debug("Killing thread")
                return ERROR #kill the thread 
            choose_game_type = response[0:5]
            game = response[5:]
            
            responses = state["client responses"]["choose game"]
            if choose_game_type in responses:
                if choose_game_type == "egame":
                    chosen_game = self.add_player_to_game(player, game)
                elif choose_game_type == "ngame":
                    chosen_game = self.create_new_game(player, game)
                elif choose_game_type == "updat":
                    chosen_game = False
                else:
                    chosen_game = self.client_quit(player)
            else:
                chosen_game = self.choose_game_error(choose_game_type, player)
                return ERROR 

    # Expects reponse - blocking until response is recieved
    # If a player has disconnected the player will be removed
    #   from idle_players and the connection is closed
    def call(self, player: Player, message: str):
        """ Call to server """
        self.logger.debug(f"Sending message {message}")
        connection = player.get_connection()
        connection.sendall(message.encode('utf-8'))
        self.logger.debug("Message sent")
     
        (ready_read, _, _) = select.select([connection], [], [])
        data = connection.recv(1024)
        if data != b'': # Recieved response from client
            response = data.decode('utf-8')
            self.logger.debug(f"Response: {response}")
            return response
        else: # Client has disconnected
            self.logger.debug("Client disconnected")
            self.remove_player(player)

    # Expects response 'ok'
    # Block until 'ok' response in order to enforce order of communication
    # with client
    # If it recieves a response other than 'ok' the connection is ternimated
    # and error is sent to the client
    def cast(self, player: Player, message: str):
        """ Cast to server """
        connection = player.get_connection()
        connection.sendall(message.encode('utf-8'))

        (ready_read, _, _) = select.select([connection], [], [])
        data = connection.recv(1024)
        if data != b'': # Recieved response from client
            response = data.decode('utf-8')
            if response != "ok":
                connection.sendall(States.ERROR["error"])
                self.remove_player(player)
        else: # Client has disconnected
            self.logger.debug("Client disconnected")
            self.remove_player(player)

    ### LOGIN STATE ###
    def new_player(self, new_player, username, password):
        """ Handle new player login """
        if username in self.login_cache.get_dict():
            self.cast(
                new_player, 
                States.LOGIN["server commands"]["username used"]
            )
            return False
        self.login_cache.update(username, password)
        new_player.set_username(username)
        return True
    def existing_player(self, new_player, username, password):
        """ Handle existing player login """
        if username not in self.login_cache.get_dict():
            self.cast(
                new_player, 
                States.LOGIN["server commands"]["invalid login"]
            )
            return False
        if password == self.login_cache.get(username):
            new_player.set_username(username)
            return True
        else:
            self.cast(
                new_player, 
                States.LOGIN["server commands"]["invalid login"]
            )
            return False
    def login_error(self, login_type, new_player):
        """ Handle bad client response to login request """
        # If we don't get a valid response from the client 
        # raise an error and terminate the connection

        #TODO: for debugging - remove this
        self.logger.debug(f"Login type: {login_type}")

        self.cast(new_player, States.ERROR["error"])
        self.remove_player(new_player)
        return True

    ### CHOOSE_GAME STATE ###

    def add_player_to_game(self, player, room_name):
        """ Handle join game response """
        # attempt to add player to game
        game = None
        for waiting_game in self.waiting_game_rooms.get_dict():
            if waiting_game.get_room_name() == room_name:
                game = waiting_game
        if game == None:
            self.cast(player, States.CHOOSE_GAME["server commands"]["printing"] +
                              "You didn't enter a valid game room name, try again")
            return False
        max_players = game.get_max_players()
        # -1 means that we couldn't increment the value because we were already at max
        if self.waiting_game_rooms.increment_if_less_x(game, max_players) == -1:
            self.cast(player, States.CHOOSE_GAME["server commands"]["room_filled"])
            return False
        game.add_player(player)
        player.set_in_game(True)
        player.set_game(game)
        
        if game.get_max_players() == game.get_num_players():
            # start game
            self.logger.debug("starting game")
            self.waiting_game_rooms.remove(game)
            for pl in game.get_players():
                self.idle_players.remove(pl)
            t = threading.Thread(target=game.run, args=[self, game.get_players()])
            t.start()

            # Collect result of threading on game finish
            t.join()

            # Clean up game
            old_game_players = game.get_players()
            self.registered_games.decrement(game.get_game_type())
            for pl in old_game_players:
                self.idle_players.append(pl)
                pl.set_in_game(False)
                pl.set_game(None)

                # create and start new threads for all players to 
                # choose game again
                if pl != player:
                    self.logger.debug("Starting new player")
                    player_thread = threading.Thread(
                        target=self.handle_choose_game, 
                        args=[pl]
                    )
                    self.logger.debug("new player thread created")
                    self.player_threads.append(player_thread)
                    player_thread.start()
                    self.logger.debug("new player started")
                else:
                    # let this player choose new game
                    return False
        else:
            self.cast(
                player, 
                States.CHOOSE_GAME["server commands"]["waiting for players"]
            )
            return True
    
    def create_new_game(self, player, game_type_str):
        """ Handle create new game response """
        # attempt to create new game
        # This increments the value of registered_games if doing so creates 
        # a valid num of game instances
        # This is all done with the lock
        if game_type_str not in GAMES.keys():
            err = f"\n{Fore.RED}{game_type_str} IS NOT A VALID GAME TYPE. PLEASE TRY AGAIN.{Fore.RESET}"
            self.cast(player, States.CHOOSE_GAME["server commands"]["printing"] + err)
            # "YOU DIDN'T ENTER A VALID GAME TYPE. PLEASE TRY AGAIN.")
            return False

        val = self.registered_games.increment_if_less_x(game_type_str, MAX_GAME_INSTANCES)
        if val == -1:
            self.cast(
                player, 
                States.CHOOSE_GAME["server commands"]["max_game_inst"]
            )
            return False
        player_list = LockedList()
        player_list.append(player)
        new_game = GAMES[game_type_str](
            players=player_list, 
            room_name= f"{game_type_str}{val}"
        )
        player.set_in_game(True)
        player.set_game(new_game)
        
        if new_game.get_max_players() == 1:
            # start game
            self.logger.debug("starting game")
            for pl in new_game.get_players():
                self.idle_players.remove(pl)
            t = threading.Thread(
                target=new_game.run, 
                args=[self, new_game.get_players()]
            )
            t.start()

            # Collect result of threading on game finish
            t.join()

            # Clean up game
            self.logger.debug("Cleaning up game")
            old_game_players = new_game.get_players()
            self.registered_games.decrement(new_game.get_game_type())
            for pl in old_game_players:
                self.logger.debug("In loop")
                self.idle_players.append(pl)
                pl.set_in_game(False)
                pl.set_game(None)

                # create and start new threads for all players to 
                # choose game again
                if pl != player:
                    self.logger.debug("Starting new player")
                    player_thread = threading.Thread(
                        target=self.handle_choose_game, 
                        args=[pl]
                    )
                    self.logger.debug("new player thread created")
                    self.player_threads.append(player_thread)
                    player_thread.start()
                    self.logger.debug("new player started")
                else:
                    # let this player choose new game
                    return False
        else:
            # update waiting_game_rooms
            self.waiting_game_rooms.update(new_game, 1)
            self.cast(
                player, 
                States.CHOOSE_GAME["server commands"]["waiting for players"]
            )
            return True
        
    def client_quit(self, player):
        """ Handle quit cardgala response """
        state = States.END
        self.cast(player, state["server commands"]["end"])
        self.remove_player(player)
        return True
        
    def choose_game_error(self, choose_game_type, new_player):
        """ Handle bad response from client """
        # If we don't get a valid response from the client 
        # raise an error and terminate the connection

        #TODO: for debugging - remove this
        self.logger.debug(f"Choose game type: {choose_game_type}")

        self.cast(new_player, States.ERROR["error"])
        self.remove_player(new_player)
        return True
    
    def remove_player(self, player):
        """ Remove player from server """
        self.logger.debug("Removing player")
        if player.is_in_game():
            game = player.get_game()
            game.remove_player(player)
            if game in self.waiting_game_rooms:
                self.waiting_game_rooms.update(
                    game, 
                    self.waiting_game_rooms.get(game) - 1
                )
                if self.waiting_game_rooms.get(game) == 0:
                    self.logger.debug("Game removed")
                    self.waiting_game_rooms.remove(game)  
            else:
                #TODO: send message to other players - a player disconnected...
                for player in game.get_players():
                    message = "\n{Fore.RED}ONE OF THE OTHER PLAYERS DISCONNECTED. GAME OVER.{Fore.RESET}"
                    self.cast(player, States.CHOOSE_GAME["server commands"]["printing"] + message)

        if player in self.idle_players:
            self.idle_players.remove(player)                   

        player.get_connection().close()
        self.logger.debug("Done removing player")

    def send_waiting_players_update(self):
        """ Handle players waiting for enough players to join their room """
        while True:
            for game in self.waiting_game_rooms.get_dict().copy():
                num_players = game.get_num_players()
                max_players = game.get_max_players()
                for player in game.get_players():
                    message = f"\r{Fore.GREEN}Waiting for players to join. {num_players}/{max_players} joined{Fore.RESET}"
                    self.cast(
                        player, 
                        States.CHOOSE_GAME["server commands"]["printing over"]
                                + message
                    )
            time.sleep(1)
