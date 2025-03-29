from player import Player

class Game():
    def __init__(self):
        self.max_players: int = None
        self.players: list[Player] = None
        self.name: str = None
    