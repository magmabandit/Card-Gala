import argparse
import socket
import select
import sys

PORT = 9998

class Client():

    def __init__(self, hostname):
        self.hostname = hostname
        self.connection = None

    def connect_to_server(self):
        conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_sock.connect((self.hostname, PORT))

        self.connection = conn_sock

    def run_client(hostname):
        while True:
            input_list = [conn_sock, sys.stdin]
            try:
                (ready_read, _, _) = select.select(input_list, [], [])
            except ValueError:
                break

            for sock in ready_read:
                if sock is conn_sock:
                    data = sock.recv(1024)
                    if data:
                        sys.stdout.write(data.decode('utf-8'))
                        sys.stdout.flush()
                    else:
                        # client_sockets.remove(sock)
                        sock.close()
                elif sock is sys.stdin:
                    input = sys.stdin.readline().encode('utf-8')
                    if not input:
                        conn_sock.close()
                        return
                    conn_sock.sendall(input)


