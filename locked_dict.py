import threading

class LockedDict():
    """
    class LockedDict
    Thread-safe dictionaries
    """
    def __init__(self):
        self.dict = {}
        self.lock = threading.Lock()

    # Add a new key-value or update an existing one
    def update(self, key, value):
        """
        Updates the value of the element at the specified index
        If the specified key does not exist in the dictionary a
        new key-value pair is created
        Returns: None
        """
        with self.lock:
            self.dict[key] = value
    
    def remove(self, key):
        """
        Removes the key-value pair specified by the key
        Returns: None
        """
        with self.lock:
            self.dict.pop(key)

    def get(self, key):
        """
        Returns: the value specified by the key
        """
        with self.lock:
            return self.dict[key]
        
    def get_dict(self):
        """
        Returns: the dictionary
        Note: the returned dictionary is not thread-safe
        """
        with self.lock:
            return self.dict
        
    def increment_if_less_x(self, key, x):
        """
        If the value specified by dict[key] is less than the
        value specified by x, return the value specified by
        dict[key], otherwise return -1

        Note: the function expects that no values in the dictionary
              have the value -1 
        """
        with self.lock:
            if self.dict[key] < x:
                self.dict[key] += 1
                return self.dict[key]
            else:
                return -1
    
    def decrement(self, key):
        """
        Decrements the value specified by dict[key] by 1
        Returns: None
        """
        with self.lock:
            self.dict[key] -= 1
            
    ### waiting_games specific functions ###
    ### These functions should only be called by waiting_game_rooms ###

    def format_waiting_games_for_send(self):
        """
        Returns: a string that can be parsed for data about all of the
                 game object keys in a list
        Note: this function can only be called on LockDict's where the
              keys are all game objects
        """
        with self.lock:
            response = ""
            for game in self.dict.keys():
                game_type = game.get_game_type() # Game type
                room_name = game.get_room_name() # Room name
                print("TYPE OF PLAYERS LIST OBJ ====>", type(game.players))
                players = game.get_players()
                players = list(map(lambda x: x.get_username(), players))
                # Username of players in the room
                players_string = str(players)
                # Number of spots left in the room
                num_spots_left = str(game.get_max_players() - len(players))
                response += ("|" + 
                             room_name + ":" + 
                             game_type + ":" + 
                             players_string + ":" + 
                             num_spots_left)
            return response
        