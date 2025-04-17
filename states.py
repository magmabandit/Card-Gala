class States():
    ### Server States ###
    ERROR = {
        "server commands": {
            "error": "error"
        },
        "client responses": {}
    }

    #TODO: add printing
    LOGIN = {
        "server commands": {
            "login": "login",
            "invalid login": "invlo",
            "username used": "uused",
            "set username": "suser",
        },
        "client responses": {
            "login": ["newpl", "exist"]
        }
    }

    CHOOSE_GAME = {
        "server commands": {
            "choose game": "cgame",
            "max_game_inst": "maxgm",
            "room_filled": "froom",
            "waiting for players": "wplay",
            "printing": "print",
        },
        "client responses": {
            "choose game": ["egame", "ngame", "updat", "quitg"]
        }
    }

    END = {
        "server commands": {
            "end": "endgm"
        },
        "client responses": {}
    }

    ### Game States ###

    BLACKJACK = {
        "server commands" : {
            "enter money": "money",
            "place bet": "plbet",
            "intial hand": "ihand",
            "printing": "print",
            "Player-choice": "SxorH",
            "Player-choice2": "YxorN",
            "rank": "crank",
            "suit": "csuit",
            "suit_change": "suitch",
        },
        "client responses": {}
    }

    PRESSTHEBUTTON = {
        "server commands" : {
            "printing": "print",
            "countdown": "cdown",
            "listen-keypress": "press",
        },
        "client responses": {}
    }
