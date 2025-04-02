import socket
import select
import sys

PORT = 9998

# List of possibe games to choose from
GAMES = ["blackjack"]

MAX_GAME_INSTANCES = 4

class Client():

    def __init__(self, hostname):
        self.hostname = hostname
        self.connection = None
        self.state = {}
        self.username = ""

        self.ERROR = {"error": "error"}

        self.LOGIN = {
            "message": "login",
            "invalid login": "invlo",
            "username used": "uused",
            "set username": "suser",
            "responses": {"enter_user_pass": self.login},
        }

        self.CHOOSE_GAME = {
            "message": "cgame",
            "max_game_inst": "maxgm",
            "room_filled": "froom",
            "responses":{"choose_game": self.choose_game}
        }

        self.END = {"end": "endgm"}

    def connect_to_server(self):
        print("connecting...")
        conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_sock.connect((self.hostname, PORT))
        print("connected!!!")

        self.connection = conn_sock

    def run_client(self):
        while True:
            print("waiting for input")
            input_list = [self.connection]
            try:
                (ready_read, _, _) = select.select(input_list, [], [])
            except ValueError:
                break

            print("doing stuff...")
            for sock in ready_read:
                message = sock.recv(1024).decode('utf-8')
                if message:
                    if message == self.LOGIN["message"]:
                        print("login message recieved")
                        self.state = self.LOGIN
                        self.state["responses"]["enter_user_pass"]()

                    elif message[0:5] == self.LOGIN["set username"]:
                        self.username = message[5:]
                        print(f"Welcome {self.username}!!")
                        self.connection.sendall("ok".encode('utf-8'))
                    
                    elif message == self.LOGIN["invalid login"]:
                        print("incorrect username or password, try again")
                        self.connection.sendall("ok".encode('utf-8'))

                    elif message == self.LOGIN["username used"]:
                        print("the username you entered is owned by another player. please choose a different username")
                        self.connection.sendall("ok".encode('utf-8'))

                    elif message[0:5] == self.CHOOSE_GAME["message"]:
                        print("Choose game!!")
                        self.state = self.CHOOSE_GAME
                        self.state["responses"]["choose_game"](message[5:])

                    elif message == self.CHOOSE_GAME["max_game_inst"]:
                        print(f"There can only be {MAX_GAME_INSTANCES} games of the same type running at the same time. Please join an existing game or choose a different type of game to play.")
                        self.connection.sendall("ok".encode('utf-8'))   

                    elif message == self.CHOOSE_GAME["room_filled"]:
                        print("The room filled up before you got in. Please try again.")
                        self.connection.sendall("ok".encode('utf-8'))  

                    elif message == self.END["end"]:
                        print("Thank you for playing CARD-GALA, goodbye!")
                        self.connection.sendall("ok".encode('utf-8'))  
                        sock.close()
                        exit(0)  
                    
                    elif message == self.ERROR["error"]:
                        print("server recieved bad message, closing connection")
                        sock.close()
                        exit(1)           

                    else:
                        print(f"Error: incorrect message {message} recieved")
                        sock.close()
                        exit(1)
                else:
                    print("Server disconnected")
                    sock.close()
                    exit(1)
    
    def login(self):
        print("Welcome to CARD-GALA")
        entered_credentials = False
        response = ""
        while not entered_credentials:
            returning_user = input("Are you a returning user (y/n)? ")
            if returning_user == "y":
                username = self.get_valid_username()
                password = self.get_valid_password()
                response = "exist" + username + password
                entered_credentials = True
            elif returning_user == "n":
                username = self.get_valid_username()
                password = self.get_valid_password()
                response = "newpl" + username + password
                entered_credentials = True
            else:
                print("Invalid input - try again (must enter y or n)")
        self.connection.sendall(response.encode('utf-8'))
    
    def get_valid_username(self):
        valid_username = False
        while not valid_username:
            username = input("Enter your username: ")
            if len(username) != 5:
                print(f"Invalid username {username}, username must must be 5 chars")
            else:
                return username
            
    def get_valid_password(self):
        valid_password = False
        while not valid_password:
            password = input("Enter your password: ")
            if len(password) != 5:
                print(f"Invalid password {password}, password must must be 5 chars")
            else:
                return password
            
    def choose_game(self, message):
        room_names = []
        # get the list of games from the remainder of the sent string
        waiting_games_str = message
        can_join = False

        if waiting_games_str == "":
            print("There are no games waiting to start -- create a new game")
        else:
            can_join = True
            # Client wants to know type of game, room name, num spots left, whos in the game
            # games are separated by '|' symbol, subcategories by commas
            print("Choose from one of the following games or create a new game")
            waiting_games = waiting_games_str.split("|")
            print(f"Waiting games: {waiting_games}")
            num = 1
            for game in waiting_games:
                if game != "":
                    print(f"game: {game}")
                    game_info = game.split(":")
                    print(f"game info: {game_info}")
                    room_names.append(game_info[0])
                    print(f"Game #{num}")
                    print(f"room name: {game_info[0]}")
                    print(f"game type: {game_info[1]}")
                    print(f"players: {game_info[2]}")
                    print(f"number of spots left: {game_info[3]}")
                    print()
                    num += 1

        # Client chooses one of the availible games or chooses to create a new game 
        # from the list GAMES
        # Also sends response to server (if client choose an existing game
        # server needs to know which game it is)
        response = ""
        chosen_game = False
        while not chosen_game:
            create_or_join = input("Do you want to create a new game or join an existing one? (c/j). Type q to quit the game.")
            if create_or_join == "j":
                if can_join:
                    num_rooms = len(room_names)
                    chosen_game_num = self.select_valid_game_num(num_rooms)
                    response = "egame" + str(room_names[int(chosen_game_num) - 1])
                    chosen_game = True
                else:
                    print("No games to join - please create a new game")
                    chosen_game = False
            elif create_or_join == "c":
                game_type = input(f"Which of the following games do you want to play: {GAMES}")
                response = "ngame" + game_type
                chosen_game = True
            elif create_or_join == "q":
                response = "quitg"
                chosen_game = True
            else:
                print("Invalid input - try again (must enter c or j)")
        self.connection.sendall(response.encode('utf-8'))

    def select_valid_game_num(self, num_rooms):
        selected_valid_num = False
        while not selected_valid_num:
            chosen_game_num = input("Choose a the number of the game that you would like to play")
            if int(chosen_game_num) > num_rooms:
                print(f"The number you selected {chosen_game_num} is greater than the number of games {num_rooms}. Please try again.")
            else:
                return chosen_game_num
                


