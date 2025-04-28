# Card-Gala

Abdullahi Abdi, Kevin Arellano Flores, Ethan Goldman, Alex Lee

Final Project, CS-21: Concurrent Programming

Tufts University, Spring 2025

## To Run
**Running the Server**: `python3 cardgala_server.py`

**Running a Client** `python3 cardgala.py`

**Note:**
> running a client in debug mode: `python3 cardgala.py --h server-ip -d`

> by default, `cardgala.py` attempts to connect to a server running on
  localhost -- if you wish to connect to a server at a specific ip
  address include the `--h` tag followed by the ip address.

## Required Libraries: Install Before Running
- abc
- argparse
- colorama
- logging
- multiprocessing
- random
- select
- socket
- string
- sys
- threading
- time
- tqdm

## Summary of Files:
- `ascii_art.py`: dedicated file for storage of ASCII art used throughout the program.
- `BJCard.py`: defines the Card class used by the Blackjack and CrazyEight games.
- `BJDeaer.py`: defines the Dealer class used by the Blackjack and CrazyEight games.
- `BJDeck.py`: defines the Deck class used by the Blackjack and CrazyEight games.
- `BJGame.py`: defines the mechanics of the single-player Blackjack game.
- `BJHand.py`: defines the Hand class used by the Blackjack games.
- `BJPlayer.py`: defines the Player class used by the Blackjack games.
- `BJTwoPLayer.py`: defines the mechanics of the two-player Blackjack game.
- `cardgala_server.py`: creates and runs a Cardgala server instance.
- `cardgala.py`: creates and runs a Cardgala client instance.
- `client.py`: defines the client-side mechanics for logging-into Cardgala, joining games, and in-game commands.
- `CrazyEight.py`: defines the mechanics of the two-player CrazyEight game.
- `CrazyEightHand.py`: defines the mechanics for adding, removing, accessing, and drawing cards from a deck according to the logic of a CrazyEight game.
- `CrazyEightPLayer.py`: defines the mechanics for the turns of players throughout a CrazyEight game.
- `game.py`: declares and defines abstract methods for Cardgala games.
- `locked_dict.py`: defines a thread-safe dictionary.
- `locked_list.py`: defines a thread-safe list.
- `player.py`: stores and provides access to client-related data
- `PTBGame.py`: defines the mechanics of the Press the Button game.
- `README.md`: this file.
- `server.py`: defines the mechanics for the cardgala server.
- `states.py`: defines the various states communicated between the server and client.
