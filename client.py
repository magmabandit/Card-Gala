# client.py
# implementation of client-side logic for login, joining games, and in-game
# commands 


import socket
import select
import sys

# for PTB
import tqdm
import time

from colorama import Fore, Back, Style
from ascii_art import art

from states import States

PORT = 9998

# List of possibe games to choose from
GAMES = ["blackjack", "blackjack2player", "crazy8", "pressthebutton"]

MAX_GAME_INSTANCES = 4

class Client():
    """
    
    hostname: hostname IP of server
    connection: socket object to communicate to server
    username: str type name of user
    DEBUG: flag for print statements
    
    """
    def __init__(self, hostname, debug):
        self.hostname = hostname
        self.connection = None
        self.username = ""
        self.DEBUG = debug # debug flag

    def connect_to_server(self):
        """
        attempts to connect to server using given hostname. Upon success, sets
        client connection to newly retrieved socket object
        """
        if self.DEBUG:
            print("connecting...", file=sys.stderr)
        conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_sock.connect((self.hostname, PORT))
        if self.DEBUG:
            print("connected!!!", file=sys.stderr)

        self.connection = conn_sock

    def run_client(self):
        """
        State in which the client may recieve/send messages to the server.
        Includes game specific commands.
        """
        while True:
            if self.DEBUG:
                print("waiting for input", file=sys.stderr)
            input_list = [self.connection]
            try:
                (ready_read, _, _) = select.select(input_list, [], [])
            except ValueError:
                break
            if self.DEBUG:
                print("doing stuff...", file=sys.stderr)
            for sock in ready_read:
                message = sock.recv(1024).decode('utf-8', 'ignore')
                if message:
                    if message == States.LOGIN["server commands"]["login"]:
                        if self.DEBUG:
                            print("login message recieved", file=sys.stderr)
                        self.state = States.LOGIN
                        self.login()

                    elif message[0:5] == States.LOGIN["server commands"]["set username"]:
                        self.username = message[5:]
                        print(f"{Fore.GREEN}SUCCESSFULLY LOGGED IN!\n")
                        print(f"{Fore.WHITE}WELCOME {self.username}!")
                        self.connection.sendall("ok".encode('utf-8'))
                    
                    elif message == States.LOGIN["server commands"]["invalid login"]:
                        print(f"{Fore.RED}INCORRECT USERNAME USERNAME OR PASSWORD: PLEASE TRY AGAIN{Fore.WHITE}\n")
                        self.connection.sendall("ok".encode('utf-8'))

                    elif message == States.LOGIN["server commands"]["username used"]:
                        print(f"{Fore.RED}THE USERNAME YOU ENTERED IS OWNED BY ANOTHER PLAYER.\nPLEASE CHOOSE A DIFFERENT USERNAME.\n")
                        self.connection.sendall("ok".encode('utf-8'))

                    elif message[0:5] == States.CHOOSE_GAME["server commands"]["choose game"]:
                        print(f"\n{Fore.WHITE}CHOOSE A GAME FROM THE LIST BELOW OR CREATE A NEW ONE: ")
                        self.choose_game(message[5:])

                    elif message == States.CHOOSE_GAME["server commands"]["max_game_inst"]:
                        print(f"THERE CAN ONLY BE {MAX_GAME_INSTANCES} GAMES OF THE SAME TYPE RUNNING AT THE SAME TIME.\n \
                              PLEASE JOIN AN EXISTING GAME OR CHOOSE A DIFFERENT TYPE OF GAME TO PLAY.")
                        self.connection.sendall("ok".encode('utf-8'))   

                    elif message == States.CHOOSE_GAME["server commands"]["room_filled"]:
                        print("THE ROOM FILLED UP BEFORE YOU GOT IN. PLEASE TRY AGAIN.")
                        self.connection.sendall("ok".encode('utf-8'))  

                    elif message == States.CHOOSE_GAME["server commands"]["waiting for players"]:
                        print(f"\n{Fore.GREEN}WAITING FOR PLAYERS TO JOIN THE GAME...{Fore.WHITE}")
                        self.connection.sendall("ok".encode('utf-8')) 

                    elif message[0:5] == States.CHOOSE_GAME["server commands"]["printing"]:
                        print(message[5:])
                        self.connection.sendall("ok".encode('utf-8')) 

                    elif message[0:5] == States.CHOOSE_GAME["server commands"]["printing over"]:
                        print(message[5:], end="\r")
                        self.connection.sendall("ok".encode('utf-8')) 
                    
                    ### Blackjack specific stuff ###
                    
                    elif message[0:5] == States.BLACKJACK["server commands"]["printing"]:
                        print(message[5:])
                        self.connection.sendall("ok".encode('utf-8')) 
                    
                    elif message == States.BLACKJACK["server commands"]["enter money"]:
                        self.enter_money()
                    elif message == States.BLACKJACK["server commands"]["rank"]:
                        value = input("ENTER RANK OF CARD. FOR EXAMPLE: A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K. ")
                        self.connection.sendall(value.encode('utf-8'))
                    elif message == States.BLACKJACK["server commands"]["suit"]:
                        value = input("ENTER SUIT OF CARD: Hearts, Diamonds, Clubs, Spades. ")
                        self.connection.sendall(value.encode('utf-8'))
                    elif message == States.BLACKJACK["server commands"]["suit_change"]:
                        value = input("ENTER SUIT OF THE TOP CARD: Hearts, Diamonds, Clubs, Spades. ")
                        self.connection.sendall(value.encode('utf-8'))
                    elif message[0:5] == States.BLACKJACK["server commands"]["place bet"]:
                        self.place_bet(message[5:])

                    elif message[0:5] == States.BLACKJACK["server commands"]["Player-choice"]:
                        move = input(f"\nDO YOU WANT TO HIT {Style.DIM}(H){Style.NORMAL} OR STAND {Style.DIM}(S){Style.NORMAL}? ").lower()
                        self.connection.sendall(move.encode('utf-8')) 
                    
                    elif message[0:5] == States.BLACKJACK["server commands"]["Player-choice2"]:
                        game_check = input(f"{Fore.BLUE}PLAY AGAIN (Y/N)? {Fore.WHITE}").lower()
                        self.connection.sendall(game_check.encode('utf-8')) 

                    elif message[0:5] == States.BLACKJACK["server commands"]["intial hand"]:
                        hand = message[5:]
                        hand_msgs = hand.split(",")
                        your_cards = hand_msgs[0].split()
                        # print(your_cards)
                        # print(hand_msgs)
                        # print("HERE????", art[your_cards[0]], art[your_cards[1]])
                        print(f"\n{Style.DIM}-----------------------------------------------------------------------------{Style.NORMAL}")
                        print(f"\nYOUR HAND: \n\n{art[your_cards[0]]}\n\n{art[your_cards[1]]}\n")
                        print(f"YOUR HAND VALUE: {hand_msgs[1]}\n")
                        # print(art[your_cards[0]], art[your_cards[1]])
                        print(f"DEALER'S FIRST CARD: \n\n{art[hand_msgs[2]]}\n")
                        # print(art[hand_msgs[2]])
                        print(f"DEALER'S HAND VALUE: \b{hand_msgs[3]}")
                        print(f"\n{Fore.BLUE}IT IS YOUR TURN!{Fore.WHITE}")

                        self.connection.sendall("ok".encode('utf-8')) 

                    elif message[0:5] == States.PRESSTHEBUTTON["server commands"]["printing"]:
                        print(message[5:])
                        self.connection.sendall("ok".encode('utf-8')) 
                    elif message[0:5] == States.PRESSTHEBUTTON["server commands"]["countdown"]:
                        t = int(message[5:])
                        for i in tqdm.tqdm(range(t)):
                            time.sleep(0.5)
                        self.connection.sendall("ok".encode('utf-8')) 
                    elif message[0:5] == States.PRESSTHEBUTTON["server commands"]["listen-keypress"]:
                        key = message[5:]
                        timeout = 2 # seconds
                    
                        try:
                            i, _, _ = select.select([sys.stdin], [], [], timeout)
                            if i:
                                pressed = sys.stdin.read(1)
                                if pressed == key:
                                    self.connection.sendall("t".encode('utf-8'))
                                else:
                                    self.connection.sendall("f".encode('utf-8'))
                            else:
                                # Timeout expired
                                self.connection.sendall("f".encode('utf-8'))
                        except Exception as e:
                            print(f"keypress error: {e}")
                            self.connection.sendall("f".encode('utf-8'))
                            
                    ###########################################################

                    elif message == States.END["server commands"]["end"]:
                        print(f"\n{Fore.BLUE}THANK YOU FOR PLAYING CARD-GALA, GOODBYE!{Fore.WHITE}")
                        self.connection.sendall("ok".encode('utf-8'))  
                        sock.close()
                        exit(0)
                    
                    elif message == States.ERROR["server commands"]["error"]:
                        if self.DEBUG:
                            print("server recieved bad message, closing connection", file=sys.stderr)
                        sock.close()
                        exit(1)           

                    else:
                        if self.DEBUG:
                            print(f"Error: incorrect message {message} recieved", file=sys.stderr)
                        sock.close()
                        exit(1)
                else:
                    if self.DEBUG:
                        print("Server disconnected", file=sys.stderr)
                    sock.close()
                    exit(1)
    
    def login(self):
        """
        Display and logic for new user account creation and returning user login
        """
        print(f"""{Fore.BLUE}-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+
                                                                                
                                                                                
                        {Fore.RED}__/\__                                                  
                        {Fore.RED}\    /                                               
                      {Fore.BLUE}XX{Fore.RED}/_  _\{Fore.BLUE}XX                                           
                      {Fore.BLUE}XXXX{Fore.RED}\/{Fore.BLUE}XXXX      {Fore.YELLOW}XXXX                                   
                      {Fore.BLUE}XX      XX  {Fore.YELLOW}XXXX    XXXX                                  
                      {Fore.BLUE}XX      {Fore.YELLOW}XXXX            XXXX                              
                      {Fore.BLUE}XX  {Fore.YELLOW}XXXX                    XXXX                          
                      {Fore.YELLOW}XXXX        {Fore.RED}W E L C O M E       {Fore.YELLOW}XXXX                      
                  XXXX                                    XXXX                  
               XXX            {Fore.BLUE}T O   F A B U L O U S           {Fore.YELLOW}XXX               
               XXX                                            XXX               
                  XXXXX         {Fore.RED}C A R D   G A L A        {Fore.YELLOW}XXXXX                  
                      {Fore.BLUE}XX{Fore.YELLOW}XXXX                         XXXX                       
                      {Fore.BLUE}XX    {Fore.YELLOW}XXXX                XXXXX                           
                      {Fore.BLUE}XX      XX{Fore.YELLOW}XXXXX      XXXXX                                
                      {Fore.BLUE}XX      XX     {Fore.YELLOW}XXXXXX                                     
                      {Fore.BLUE}XX      XX                                                
                      XX      XX                                                
                      XX      XX                                                
                      XX      XX                                                
                      XX      XX                                                
{Fore.BLUE}-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+-+H+{Fore.WHITE}""")
        entered_credentials = False
        response = ""
        # for a in art:
        #     print(art[a])
        while not entered_credentials:
            returning_user = input(f"\n{Fore.WHITE}ARE YOU A RETURNING USER {Style.DIM}(y/n){Style.NORMAL}? ")
            if returning_user == "y":
                username = input("\nPLEASE ENTER YOUR USERNAME: ")
                password = input("PLEASE ENTER YOUR PASSWORD: ")
                print(f"\n{Style.DIM}LOGGING IN...\n{Style.NORMAL}")
                response = "exist" + username + "," + password
                entered_credentials = True
            elif returning_user == "n":
                username = input("\nENTER A NEW USERNAME: ")
                password = input("ENTER A NEW PASSWORD: ")
                print(f"\n{Style.DIM}CREATING ACCOUNT...\n{Style.NORMAL}")
                response = "newpl" + username + "," + password
                entered_credentials = True
            else:
                print(f"\n{Fore.RED}INVALID INPUT - PLEASE TRY AGAIN (MUST ENTER {Style.DIM}y {Style.NORMAL}OR {Style.DIM}n{Style.DIM})")
        self.connection.sendall(response.encode('utf-8'))
            
    def choose_game(self, message):
        room_names = []
        # get the list of games from the remainder of the sent string
        waiting_games_str = message
        can_join = False

        if waiting_games_str == "":
            print(f"\n{Style.DIM}THERE ARE NO GAMES WAITING TO START -- CREATE A NEW GAME\n{Style.NORMAL}")
        else:
            can_join = True
            # Client wants to know type of game, room name, num spots left, whos in the game
            # games are separated by '|' symbol, subcategories by commas
            # print("Choose from one of the following games or create a new game")
            waiting_games = waiting_games_str.split("|")
            print(f"{Style.DIM}\nWAITING: {waiting_games}")
            num = 1
            for game in waiting_games:
                if game != "":
                    print("------------------------------------------------")
                    game_info = game.split(":")
                    if self.DEBUG:
                        print(f"GAME: {game}")
                        print(f"GAME INFO: {game_info}", file=sys.stderr)
                    room_names.append(game_info[0])
                    print(f"GAME #{num}")
                    print(f"ROOM NAME: {game_info[0]}")
                    print(f"GAME TYPE: {game_info[1]}")
                    print(f"PLAYERS: {game_info[2]}")
                    print(f"NUMBER OF SPOTS LEFT: {game_info[3]}")
                    print("------------------------------------------------")
                    print(f"{Style.NORMAL}")
                    num += 1

        # Client chooses one of the availible games or chooses to create a new game 
        # from the list GAMES
        # Also sends response to server (if client choose an existing game
        # server needs to know which game it is)
        response = ""
        chosen_game = False
        while not chosen_game:
            create_or_join = input(f"{Fore.WHITE}DO YOU WANT TO CREATE A NEW GAME {Style.DIM}(c){Style.NORMAL}, JOIN AN EXISTING ONE {Style.DIM}(j){Style.NORMAL},\nGET AN UPDATED LIST OF AVAILABLE GAMES {Style.DIM}(u){Style.NORMAL}, OR QUIT THE GAME {Style.DIM}(q){Style.NORMAL}? ")
            if create_or_join == "j":
                if can_join:
                    num_rooms = len(room_names)
                    chosen_game_num = self.select_valid_game_num(num_rooms)
                    response = "egame" + str(room_names[int(chosen_game_num) - 1])
                    chosen_game = True
                else:
                    print(f"{Fore.RED}\nNO GAMES TO JOIN. PLEASE CREATE A NEW GAME.\n{Fore.WHITE}")
                    chosen_game = False
            elif create_or_join == "c":
                print("\nWHICH OF THE FOLLOWING GAMES DO YOU WANT TO PLAY?")
                # game_type = input(f"\nWHICH OF THE FOLLOWING GAMES DO YOU WANT TO PLAY?\n")
                for game in GAMES:
                    print(f"{Style.DIM}- {game}{Style.NORMAL}")
                game_type = input("\n")
                response = "ngame" + game_type
                chosen_game = True
            elif create_or_join == "u":
                response = "updat"
                chosen_game = True
            elif create_or_join == "q":
                response = "quitg"
                chosen_game = True
            else:
                # print(f"\n{Fore.RED}INVALID INPUT. THERE ARE  (c or j){Fore.WHITE}{Style.DIM}(MUST ENTER c OR j){Style.NORMAL}\n{Fore.RESET}")
                print(f"\n{Fore.RED}INVALID INPUT. PLEASE TRY AGAIN.\n{Fore.WHITE}")

        # print(f"{Style.DIM}JOINING {game_type}...{Style.NORMAL}")
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
            value = input("ENTER THE AMOUNT OF MONEY YOU WANT TO START WITH: ")
            if value.isdigit() and float(value) > 0:
                self.connection.sendall(value.encode('utf-8'))
                entered_money = True
            else:
                print(f"\n{Fore.RED}YOU DID NOT ENTER A VALID AMOUNT OF MONEY...\nTRY AGAIN, OR COME "
                + f"BACK WHEN YOU ACTUALLY HAVE MONEY!{Fore.WHITE}\n")
    
    def place_bet(self, money):
        print(f"\nYOU HAVE ${money}")
        placed_bet = False
        while not placed_bet:
            bet = input("ENTER YOUR BET: ")
            if bet.isdigit() and float(bet) > 0 and float(bet) <= float(money):
                # print("bet: ", bet)
                self.connection.sendall(bet.encode('utf-8'))
                placed_bet = True                
            else:
                print(f"\n{Fore.RED}YOU DID NOT ENTER A VALID BET.\nYOUR BET MUST BE GREATER THAN $0 AND WITHIN YOUR AVAILABLE AMOUNT OF MONEY!\n{Fore.WHITE}")

    #####################

    ### PressTheButton functions ###
       


