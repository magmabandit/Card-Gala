import socket
import select
import sys

PORT = 9998

class Client():

    def __init__(self, hostname):
        self.hostname = hostname
        self.connection = None
        self.state = {}

    def connect_to_server(self):
        conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_sock.connect((self.hostname, PORT))

        self.connection = conn_sock

    def run_client(self, hostname):
        while True:
            input_list = [self.connection]
            try:
                (ready_read, _, _) = select.select(input_list, [], [])
            except ValueError:
                break

            for sock in ready_read:
                message = sock.recv(1024).decode('utf-8')
                if message:
                    match message:
                        case self.LOGIN["message"]:
                            state = self.LOGIN
                            state["enter_user_pass"]()
                        case self.LOGIN["invalid login"]:
                            print("server recieved bad message, closing connection")
                            sock.close()
                            exit(1)
                        case self.LOGIN["error"]:
                            print("incorrect username or password, try again")
                        case self.CHOOSE_GAME["message"]:
                            state = self.CHOOSE_GAME
                            print("Choose game!!")
                            continue
                        case _:
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
            elif returning_user == "n":
                username = self.get_valid_username()
                password = self.get_valid_password()
                response = "newpl" + username + password
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

    LOGIN = {
        "message": "login",
        "invalid login": "invlo",
        "error": "error",
        "responses": {"enter_user_pass": login},
    }

    CHOOSE_GAME = {
        "message": "cgame"
    }
                


