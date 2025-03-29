import socket
import select
import sys

PORT = 9998

class Client():

    def __init__(self, hostname):
        self.hostname = hostname
        self.connection = None
        self.state = {}
        self.username = ""

        self.games = ["game"] #TODO: list of names of possible games

        self.ERROR = {"error": "error"}

        self.LOGIN = {
            "message": "login",
            "invalid login": "invlo",
            "username used": "uused",
            "set username": "suser",
            "responses": {"enter_user_pass": self.login},
        }

        self.CHOOSE_GAME = {
            "message": "cgame"
        }

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
                        state = self.LOGIN
                        state["responses"]["enter_user_pass"]()

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

                    elif message == self.ERROR["error"]:
                        print("server recieved bad message, closing connection")
                        sock.close()
                        exit(1)

                    elif message == self.CHOOSE_GAME["message"]:
                        print("Choose game!!")
                        state = self.CHOOSE_GAME

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
                


