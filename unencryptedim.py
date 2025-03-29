import argparse
import socket
import select
import sys

# Example from CS114
# Written by Dan Votipka

# HOST = '127.0.0.1'
PORT = 9998

def run_server():
    # stores new connections to the server
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(('', PORT))
    listen_socket.listen()
    client_sockets = []

    while True:
        read_list = [listen_socket] + client_sockets + [sys.stdin]
        (ready_read, _, _) = select.select(read_list, [], [])

        for sock in ready_read:
            if sock is listen_socket:
                new_conn, addr = sock.accept()
                client_sockets.append(new_conn)
            elif sock is sys.stdin:
                input = sys.stdin.readline().encode('utf-8')
                if not input:
                    listen_socket.close()
                    for c in client_sockets :
                        c.close()
                    return
                for c in client_sockets:
                    c.sendall(input)
            else:
                data = sock.recv(1024)
                if data != b'':
                    sys.stdout.write(data.decode('utf-8'))
                    sys.stdout.flush()
                else:
                    client_sockets.remove(sock)
                    sock.close()

def run_client(hostname):
    conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_sock.connect((hostname, PORT))

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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', '--s', action='store_true')
    parser.add_argument('--client', '--c') # Requires str

    args = parser.parse_args()

    if args.server:
        run_server()
    elif args.client:
        if args.client == "":
            raise Exception("--c flag requires a hostname argument")
        else:
            run_client(args.client)


if __name__ == '__main__':
    main()
