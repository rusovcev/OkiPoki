from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import create_engine, Column, Integer, String, Boolean
from OkiPoki import app

db = SQLAlchemy(app)


#class Player():
#    __tablename__ = "players"
#    id = Column(Integer, primary_key=True)
#    name = Column(String(20), unique=True)
#    logged = Column(Boolean)

#    def __init__(self, name=None, logged=True):
#        self.name = name

#    def __repr__(self):
#        return '<Player %r>' % (self.name)

class Player(db.Model):
    """description of class"""
    name = db.Column(db.String(80), primary_key=True, unique=True)
    password = db.Column(db.String(80))
    #logged = db.Column(db.Boolean)
    wins = db.Column(db.Integer)
    loses = db.Column(db.Integer)
    draws = db.Column(db.Integer)

    def __init__(self, name, password):
        self.name = name
        self.password = password
        #self.logged = True
        self.wins = 0
        self.loses = 0
        self.draws = 0

    def __repr__(self):
        return '<User %r>' % self.name

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.name)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    playerX = db.Column(db.String(80))
    playerO = db.Column(db.String(80))
    player2move = db.Column(db.String(1))
    f1 = db.Column(db.String(1))
    f2 = db.Column(db.String(1))
    f3 = db.Column(db.String(1))
    f4 = db.Column(db.String(1))
    f5 = db.Column(db.String(1))
    f6 = db.Column(db.String(1))
    f7 = db.Column(db.String(1))
    f8 = db.Column(db.String(1))
    f9 = db.Column(db.String(1))

    def __init__(self, playerX, playerO):
        self.playerX = playerX
        self.playerO = playerO
        self.player2move = 'X'
        self.f1 = None
        self.f2 = None
        self.f3 = None
        self.f4 = None
        self.f5 = None
        self.f6 = None
        self.f7 = None
        self.f8 = None
        self.f9 = None
    
    def gameUpdate(self, field, player):
        if field == "f1" and self.f1 is None:
            self.f1 = player
            return True
        elif field == "f2" and self.f2 is None:
            self.f2 = player
            return True
        elif field == "f3" and self.f3 is None:
            self.f3 = player
            return True
        elif field == "f4" and self.f4 is None:
            self.f4 = player
            return True
        elif field == "f5" and self.f5 is None:
            self.f5 = player
            return True
        elif field == "f6" and self.f6 is None:
            self.f6 = player
            return True
        elif field == "f7" and self.f7 is None:
            self.f7 = player
            return True
        elif field == "f8" and self.f8 is None:
            self.f8 = player
            return True
        elif field == "f9" and self.f9 is None:
            self.f9 = player
            return True
        else:
            return False

    def switchPlayer(self):
        if self.player2move == "X":
            self.player2move = "O"
            return True
        elif self.player2move == "O":
            self.player2move = "X"
            return True
        else:
            return False
    
    def gameWon(self):
        if  "X" == self.f1 == self.f2 == self.f3 or \
            "X" == self.f4 == self.f5 == self.f6 or \
            "X" == self.f7 == self.f8 == self.f9 or \
            "X" == self.f1 == self.f4 == self.f7 or \
            "X" == self.f2 == self.f5 == self.f8 or \
            "X" == self.f3 == self.f6 == self.f9 or \
            "X" == self.f1 == self.f5 == self.f9 or \
            "X" == self.f3 == self.f5 == self.f7:
            return "X"
        elif "O" == self.f1 == self.f2 == self.f3 or \
            "O" == self.f4 == self.f5 == self.f6 or \
            "O" == self.f7 == self.f8 == self.f9 or \
            "O" == self.f1 == self.f4 == self.f7 or \
            "O" == self.f2 == self.f5 == self.f8 or \
            "O" == self.f3 == self.f6 == self.f9 or \
            "O" == self.f1 == self.f5 == self.f9 or \
            "O" == self.f3 == self.f5 == self.f7:
            return "O"
        else:
            return False

    def gameOver(self):
        if self.f1 is not None and self.f2 is not None and self.f3 is not None and self.f4 is not None and self.f5 is not None and self.f6 is not None and self.f7 is not None and self.f8 is not None and self.f9 is not None:
            return True
        else:
            return False

    def AI_finish(self, AI):
        if AI == self.f1 == self.f2 and self.f3 is None: # 1st row
            self.f3 = AI
            return True
        elif AI == self.f1 == self.f3 and self.f2 is None: # 1st row
            self.f2 = AI
            return True
        elif AI == self.f2 == self.f3 and self.f1 is None: # 1st row
            self.f1 = AI
            return True
        elif AI == self.f4 == self.f5 and self.f6 is None: # 2nd row
            self.f6 = AI
            return True
        elif AI == self.f4 == self.f6 and self.f5 is None: # 2nd row
            self.f5 = AI
            return True
        elif AI == self.f5 == self.f6 and self.f4 is None: # 2nd row
            self.f4 = AI
            return True
        elif AI == self.f7 == self.f8 and self.f9 is None: # 3rd row
            self.f9 = AI
            return True
        elif AI == self.f7 == self.f9 and self.f8 is None: # 3rd row
            self.f8 = AI
            return True
        elif AI == self.f8 == self.f9 and self.f7 is None: # 3rd row
            self.f7 = AI
            return True
        elif AI == self.f1 == self.f4 and self.f7 is None: # 1st col
            self.f7 = AI
            return True
        elif AI == self.f1 == self.f7 and self.f4 is None: # 1st col
            self.f4 = AI
            return True
        elif AI == self.f4 == self.f7 and self.f1 is None: # 1st col
            self.f1 = AI
            return True
        elif AI == self.f2 == self.f5 and self.f8 is None: # 2nd col
            self.f8 = AI
            return True
        elif AI == self.f2 == self.f8 and self.f5 is None: # 2nd col
            self.f5 = AI
            return True
        elif AI == self.f5 == self.f8 and self.f2 is None: # 2nd col
            self.f2 = AI
            return True
        elif AI == self.f3 == self.f6 and self.f9 is None: # 3rd col
            self.f9 = AI
            return True
        elif AI == self.f3 == self.f9 and self.f6 is None: # 3rd col
            self.f6 = AI
            return True
        elif AI == self.f6 == self.f9 and self.f3 is None: # 3rd col
            self.f3 = AI
            return True
        elif AI == self.f1 == self.f5 and self.f9 is None: # 1st diag
            self.f9 = AI
            return True
        elif AI == self.f1 == self.f9 and self.f5 is None: # 1st diag
            self.f5 = AI
            return True
        elif AI == self.f5 == self.f9 and self.f1 is None: # 1st diag
            self.f1 = AI
            return True
        elif AI == self.f3 == self.f5 and self.f7 is None: # 2nd diag
            self.f7 = AI
            return True
        elif AI == self.f3 == self.f7 and self.f5 is None: # 2nd diag
            self.f5 = AI
            return True
        elif AI == self.f5 == self.f7 and self.f3 is None: # 2nd diag
            self.f3 = AI
            return True
        else:
            return False

    def AI_deffensive(self, AI, opponent):
        if opponent == self.f1 == self.f2 and self.f3 is None: # 1st row
            self.f3 = AI
            return True
        elif opponent == self.f1 == self.f3 and self.f2 is None: # 1st row
            self.f2 = AI
            return True
        elif opponent == self.f2 == self.f3 and self.f1 is None: # 1st row
            self.f1 = AI
            return True
        elif opponent == self.f4 == self.f5 and self.f6 is None: # 2nd row
            self.f6 = AI
            return True
        elif opponent == self.f4 == self.f6 and self.f5 is None: # 2nd row
            self.f5 = AI
            return True
        elif opponent == self.f5 == self.f6 and self.f4 is None: # 2nd row
            self.f4 = AI
            return True
        elif opponent == self.f7 == self.f8 and self.f9 is None: # 3rd row
            self.f9 = AI
            return True
        elif opponent == self.f7 == self.f9 and self.f8 is None: # 3rd row
            self.f8 = AI
            return True
        elif opponent == self.f8 == self.f9 and self.f7 is None: # 3rd row
            self.f7 = AI
            return True
        elif opponent == self.f1 == self.f4 and self.f7 is None: # 1st col
            self.f7 = AI
            return True
        elif opponent == self.f1 == self.f7 and self.f4 is None: # 1st col
            self.f4 = AI
            return True
        elif opponent == self.f4 == self.f7 and self.f1 is None: # 1st col
            self.f1 = AI
            return True
        elif opponent == self.f2 == self.f5 and self.f8 is None: # 2nd col
            self.f8 = AI
            return True
        elif opponent == self.f2 == self.f8 and self.f5 is None: # 2nd col
            self.f5 = AI
            return True
        elif opponent == self.f5 == self.f8 and self.f2 is None: # 2nd col
            self.f2 = AI
            return True
        elif opponent == self.f3 == self.f6 and self.f9 is None: # 3rd col
            self.f9 = AI
            return True
        elif opponent == self.f3 == self.f9 and self.f6 is None: # 3rd col
            self.f6 = AI
            return True
        elif opponent == self.f6 == self.f9 and self.f3 is None: # 3rd col
            self.f3 = AI
            return True
        elif opponent == self.f1 == self.f5 and self.f9 is None: # 1st diag
            self.f9 = AI
            return True
        elif opponent == self.f1 == self.f9 and self.f5 is None: # 1st diag
            self.f5 = AI
            return True
        elif opponent == self.f5 == self.f9 and self.f1 is None: # 1st diag
            self.f1 = AI
            return True
        elif opponent == self.f3 == self.f5 and self.f7 is None: # 2nd diag
            self.f7 = AI
            return True
        elif opponent == self.f3 == self.f7 and self.f5 is None: # 2nd diag
            self.f5 = AI
            return True
        elif opponent == self.f5 == self.f7 and self.f3 is None: # 2nd diag
            self.f3 = AI
            return True
        else:
            return False

    def AI_offensive(self, AI):
        if self.f5 is None and (self.f1 == AI or self.f2 == AI or self.f3 == AI or self.f4 == AI or self.f6 == AI or self.f7 or self.f8 == AI or self.f9 == AI):
            self.f5 = AI
            return True
        elif self.f1 is None and self.f5 == AI and self.f9 is None:
            self.f1 = AI
            return True
        elif self.f1 is None and (self.f2 == AI or self.f3 == AI or self.f4 == AI or self.f7 == AI or self.f5 == AI or self.f9 == AI):
            self.f1 = AI
            return True
        elif self.f3 is None and (self.f1 == AI or self.f2 == AI or self.f6 == AI or self.f9 == AI or self.f5 == AI or self.f7 == AI):
            self.f3 = AI
            return True
        elif self.f7 is None and (self.f1 == AI or self.f4 == AI or self.f8 == AI or self.f9 == AI or self.f5 == AI or self.f3 == AI):
            self.f7 = AI
            return True
        elif self.f9 is None and (self.f3 == AI or self.f6 == AI or self.f7 == AI or self.f8 == AI or self.f5 == AI or self.f1 == AI):
            self.f9 = AI
            return True
        elif self.f2 is None and (self.f1 == AI or self.f3 == AI or self.f5 == AI or self.f8 == AI):
            self.f2 = AI
            return True
        elif self.f4 is None and (self.f1 == AI or self.f7 == AI or self.f5 == AI or self.f6 == AI):
            self.f4 = AI
            return True
        elif self.f6 is None and (self.f3 == AI or self.f9 == AI or self.f5 == AI or self.f4 == AI):
            self.f6 = AI
            return True
        elif self.f8 is None and (self.f7 == AI or self.f9 == AI or self.f5 == AI or self.f2 == AI):
            self.f8 = AI
            return True
        else:
            return False

    def AI_justplay(self, AI):
        if self.f5 is None:
            self.f5 = AI
            return True
        elif self.f1 is None:
            self.f1 = AI
            return True
        elif self.f3 is None:
            self.f3 = AI
            return True
        elif self.f7 is None:
            self.f7 = AI
            return True
        elif self.f9 is None:
            self.f9 = AI
            return True
        elif self.f2 is None:
            self.f2 = AI
            return True
        elif self.f4 is None:
            self.f4 = AI
            return True
        elif self.f6 is None:
            self.f6 = AI
            return True
        elif self.f8 is None:
            self.f8 = AI
            return True
        else:
            return False
