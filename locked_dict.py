import threading

class LockedDict():
    def __init__(self):
        self.dict = {}
        self.lock = threading.Lock()

    # Add a new key-value or update an existing one
    def update(self, key, value):
        with self.lock:
            self.dict[key] = value
    
    def remove(self, key):
        with self.lock:
            self.dict.pop(key)

    def get(self, key):
        with self.lock:
            return self.dict[key]
        
    def get_dict(self):
        with self.lock:
            return self.dict
        
    # Should only be called by waiting_game_rooms
    # This function is only in this class because I want to use the lock for it
    def format_waiting_games_for_send(self):
        with self.lock:
            response = ""
            for game in self.dict.keys():
                game_type = game.get_game_type()
                room_name = game.get_room_name()
                players = self.dict[game]
                players_string = str(players)
                num_spots_left = game.get_max_players() - len(players)
                response += "|" + room_name + "," + game_type + "," + players_string + "," + num_spots_left
            return response