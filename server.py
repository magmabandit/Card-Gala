import socket
import select
import threading

from player import Player
from locked_dict import LockedDict
from locked_list import LockedList
from game import Game

PORT = 9998
MAX_GAME_INSTANCES = 4 #TODO: what should this value be?

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
                "availible games": "agame",
            },
            "responses" : {},
        }

    #TODO: take input from stdin - if user types 'quit\n' the server cleans up and stops running
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
        finally:
            for thread in self.player_threads:
                thread.join()
    
    def host_player(self, player):
        ### LOGIN ###
        state = self.LOGIN

        logged_in = False
        error = False
        while not logged_in:
            print("logging in!!")
            # Initiate the login sequence and get 
            # returning/exisiting user, username, password from client
            # TODO: usernames & passwords must currently be 5 chars - is that ok?
            response = self.call(player, state["commands"]["login"])
            if response is None: # The client connection closed
                print("Killing thread")
                return #kill the thread
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
                error = True
        
        if error:
            player.get_connection().close()
            self.idle_players.remove(player)
            return # If there is an error, kill the thread
        
        self.cast(player, state["commands"]["set username"] + player.get_username())

        ### CHOOSE GAME ###
        print("Entering choose game state")
        state = self.CHOOSE_GAME
        self.call(player, state["commands"]["choose game"] + self.waiting_game_rooms.dict_to_string())

        # response = self.call(player, state["commands"]["availible games"])

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
