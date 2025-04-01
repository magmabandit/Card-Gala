from player import Player
from abc import ABC, abstractmethod

class Game(ABC):
    def __init__(self, max_players, players, game_type, room_name):
        self.max_players: int = max_players
        self.players: list[Player] = players
        self.game_type: str = game_type
        self.room_name: str = room_name

    @abstractmethod
    def run():
        raise NotImplementedError
    
    def leave_game():
        return
    
    def get_max_players(self):
        return self.max_players
    
    def get_players(self):
        return self.players
    
    def get_room_name(self):
        return self.room_name
    
    def get_game_type(self):
        return self.game_type
    