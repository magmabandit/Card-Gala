import socket

class Player():
    def __init__(self, connection: socket.socket):
        self.username = ""
        self.connection = connection
        self.in_game = False

    def get_username(self):
        return self.username
    
    def get_connection(self):
        return self.connection
    
    def is_in_game(self):
        return self.in_game
    
    def set_username(self, username: str):
        self.username = username
    
    def set_connection(self, connection: socket.socket):
        self.connection = connection
    
    def set_in_game(self, in_game: bool):
        self.in_game = in_game