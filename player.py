# player.py
# stores and gives access to client-related data

import socket

class Player():
    """
    Player class
    Represents the client connection on the server
    """
    def __init__(self, connection: socket.socket):
        """
        __init__

        args: 
            connection: the TCP socket connection between the server and
                        the client represented by a specific player object
        Returns: None
        Results: Initializes player variable and sets the players
                 connection
        """
        self.username = ""
        self.connection = connection
        self.in_game = False
        self.game = None

    # Getters and setters for player class variables

    def get_username(self):
        return self.username
    
    def get_connection(self):
        return self.connection
    
    def get_game(self):
        return self.game
    
    def is_in_game(self):
        return self.in_game
    
    def set_username(self, username: str):
        self.username = username
    
    def set_connection(self, connection: socket.socket):
        self.connection = connection

    def set_game(self, game):
        self.game = game
    
    def set_in_game(self, in_game: bool):
        self.in_game = in_game