#
# cardgala.py
#
# Run an instance of the cardgala client

import argparse

from client import Client

def main():
    """ Parses args from command line and runs client instance """
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', '--h', default="127.0.0.1")
    parser.add_argument(
        "-d", 
        required=False, 
        default=False, 
        action='store_true'
    )
    args = parser.parse_args()

    client = Client(args.hostname, args.d)
    
    client.connect_to_server()
    client.run_client()
    

if __name__ == '__main__':
    main()

