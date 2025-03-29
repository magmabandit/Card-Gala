import socket
import select
import threading

from player import Player
from locked_dict import LockedDict
from locked_list import LockedList

PORT = 9998
MAX_GAME_INSTANCES = 4 #TODO: what should this value be?

class Server:

    def __init__(self):
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind(('', PORT))
        self.listen_socket.listen() # TODO: do we need to pass a larger arg to this function so we can accept multiple connections at the same time?

        self.login_cache = LockedDict()
        self.idle_players = LockedList()

        self.player_threads = []

    def run_server(self):
        try:
            while True:
                read_list = [self.listen_socket]
                (ready_read, _, _) = select.select(read_list, [], [])

                # TODO: Do this with threading?
                for sock in ready_read:

                    # When a new client attempts to connect, accept the connection
                    # and init the new player
                    new_conn, addr = sock.accept()
                    new_player = Player(connection=new_conn)
                    self.idle_players.append(new_player)

                    player_thread = threading.Thread(target=self.host_player, args=(new_player))
                    self.player_threads.append(player_thread)
                    player_thread.start()
        finally:
            for thread in self.player_threads:
                thread.join()
    
    def host_player(self, player):
        state = self.LOGIN

        logged_in = False
        error = False
        while not logged_in:
            # Initiate the login sequence and get 
            # returning/exisiting user, username, password from client
            # TODO: usernames & passwords must currently be 5 chars - is that ok?
            response = self.call(player, state["commands"]["login"])
            login_type = response[0:5]
            username = response[5:10]
            password = response[10:15]

            # Log player in
            responses = state["responses"]["login"]
            if login_type in responses:
                logged_in = responses[login_type](player, username, password)
            else:
                logged_in = responses["error"](login_type, player)
                error = True
        
        if error:
            return # If there is an error, kill the thread

        print("Entering choose game state")
        state = self.CHOOSE_GAME
        self.call(player, state["commands"]["choose game"])

    # Expects reponse - blocking until response is recieved
    # If a player has disconnected the player will be removed
    #   from idle_players and the connection is closed
    def call(self, player: Player, message: str):
        connection = player.get_connection()
        connection.sendall(message.encode('utf-8'))

        recieved_response = False
        response = ""
        while not recieved_response:
            (ready_read, _, _) = select.select([connection], [], [])
            if len(ready_read) > 0:
                data = connection.recv(1024)
                if data != b'': # Recieved response from client
                    response = data.decode('utf-8')
                    recieved_response = True
                else: # Client has disconnected
                    self.idle_players.remove(player)
                    connection.close()
        return response

    # Does not expect response
    # Non-blocking - just sends message
    def cast(self, player: Player, message: str):
        connection = player.get_connection()
        connection.sendall(message.encode('utf-8'))

    ### LOGIN STATE ###
    def new_player(self, new_player, username, password):
        self.login_cache.update(username, password)
        new_player.set_username(username)
        return True
    def existing_player(self, new_player, username, password):
        if password == self.login_cache.get(username):
            new_player.set_username(username)
            return True
        else:
            self.cast(new_player, "invalid login")
            return False
    def login_error(self, login_type, new_player):
        # If we don't get a valid response from the client 
        # raise an error and terminate the connection

        #TODO: for debugging - remove this
        print(f"Login type: {login_type}")

        self.cast(new_player, "error")
        self.idle_players.remove(new_player)
        new_player.get_connection().close()
        return True
    
    LOGIN = {
        "commands" : {
            "login": "login",
            "invalid login": "invlo",
            "error":"error",
        },
        "responses" : {
            "login": {"newpl": new_player, "exist": existing_player, "error": login_error},
        },
    }

    ### CHOOSE_GAME STATE ###
    
    CHOOSE_GAME = {
        "commands" : {
            "choose game": "cgame",
        },
        "responses" : {},
    }
