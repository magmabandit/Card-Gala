import socket
import select
import threading
import sys

from player import Player
from locked_dict import LockedDict
from locked_list import LockedList
from game import Game
from BJGame import BJGame

PORT = 9998
MAX_GAME_INSTANCES = 4 #TODO: what should this value be?
GAMES = {"blackjack": BJGame}
ERROR = "e"

class Server:

    def __init__(self):
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind(('', PORT))
        self.listen_socket.listen(100) # TODO: do we need to pass a larger arg to this function so we can accept multiple connections at the same time?

        self.login_cache = LockedDict()
        self.idle_players = LockedList()

        self.registered_games = LockedDict()
        self.registered_games.update("blackjack", 0) #TODO: list of names of possible games
        self.waiting_game_rooms = LockedDict()

        self.player_threads = []

        self.ERROR = {"error": "error"}
        
        self.LOGIN = {
            "commands" : {
                "login": "login",
                "invalid login": "invlo",
                "username used": "uused",
                "set username": "suser",
            },
            "responses" : {
                "login": {"newpl": self.new_player, "exist": self.existing_player, "error": self.login_error},
            },
        }

        self.CHOOSE_GAME = {
            "commands" : {
                "choose game": "cgame",
                "max_game_inst": "maxgm",
                "room_filled": "froom",
            },
            "responses" : {
                "choose game": {"egame": self.add_player_to_game, "ngame": self.create_new_game, "quitg": self.client_quit, "error": self.choose_game_error}
            },
        }

        self.END = {"end": "endgm"}

    #TODO: clean cleanup with quit
    def run_server(self):
        try:
            while True:
                # When a new client attempts to connect, accept the connection
                # and init the new player
                print("Accepting new connection")
                new_conn, addr = self.listen_socket.accept() # this command is blocking by default
                new_player = Player(connection=new_conn)
                self.idle_players.append(new_player)
                print("New connection accepted")

                print("Starting new player")
                player_thread = threading.Thread(target=self.host_player, args=[new_player])
                print("new player thread created")
                self.player_threads.append(player_thread)
                player_thread.start()
                print("new player started")

                for t in self.player_threads:
                    if not t.is_alive():
                        t.join()
        finally:
            for thread in self.player_threads:
                thread.join()
    
    def host_player(self, player):
        if self.handle_login(player) == ERROR:
            return
        if self.handle_choose_game(player) == ERROR:
            return 
    
    def handle_login(self, player):
        state = self.LOGIN

        logged_in = False
        while not logged_in:
            print("logging in!!")
            # Initiate the login sequence and get 
            # returning/exisiting user, username, password from client
            # TODO: usernames & passwords must currently be 5 chars - is that ok?
            response = self.call(player, state["commands"]["login"])
            if response is None: # The client connection closed
                print("Killing thread")
                return ERROR #kill the thread
            login_type = response[0:5]
            username = response[5:10]
            password = response[10:15]

            print(f"login type: {login_type}, username: {username}, password: {password}")

            # Log player in
            #TODO: is it ok for multiple computers to log into the same account?
            responses = state["responses"]["login"]
            if login_type in responses:
                logged_in = responses[login_type](player, username, password)
            else:
                logged_in = responses["error"](login_type, player)
                return ERROR # If there is an error, kill the thread
        
        self.cast(player, state["commands"]["set username"] + player.get_username())
    
    def handle_choose_game(self, player):
        state = self.CHOOSE_GAME

        chosen_game = False
        while not chosen_game:
            print("Entering choose game state")
            response = self.call(player, state["commands"]["choose game"] + self.waiting_game_rooms.format_waiting_games_for_send())
            if response is None: # The client connection closed
                print("Killing thread")
                return ERROR #kill the thread
            
            choose_game_type = response[0:5]
            game = response[5:]
            
            responses = state["responses"]["choose game"]
            if choose_game_type in responses:
                chosen_game = responses[choose_game_type](player, game)
            else:
                chosen_game = responses["error"](choose_game_type, player)
                return ERROR 

    # Expects reponse - blocking until response is recieved
    # If a player has disconnected the player will be removed
    #   from idle_players and the connection is closed
    def call(self, player: Player, message: str):
        print(f"Sending message {message}")
        connection = player.get_connection()
        connection.sendall(message.encode('utf-8'))
        print("Message sent")
     
        (ready_read, _, _) = select.select([connection], [], [])
        print ("recieved response")
        data = connection.recv(1024)
        if data != b'': # Recieved response from client
            response = data.decode('utf-8')
            print(f"Response: {response}")
            return response
        else: # Client has disconnected
            print("Client disconnected")
            self.idle_players.remove(player)
            connection.close()

    # Expects response 'ok'
    # Block until 'ok' response in order to enforce order of communication with client
    # If it recieves a response other than 'ok' the connection is ternimated and error
    # is sent to the client
    def cast(self, player: Player, message: str):
        connection = player.get_connection()
        connection.sendall(message.encode('utf-8'))

        (ready_read, _, _) = select.select([connection], [], [])
        print ("recieved response")
        data = connection.recv(1024)
        if data != b'': # Recieved response from client
            response = data.decode('utf-8')
            if response != "ok":
                connection.sendall(self.ERROR["error"])
                self.idle_players.remove(player)
                connection.close()
        else: # Client has disconnected
            print("Client disconnected")
            self.idle_players.remove(player)
            connection.close()

    ### LOGIN STATE ###
    def new_player(self, new_player, username, password):
        if username in self.login_cache.get_dict():
            self.cast(new_player, self.LOGIN["commands"]["username used"])
            return False
        self.login_cache.update(username, password)
        new_player.set_username(username)
        return True
    def existing_player(self, new_player, username, password):
        if username not in self.login_cache.get_dict():
            self.cast(new_player, self.LOGIN["commands"]["invalid login"])
            return False
        if password == self.login_cache.get(username):
            new_player.set_username(username)
            return True
        else:
            self.cast(new_player, self.LOGIN["commands"]["invalid login"])
            return False
    def login_error(self, login_type, new_player):
        # If we don't get a valid response from the client 
        # raise an error and terminate the connection

        #TODO: for debugging - remove this
        print(f"Login type: {login_type}")

        self.cast(new_player, self.ERROR["error"])
        self.idle_players.remove(new_player)
        new_player.get_connection().close()
        return True

    ### CHOOSE_GAME STATE ###

    def add_player_to_game(self, player, room_name):
        # attempt to add player to game
        game = None
        for waiting_game in self.waiting_game_rooms.get_dict():
            if waiting_game.get_room_name() == room_name:
                game = waiting_game
        if game == None:
            print("Error")
            return False
        max_players = game.get_max_players()
        # -1 means that we couldn't increment the value because we were already at max
        if self.waiting_game_rooms.increment_if_less_equal_x(game, max_players) == -1:
            self.cast(player, self.CHOOSE_GAME["commands"]["room_filled"])
            return False
        game.add_player(player)
        
        if game.get_max_players() == game.get_num_players():
            # start game TODO
            print("starting game")
            # Do multiprocessing stuff
            # Collect result of multiprocessing on game finish
            # create and start new threads for all players to choose game again
            # let this player choose new game
        else:
            return True
    
    def create_new_game(self, player, game_type_str):
        # attempt to create new game
        # This increments the value of registered_games if doing so creates a valid num of game instances
        # This is all done with the lock
        val = self.registered_games.increment_if_less_equal_x(game_type_str, MAX_GAME_INSTANCES)
        if val == -1:
            self.cast(player, self.CHOOSE_GAME["commands"]["max_game_inst"])
            return False
        player_list = LockedList()
        player_list.append(player)
        new_game = GAMES[game_type_str](players=player_list, room_name= f"{game_type_str}{val}")
        
        if new_game.get_max_players() == 1:
            # start game TODO
            print("starting game")
            # Do multiprocessing stuff
            # Collect result of multiprocessing on game finish
            # create and start new threads for all players to choose game again
            # let this player choose new game
        else:
            # update waiting_game_rooms
            self.waiting_game_rooms.update(new_game, 1)
            return True
        
    def client_quit(self, player, game):
        state = self.END
        self.cast(player, state["end"])
        self.idle_players.remove(player)
        player.get_connection().close()
        return True
        
    def choose_game_error(self, choose_game_type, new_player):
        # If we don't get a valid response from the client 
        # raise an error and terminate the connection

        #TODO: for debugging - remove this
        print(f"Choose game type: {choose_game_type}")

        self.cast(new_player, self.ERROR["error"])
        self.idle_players.remove(new_player)
        new_player.get_connection().close()
        return True
