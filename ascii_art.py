from colorama import Fore, Back, Style

art = {
    "ASpades": """XXXXXXXXXXXXXXXXXXX
X                 X
X A               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X   X         X   X
X    X   X   X    X
X     XXX XXX     X
X       X X       X
X      XXXXX      X
X               A X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "2Spades": """XXXXXXXXXXXXXXXXXXX
X                 X
X 2               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X   X         X   X
X    X   X   X    X
X     XXX XXX     X
X       X X       X
X      XXXXX      X
X               2 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "3Spades": """XXXXXXXXXXXXXXXXXXX
X                 X
X 3               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X   X         X   X
X    X   X   X    X
X     XXX XXX     X
X       X X       X
X      XXXXX      X
X               3 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "4Spades": """XXXXXXXXXXXXXXXXXXX
X                 X
X 4               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X   X         X   X
X    X   X   X    X
X     XXX XXX     X
X       X X       X
X      XXXXX      X
X               4 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "5Spades": """XXXXXXXXXXXXXXXXXXX
X                 X
X 5               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X   X         X   X
X    X   X   X    X
X     XXX XXX     X
X       X X       X
X      XXXXX      X
X               5 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "6Spades": """XXXXXXXXXXXXXXXXXXX
X                 X
X 6               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X   X         X   X
X    X   X   X    X
X     XXX XXX     X
X       X X       X
X      XXXXX      X
X               6 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "7Spades": """XXXXXXXXXXXXXXXXXXX
X                 X
X 7               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X   X         X   X
X    X   X   X    X
X     XXX XXX     X
X       X X       X
X      XXXXX      X
X               7 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "8Spades": """XXXXXXXXXXXXXXXXXXX
X                 X
X 8               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X   X         X   X
X    X   X   X    X
X     XXX XXX     X
X       X X       X
X      XXXXX      X
X               8 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "9Spades": """XXXXXXXXXXXXXXXXXXX
X                 X
X 9               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X   X         X   X
X    X   X   X    X
X     XXX XXX     X
X       X X       X
X      XXXXX      X
X               9 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "10Spades": """XXXXXXXXXXXXXXXXXXX
X                 X
X 10              X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X   X         X   X
X    X   X   X    X
X     XXX XXX     X
X       X X       X
X      XXXXX      X
X              10 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "JSpades": """XXXXXXXXXXXXXXXXXXX
X                 X
X J               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X   X         X   X
X    X   X   X    X
X     XXX XXX     X
X       X X       X
X      XXXXX      X
X               J X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "QSpades": """XXXXXXXXXXXXXXXXXXX
X                 X
X Q               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X   X         X   X
X    X   X   X    X
X     XXX XXX     X
X       X X       X
X      XXXXX      X
X               Q X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "KSpades": """XXXXXXXXXXXXXXXXXXX
X                 X
X K               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X   X         X   X
X    X   X   X    X
X     XXX XXX     X
X       X X       X
X      XXXXX      X
X               K X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "AHearts": """XXXXXXXXXXXXXXXXXXX
X                 X
X A               X
X                 X
X     XXX XXX     X
X    X   X   X    X
X   X         X   X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X                 X
X               A X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "2Hearts": """XXXXXXXXXXXXXXXXXXX
X                 X
X 2               X
X                 X
X     XXX XXX     X
X    X   X   X    X
X   X         X   X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X                 X
X               2 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "3Hearts": """XXXXXXXXXXXXXXXXXXX
X                 X
X 3               X
X                 X
X     XXX XXX     X
X    X   X   X    X
X   X         X   X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X                 X
X               3 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "4Hearts": """XXXXXXXXXXXXXXXXXXX
X                 X
X 4               X
X                 X
X     XXX XXX     X
X    X   X   X    X
X   X         X   X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X                 X
X               4 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "5Hearts": """XXXXXXXXXXXXXXXXXXX
X                 X
X 5               X
X                 X
X     XXX XXX     X
X    X   X   X    X
X   X         X   X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X                 X
X               5 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "6Hearts": """XXXXXXXXXXXXXXXXXXX
X                 X
X 6               X
X                 X
X     XXX XXX     X
X    X   X   X    X
X   X         X   X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X                 X
X               6 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "7Hearts": """XXXXXXXXXXXXXXXXXXX
X                 X
X 7               X
X                 X
X     XXX XXX     X
X    X   X   X    X
X   X         X   X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X                 X
X               7 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "8Hearts": """XXXXXXXXXXXXXXXXXXX
X                 X
X 8               X
X                 X
X     XXX XXX     X
X    X   X   X    X
X   X         X   X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X                 X
X               8 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "9Hearts": """XXXXXXXXXXXXXXXXXXX
X                 X
X 9               X
X                 X
X     XXX XXX     X
X    X   X   X    X
X   X         X   X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X                 X
X               9 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "10Hearts": """XXXXXXXXXXXXXXXXXXX
X                 X
X 10              X
X                 X
X     XXX XXX     X
X    X   X   X    X
X   X         X   X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X                 X
X              10 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "JHearts": """XXXXXXXXXXXXXXXXXXX
X                 X
X J               X
X                 X
X     XXX XXX     X
X    X   X   X    X
X   X         X   X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X                 X
X               J X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "QHearts": """XXXXXXXXXXXXXXXXXXX
X                 X
X Q               X
X                 X
X     XXX XXX     X
X    X   X   X    X
X   X         X   X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X                 X
X               Q X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "KHearts": """XXXXXXXXXXXXXXXXXXX
X                 X
X K               X
X                 X
X     XXX XXX     X
X    X   X   X    X
X   X         X   X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X                 X
X               K X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "ADiamonds": """XXXXXXXXXXXXXXXXXXX
X                 X
X A               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X               A X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "2Diamonds": """XXXXXXXXXXXXXXXXXXX
X                 X
X 2               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X               2 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "3Diamonds": """XXXXXXXXXXXXXXXXXXX
X                 X
X 3               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X               3 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "4Diamonds": """XXXXXXXXXXXXXXXXXXX
X                 X
X 4               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X               4 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "5Diamonds": """XXXXXXXXXXXXXXXXXXX
X                 X
X 5               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X               5 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "6Diamonds": """XXXXXXXXXXXXXXXXXXX
X                 X
X 6               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X               6 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "7Diamonds": """XXXXXXXXXXXXXXXXXXX
X                 X
X 7               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X               7 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "8Diamonds": """XXXXXXXXXXXXXXXXXXX
X                 X
X 8               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X               8 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "9Diamonds": """XXXXXXXXXXXXXXXXXXX
X                 X
X 9               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X               9 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "10Diamonds": """XXXXXXXXXXXXXXXXXXX
X                 X
X 10              X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X              10 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "JDiamonds": """XXXXXXXXXXXXXXXXXXX
X                 X
X J               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X               J X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "QDiamonds": """XXXXXXXXXXXXXXXXXXX
X                 X
X Q               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X               Q X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "KDiamonds": """XXXXXXXXXXXXXXXXXXX
X                 X
X K               X
X        X        X
X       X X       X
X      X   X      X
X     X     X     X
X    X       X    X
X   X         X   X
X    X       X    X
X     X     X     X
X      X   X      X
X       X X       X
X        X        X
X               K X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "AClubs": """XXXXXXXXXXXXXXXXXXX
X                 X
X A               X
X                 X
X      XXXXX      X
X     X     X     X
X     X     X     X
X    XX     XX    X
X   X         X   X
X   X         X   X
X   X   XXX   X   X
X    XXX   XXX    X
X       X X       X
X      XXXXX      X
X               A X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "2Clubs": """XXXXXXXXXXXXXXXXXXX
X                 X
X 2               X
X                 X
X      XXXXX      X
X     X     X     X
X     X     X     X
X    XX     XX    X
X   X         X   X
X   X         X   X
X   X   XXX   X   X
X    XXX   XXX    X
X       X X       X
X      XXXXX      X
X               2 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "3Clubs": """XXXXXXXXXXXXXXXXXXX
X                 X
X 3               X
X                 X
X      XXXXX      X
X     X     X     X
X     X     X     X
X    XX     XX    X
X   X         X   X
X   X         X   X
X   X   XXX   X   X
X    XXX   XXX    X
X       X X       X
X      XXXXX      X
X               3 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "4Clubs": """XXXXXXXXXXXXXXXXXXX
X                 X
X 4               X
X                 X
X      XXXXX      X
X     X     X     X
X     X     X     X
X    XX     XX    X
X   X         X   X
X   X         X   X
X   X   XXX   X   X
X    XXX   XXX    X
X       X X       X
X      XXXXX      X
X               4 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "5Clubs": """XXXXXXXXXXXXXXXXXXX
X                 X
X 5               X
X                 X
X      XXXXX      X
X     X     X     X
X     X     X     X
X    XX     XX    X
X   X         X   X
X   X         X   X
X   X   XXX   X   X
X    XXX   XXX    X
X       X X       X
X      XXXXX      X
X               5 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "6Clubs": """XXXXXXXXXXXXXXXXXXX
X                 X
X 6               X
X                 X
X      XXXXX      X
X     X     X     X
X     X     X     X
X    XX     XX    X
X   X         X   X
X   X         X   X
X   X   XXX   X   X
X    XXX   XXX    X
X       X X       X
X      XXXXX      X
X               6 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "7Clubs": """XXXXXXXXXXXXXXXXXXX
X                 X
X 7               X
X                 X
X      XXXXX      X
X     X     X     X
X     X     X     X
X    XX     XX    X
X   X         X   X
X   X         X   X
X   X   XXX   X   X
X    XXX   XXX    X
X       X X       X
X      XXXXX      X
X               7 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "8Clubs": """XXXXXXXXXXXXXXXXXXX
X                 X
X 8               X
X                 X
X      XXXXX      X
X     X     X     X
X     X     X     X
X    XX     XX    X
X   X         X   X
X   X         X   X
X   X   XXX   X   X
X    XXX   XXX    X
X       X X       X
X      XXXXX      X
X               8 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "9Clubs": """XXXXXXXXXXXXXXXXXXX
X                 X
X 9               X
X                 X
X      XXXXX      X
X     X     X     X
X     X     X     X
X    XX     XX    X
X   X         X   X
X   X         X   X
X   X   XXX   X   X
X    XXX   XXX    X
X       X X       X
X      XXXXX      X
X               9 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "10Clubs": """XXXXXXXXXXXXXXXXXXX
X                 X
X 10              X
X                 X
X      XXXXX      X
X     X     X     X
X     X     X     X
X    XX     XX    X
X   X         X   X
X   X         X   X
X   X   XXX   X   X
X    XXX   XXX    X
X       X X       X
X      XXXXX      X
X              10 X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "JClubs": """XXXXXXXXXXXXXXXXXXX
X                 X
X J               X
X                 X
X      XXXXX      X
X     X     X     X
X     X     X     X
X    XX     XX    X
X   X         X   X
X   X         X   X
X   X   XXX   X   X
X    XXX   XXX    X
X       X X       X
X      XXXXX      X
X               J X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "QClubs": """XXXXXXXXXXXXXXXXXXX
X                 X
X Q               X
X                 X
X      XXXXX      X
X     X     X     X
X     X     X     X
X    XX     XX    X
X   X         X   X
X   X         X   X
X   X   XXX   X   X
X    XXX   XXX    X
X       X X       X
X      XXXXX      X
X               Q X
X                 X
XXXXXXXXXXXXXXXXXXX""",
    "KClubs": """XXXXXXXXXXXXXXXXXXX
X                 X
X K               X
X                 X
X      XXXXX      X
X     X     X     X
X     X     X     X
X    XX     XX    X
X   X         X   X
X   X         X   X
X   X   XXX   X   X
X    XXX   XXX    X
X       X X       X
X      XXXXX      X
X               K X
X                 X
XXXXXXXXXXXXXXXXXXX"""
    }