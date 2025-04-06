import socket
import select
import sys

from states import States

PORT = 9998

# List of possibe games to choose from
GAMES = ["blackjack"]

MAX_GAME_INSTANCES = 4

class Client():

    def __init__(self, hostname):
        self.hostname = hostname
        self.connection = None
        self.username = ""

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
                    if message == States.LOGIN["server commands"]["login"]:
                        print("login message recieved")
                        self.state = States.LOGIN
                        self.login()

                    elif message[0:5] == States.LOGIN["server commands"]["set username"]:
                        self.username = message[5:]
                        print(f"Welcome {self.username}!!")
                        self.connection.sendall("ok".encode('utf-8'))
                    
                    elif message == States.LOGIN["server commands"]["invalid login"]:
                        print("incorrect username or password, try again")
                        self.connection.sendall("ok".encode('utf-8'))

                    elif message == States.LOGIN["server commands"]["username used"]:
                        print("the username you entered is owned by another player. please choose a different username")
                        self.connection.sendall("ok".encode('utf-8'))

                    elif message[0:5] == States.CHOOSE_GAME["server commands"]["choose game"]:
                        print("Choose game!!")
                        self.choose_game(message[5:])

                    elif message == States.CHOOSE_GAME["server commands"]["max_game_inst"]:
                        print(f"There can only be {MAX_GAME_INSTANCES} games of the same type running at the same time. Please join an existing game or choose a different type of game to play.")
                        self.connection.sendall("ok".encode('utf-8'))   

                    elif message == States.CHOOSE_GAME["server commands"]["room_filled"]:
                        print("The room filled up before you got in. Please try again.")
                        self.connection.sendall("ok".encode('utf-8'))  

                    elif message == States.CHOOSE_GAME["server commands"]["waiting for players"]:
                        print("Waiting for players to join the game...")
                        self.connection.sendall("ok".encode('utf-8')) 
                    
                    ### Blackjack specific stuff ###
                    
                    elif message[0:5] == States.BLACKJACK["server commands"]["printing"]:
                        print(message[5:])
                        self.connection.sendall("ok".encode('utf-8')) 
                    
                    elif message == States.BLACKJACK["server commands"]["enter money"]:
                        self.enter_money()
                    
                    elif message[0:5] == States.BLACKJACK["server commands"]["place bet"]:
                        self.place_bet(message[5:])

                    elif message[0:5] == States.BLACKJACK["server commands"]["Player-choice"]:
                        move = input("Do you want to (H)it or (S)tand? ").lower()
                        self.connection.sendall(move.encode('utf-8')) 
                    
                    elif message[0:5] == States.BLACKJACK["server commands"]["Player-choice2"]:
                        game_check = input("Play again? (Y/N): ").lower()
                        self.connection.sendall(game_check.encode('utf-8')) 

                    elif message[0:5] == States.BLACKJACK["server commands"]["intial hand"]:
                        hand = message[5:]
                        hand_msgs = hand.split(",")
                        print(f"\nYour Hand: {hand_msgs[0]}")
                        print(f"Hand Value: {hand_msgs[1]}")
                        print(f"Dealer's First Card: {hand_msgs[2]}")
                        print(f"Dealer's Hand Value: {hand_msgs[3]}")
                        print("It is your turn")

                        self.connection.sendall("ok".encode('utf-8')) 
                    
                    ###########################################################

                    elif message == States.END["server commands"]["end"]:
                        print("Thank you for playing CARD-GALA, goodbye!")
                        self.connection.sendall("ok".encode('utf-8'))  
                        sock.close()
                        exit(0)
                    
                    elif message == States.ERROR["server commands"]["error"]:
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
            
    ### Blackjack functions ###
    def enter_money(self):
        entered_money = False
        while not entered_money:
            value = input("Enter the amount of money you want to start with: ")
            if value.isdigit() and int(value) > 0:
                self.connection.sendall(value.encode('utf-8'))
                entered_money = True
            else:
                print("You did not enter a valid amount of Money. Come "
                "back when you have actual money.")
    
    def place_bet(self, money):
        print(f"You have ${money}")
        placed_bet = False
        while not placed_bet:
            bet = input("Enter your bet: ")
            if bet.isdigit() and int(bet) > 0 and int(bet) <= int(money):
                self.connection.sendall(bet.encode('utf-8'))
                placed_bet = True                
            else:
                print("You did not enter a valid bet. Bet must be > $0 and within your available money")




                


