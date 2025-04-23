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
    "AHearts": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "2Hearts": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "3Hearts": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "4Hearts": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "5Hearts": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "6Hearts": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "7Hearts": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "8Hearts": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "9Hearts": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "10Hearts": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "JHearts": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "QHearts": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "KHearts": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "ADiamonds": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "2Diamonds": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "3Diamonds": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "4Diamonds": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "5Diamonds": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "6Diamonds": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "7Diamonds": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "8Diamonds": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "9Diamonds": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "10Diamonds": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "JDiamonds": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "QDiamonds": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
    "KDiamonds": f"""{Fore.RED}XXXXXXXXXXXXXXXXXXX
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
XXXXXXXXXXXXXXXXXXX{Fore.WHITE}""",
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