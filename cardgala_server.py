#
# cardgala_server.py
#
# Runs a cardgala server

from server import Server

def main():
    """ Run the cardgala server """
    s = Server()
    s.run_server()

if __name__ == '__main__':
    main()