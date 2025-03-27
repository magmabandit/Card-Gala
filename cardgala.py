from client import Client
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', '--c') # Requires str
    args = parser.parse_args()

    client = None

    if args.client == "" or None:
        raise Exception("--c flag requires a hostname argument")
    else:
        client = Client(args.client)
    
    client.connect_to_server()
    

if __name__ == '__main__':
    main()

