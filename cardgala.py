import argparse

from client import Client

def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--hostname', '--h')
    # parser.add_argument("-d", required=False, default=False, action='store_true')
    # args = parser.parse_args()

    # client = None

    # # if args.hostname == "" or None:
    #     raise Exception("--h flag requires a hostname argument")
    # else:
        # debug = args.d
    client = Client("127.0.0.1", False)
    
    client.connect_to_server()
    client.run_client()
    

if __name__ == '__main__':
    main()

