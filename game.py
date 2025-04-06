from player import Player
from abc import ABC, abstractmethod
from locked_list import LockedList

class Game(ABC):
    """
    class Game
    Defines the state of a game and some game attributes
    """
    def __init__(self, max_players, players, game_type, room_name):
        """
        max_players: num players required to start the game
        players: the list of player objects in the game
        game_type: the str name of the type of game
        room_name: the game room specific name
        """
        self.max_players: int = max_players
        self.players: LockedList = players
        self.game_type: str = game_type
        self.room_name: str = room_name

    ### Subclasses must define this function ###
    ### This is the function that will be run by the server to
    ### start a new game room process
    @abstractmethod
    def run():
        raise NotImplementedError
    
    def add_player(self, player):
        """
        adds a player object to the players LockedList
        Returns: None
        """
        self.players.append(player)
    
    #TODO: haven't implemented this function
    def leave_game():
        return
    
    ### Getters for game class variables ###

    def get_max_players(self):
        return self.max_players
    
    def get_players(self):
        return self.players.get_list()
    
    def get_num_players(self):
        return self.players.get_length()
    
    def get_room_name(self):
        return self.room_name
    
    def get_game_type(self):
        return self.game_type
    