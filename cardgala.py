import argparse

from client import Client

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', '--h')
    args = parser.parse_args()

    client = None

    if args.hostname == "" or None:
        raise Exception("--h flag requires a hostname argument")
    else:
        client = Client(args.hostname)
    
    client.connect_to_server()
    client.run_client()
    

if __name__ == '__main__':
    main()

