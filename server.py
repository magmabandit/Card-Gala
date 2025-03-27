import argparse
import socket
import select
import sys

from player import Player

PORT = 9998
MAX_GAME_INSTANCES = 4 #TODO: what should this value be?

class Server:

    def __init__(self):
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind(('', PORT))
        self.listen_socket.listen()

        self.login_cache = {}
        self.idle_players = []

    def run_server(self):
        while True:
            read_list = [self.listen_socket]
            (ready_read, _, _) = select.select(read_list, [], [])

            # TODO: Do this with threading?
            for sock in ready_read:

                # If a new client attempts to connect
                if sock is self.listen_socket:
                    # 1) Accept the connection and create the player instance
                    new_conn, addr = sock.accept()
                    new_player = Player(connection=new_conn)
                    self.idle_players.append(new_player)

                    logged_in = False
                    while not logged_in:
                        # 2) Initiate the login sequence and get 
                        #    returning/exisiting user, username, password from client
                        #    #TODO: usernames & passwords must currently be 5 chars - is that ok?
                        response = self.call(new_player, "login") # TODO - make dict of states/messages to send
                        login_type = response[0:5]
                        username = response[5:10]
                        password = response[10:15]

                        # 3) Log player in
                        if login_type == "newpl":
                            self.login_cache[username] = password
                            new_player.set_username(username)
                            logged_in = True
                        elif login_type == "exist":
                            if password == self.login_cache[username]:
                                new_player.set_username(username)
                                logged_in = True
                            else:
                                self.cast(new_player, "invalid login")
                        else: # If we don't get a valid response from the client 
                              # raise an error and terminate the connection

                            #TODO: for debugging - remove this
                            print(login_type)
                            logged_in = True

                            self.cast(new_player, "error")
                            self.idle_players.remove(new_player)
                            new_player.get_connection().close()

                    # TODO: Enter Game State???
                    return


                # elif sock is sys.stdin:
                #     input = sys.stdin.readline().encode('utf-8')
                #     if not input:
                #         listen_socket.close()
                #         for c in client_sockets :
                #             c.close()
                #         return
                #     for c in client_sockets:
                #         c.sendall(input)
                # else:
                #     data = sock.recv(1024)
                #     if data != b'':
                #         sys.stdout.write(data.decode('utf-8'))
                #         sys.stdout.flush()
                #     else:
                #         client_sockets.remove(sock)
                #         sock.close()
    
    # Expects reponse - blocking until response is recieved
    # If a player has disconnected the player will be removed
    #   from idle_players and the connection is closed
    def call(self, player: Player, message: str):
        connection = player.get_connection()
        connection.sendall(message.encode('utf-8'))

        recieved_response = False
        response = ""
        while not recieved_response:
            (ready_read, _, _) = select.select([connection], [], [])
            if len(ready_read) > 0:
                data = connection.recv(1024)
                if data != b'': # Recieved response from client
                    response = data.decode('utf-8')
                    recieved_response = True
                else: # Client has disconnected
                    self.idle_players.remove(player)
                    connection.close()
        return response

    # Does not expect response
    # Non-blocking - just sends message
    def cast(self, player: Player, message: str):
        connection = player.get_connection()
        connection.sendall(message.encode('utf-8'))