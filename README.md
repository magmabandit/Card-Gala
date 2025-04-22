# Card-Gala
Concurrency Project for CS21

## To Run
**Running the server**: python3 cardgala_server.py
**Running a client** python3 cardgala.py
> running a client in debug mode: python3 cardgala.py --h server-ip -d
> cardgala.py by default attempts to connect to a server running on
  localhost -- if you wish to connect to a server at a specific ip
  address us the --h tag

## Required Libraries
abc
argparse
colorama
logging
multiprocessing
random
select
socket
string
sys
threading
time
tqdm