from flask_sqlalchemy import SQLAlchemy
from OkiPoki import app

db = SQLAlchemy(app)

class Player(db.Model):
    """description of class
    """
    name = db.Column(db.String(80), primary_key=True, unique=True)
    password = db.Column(db.String(80))
    wins = db.Column(db.Integer, default=0)
    loses = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)

    def __init__(self, name, password):
        """Example of docstring on the __init__ method.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            name (str): unique player's name.
            param2 (str): player's login passwd.

        """
        self.name = name
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.name)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    playerX = db.Column(db.String(80))
    playerO = db.Column(db.String(80))
    player2move = db.Column(db.String(1), default="X")
    row1_col1 = db.Column(db.String(1), default="n")
    row1_col2 = db.Column(db.String(1), default="n")
    row1_col3 = db.Column(db.String(1), default="n")
    row2_col1 = db.Column(db.String(1), default="n")
    row2_col2 = db.Column(db.String(1), default="n")
    row2_col3 = db.Column(db.String(1), default="n")
    row3_col1 = db.Column(db.String(1), default="n")
    row3_col2 = db.Column(db.String(1), default="n")
    row3_col3 = db.Column(db.String(1), default="n")

    def __init__(self, playerX, playerO):
        self.playerX = playerX
        """str: player X, first to play"""
        self.playerO = playerO
        """str: player O"""
    
    def gameUpdate(self, field, player):
        """
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            field (str): board field to occupy.
            player (str): player's sign.

        Returns:
            True on success, False if invalid field is played.
        """
        if field == "f1" and self.row1_col1 == "n":
            self.row1_col1 = player
            return True
        elif field == "f2" and self.row1_col2 == "n":
            self.row1_col2 = player
            return True
        elif field == "f3" and self.row1_col3 == "n":
            self.row1_col3 = player
            return True
        elif field == "f4" and self.row2_col1 == "n":
            self.row2_col1 = player
            return True
        elif field == "f5" and self.row2_col2 == "n":
            self.row2_col2 = player
            return True
        elif field == "f6" and self.row2_col3 == "n":
            self.row2_col3 = player
            return True
        elif field == "f7" and self.row3_col1 == "n":
            self.row3_col1 = player
            return True
        elif field == "f8" and self.row3_col2 == "n":
            self.row3_col2 = player
            return True
        elif field == "f9" and self.row3_col3 == "n":
            self.row3_col3 = player
            return True
        else:
            return False

    def switchPlayer(self):
        """
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Returns:
            next to play sign, False otherwise.
        """
        if self.player2move == "X":
            self.player2move = "O"
            return True
        elif self.player2move == "O":
            self.player2move = "X"
            return True
        else:
            return False

    @property
    def gameWon(self):
        """
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Returns:
            Winner's sign if game is finished, False otherwise.
        """
        if  "X" == self.row1_col1 == self.row1_col2 == self.row1_col3 or \
            "X" == self.row2_col1 == self.row2_col2 == self.row2_col3 or \
            "X" == self.row3_col1 == self.row3_col2 == self.row3_col3 or \
            "X" == self.row1_col1 == self.row2_col1 == self.row3_col1 or \
            "X" == self.row1_col2 == self.row2_col2 == self.row3_col2 or \
            "X" == self.row1_col3 == self.row2_col3 == self.row3_col3 or \
            "X" == self.row1_col1 == self.row2_col2 == self.row3_col3 or \
            "X" == self.row1_col3 == self.row2_col2 == self.row3_col1:
            return "X"
        elif "O" == self.row1_col1 == self.row1_col2 == self.row1_col3 or \
            "O" == self.row2_col1 == self.row2_col2 == self.row2_col3 or \
            "O" == self.row3_col1 == self.row3_col2 == self.row3_col3 or \
            "O" == self.row1_col1 == self.row2_col1 == self.row3_col1 or \
            "O" == self.row1_col2 == self.row2_col2 == self.row3_col2 or \
            "O" == self.row1_col3 == self.row2_col3 == self.row3_col3 or \
            "O" == self.row1_col1 == self.row2_col2 == self.row3_col3 or \
            "O" == self.row1_col3 == self.row2_col2 == self.row3_col1:
            return "O"
        else:
            return False

    @property
    def gameOver(self):
        """
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Returns:
            True if no more free fields, False otherwise.
        """
        if self.row1_col1 is not 'n' and self.row1_col2 is not 'n' and self.row1_col3 is not 'n' and self.row2_col1 is not 'n' and self.row2_col2 is not 'n' and self.row2_col3 is not 'n' and self.row3_col1 is not 'n' and self.row3_col2 is not 'n' and self.row3_col3 is not 'n':
            return True
        else:
            return False

    def AI_finish(self, AI):
        if AI == self.row1_col1 == self.row1_col2 and self.row1_col3 == "n": # 1st row
            self.row1_col3 = AI
            return True
        elif AI == self.row1_col1 == self.row1_col3 and self.row1_col2 == "n": # 1st row
            self.row1_col2 = AI
            return True
        elif AI == self.row1_col2 == self.row1_col3 and self.row1_col1 == "n": # 1st row
            self.row1_col1 = AI
            return True
        elif AI == self.row2_col1 == self.row2_col2 and self.row2_col3 == "n": # 2nd row
            self.row2_col3 = AI
            return True
        elif AI == self.row2_col1 == self.row2_col3 and self.row2_col2 == "n": # 2nd row
            self.row2_col2 = AI
            return True
        elif AI == self.row2_col2 == self.row2_col3 and self.row2_col1 == "n": # 2nd row
            self.row2_col1 = AI
            return True
        elif AI == self.row3_col1 == self.row3_col2 and self.row3_col3 == "n": # 3rd row
            self.row3_col3 = AI
            return True
        elif AI == self.row3_col1 == self.row3_col3 and self.row3_col2 == "n": # 3rd row
            self.row3_col2 = AI
            return True
        elif AI == self.row3_col2 == self.row3_col3 and self.row3_col1 == "n": # 3rd row
            self.row3_col1 = AI
            return True
        elif AI == self.row1_col1 == self.row2_col1 and self.row3_col1 == "n": # 1st col
            self.row3_col1 = AI
            return True
        elif AI == self.row1_col1 == self.row3_col1 and self.row2_col1 == "n": # 1st col
            self.row2_col1 = AI
            return True
        elif AI == self.row2_col1 == self.row3_col1 and self.row1_col1 == "n": # 1st col
            self.row1_col1 = AI
            return True
        elif AI == self.row1_col2 == self.row2_col2 and self.row3_col2 == "n": # 2nd col
            self.row3_col2 = AI
            return True
        elif AI == self.row1_col2 == self.row3_col2 and self.row2_col2 == "n": # 2nd col
            self.row2_col2 = AI
            return True
        elif AI == self.row2_col2 == self.row3_col2 and self.row1_col2 == "n": # 2nd col
            self.row1_col2 = AI
            return True
        elif AI == self.row1_col3 == self.row2_col3 and self.row3_col3 == "n": # 3rd col
            self.row3_col3 = AI
            return True
        elif AI == self.row1_col3 == self.row3_col3 and self.row2_col3 == "n": # 3rd col
            self.row2_col3 = AI
            return True
        elif AI == self.row2_col3 == self.row3_col3 and self.row1_col3 == "n": # 3rd col
            self.row1_col3 = AI
            return True
        elif AI == self.row1_col1 == self.row2_col2 and self.row3_col3 == "n": # 1st diag
            self.row3_col3 = AI
            return True
        elif AI == self.row1_col1 == self.row3_col3 and self.row2_col2 == "n": # 1st diag
            self.row2_col2 = AI
            return True
        elif AI == self.row2_col2 == self.row3_col3 and self.row1_col1 == "n": # 1st diag
            self.row1_col1 = AI
            return True
        elif AI == self.row1_col3 == self.row2_col2 and self.row3_col1 == "n": # 2nd diag
            self.row3_col1 = AI
            return True
        elif AI == self.row1_col3 == self.row3_col1 and self.row2_col2 == "n": # 2nd diag
            self.row2_col2 = AI
            return True
        elif AI == self.row2_col2 == self.row3_col1 and self.row1_col3 == "n": # 2nd diag
            self.row1_col3 = AI
            return True
        else:
            return False

    def AI_deffensive(self, AI, opponent):
        if opponent == self.row1_col1 == self.row1_col2 and self.row1_col3 == "n": # 1st row
            self.row1_col3 = AI
            return True
        elif opponent == self.row1_col1 == self.row1_col3 and self.row1_col2 == "n": # 1st row
            self.row1_col2 = AI
            return True
        elif opponent == self.row1_col2 == self.row1_col3 and self.row1_col1 == "n": # 1st row
            self.row1_col1 = AI
            return True
        elif opponent == self.row2_col1 == self.row2_col2 and self.row2_col3 == "n": # 2nd row
            self.row2_col3 = AI
            return True
        elif opponent == self.row2_col1 == self.row2_col3 and self.row2_col2 == "n": # 2nd row
            self.row2_col2 = AI
            return True
        elif opponent == self.row2_col2 == self.row2_col3 and self.row2_col1 == "n": # 2nd row
            self.row2_col1 = AI
            return True
        elif opponent == self.row3_col1 == self.row3_col2 and self.row3_col3 == "n": # 3rd row
            self.row3_col3 = AI
            return True
        elif opponent == self.row3_col1 == self.row3_col3 and self.row3_col2 == "n": # 3rd row
            self.row3_col2 = AI
            return True
        elif opponent == self.row3_col2 == self.row3_col3 and self.row3_col1 == "n": # 3rd row
            self.row3_col1 = AI
            return True
        elif opponent == self.row1_col1 == self.row2_col1 and self.row3_col1 == "n": # 1st col
            self.row3_col1 = AI
            return True
        elif opponent == self.row1_col1 == self.row3_col1 and self.row2_col1 == "n": # 1st col
            self.row2_col1 = AI
            return True
        elif opponent == self.row2_col1 == self.row3_col1 and self.row1_col1 == "n": # 1st col
            self.row1_col1 = AI
            return True
        elif opponent == self.row1_col2 == self.row2_col2 and self.row3_col2 == "n": # 2nd col
            self.row3_col2 = AI
            return True
        elif opponent == self.row1_col2 == self.row3_col2 and self.row2_col2 == "n": # 2nd col
            self.row2_col2 = AI
            return True
        elif opponent == self.row2_col2 == self.row3_col2 and self.row1_col2 == "n": # 2nd col
            self.row1_col2 = AI
            return True
        elif opponent == self.row1_col3 == self.row2_col3 and self.row3_col3 == "n": # 3rd col
            self.row3_col3 = AI
            return True
        elif opponent == self.row1_col3 == self.row3_col3 and self.row2_col3 == "n": # 3rd col
            self.row2_col3 = AI
            return True
        elif opponent == self.row2_col3 == self.row3_col3 and self.row1_col3 == "n": # 3rd col
            self.row1_col3 = AI
            return True
        elif opponent == self.row1_col1 == self.row2_col2 and self.row3_col3 == "n": # 1st diag
            self.row3_col3 = AI
            return True
        elif opponent == self.row1_col1 == self.row3_col3 and self.row2_col2 == "n": # 1st diag
            self.row2_col2 = AI
            return True
        elif opponent == self.row2_col2 == self.row3_col3 and self.row1_col1 == "n": # 1st diag
            self.row1_col1 = AI
            return True
        elif opponent == self.row1_col3 == self.row2_col2 and self.row3_col1 == "n": # 2nd diag
            self.row3_col1 = AI
            return True
        elif opponent == self.row1_col3 == self.row3_col1 and self.row2_col2 == "n": # 2nd diag
            self.row2_col2 = AI
            return True
        elif opponent == self.row2_col2 == self.row3_col1 and self.row1_col3 == "n": # 2nd diag
            self.row1_col3 = AI
            return True
        else:
            return False

    def AI_offensive(self, AI):
        if self.row2_col2 == "n" and (self.row1_col1 == AI or self.row1_col2 == AI or self.row1_col3 == AI or self.row2_col1 == AI or self.row2_col3 == AI or self.row3_col1 or self.row3_col2 == AI or self.row3_col3 == AI):
            self.row2_col2 = AI
            return True
        elif self.row1_col1 == "n" and self.row2_col2 == AI and self.row3_col3 == "n":
            self.row1_col1 = AI
            return True
        elif self.row1_col1 == "n" and (self.row1_col2 == AI or self.row1_col3 == AI or self.row2_col1 == AI or self.row3_col1 == AI or self.row2_col2 == AI or self.row3_col3 == AI):
            self.row1_col1 = AI
            return True
        elif self.row1_col3 == "n" and (self.row1_col1 == AI or self.row1_col2 == AI or self.row2_col3 == AI or self.row3_col3 == AI or self.row2_col2 == AI or self.row3_col1 == AI):
            self.row1_col3 = AI
            return True
        elif self.row3_col1 == "n" and (self.row1_col1 == AI or self.row2_col1 == AI or self.row3_col2 == AI or self.row3_col3 == AI or self.row2_col2 == AI or self.row1_col3 == AI):
            self.row3_col1 = AI
            return True
        elif self.row3_col3 == "n" and (self.row1_col3 == AI or self.row2_col3 == AI or self.row3_col1 == AI or self.row3_col2 == AI or self.row2_col2 == AI or self.row1_col1 == AI):
            self.row3_col3 = AI
            return True
        elif self.row1_col2 == "n" and (self.row1_col1 == AI or self.row1_col3 == AI or self.row2_col2 == AI or self.row3_col2 == AI):
            self.row1_col2 = AI
            return True
        elif self.row2_col1 == "n" and (self.row1_col1 == AI or self.row3_col1 == AI or self.row2_col2 == AI or self.row2_col3 == AI):
            self.row2_col1 = AI
            return True
        elif self.row2_col3 == "n" and (self.row1_col3 == AI or self.row3_col3 == AI or self.row2_col2 == AI or self.row2_col1 == AI):
            self.row2_col3 = AI
            return True
        elif self.row3_col2 == "n" and (self.row3_col1 == AI or self.row3_col3 == AI or self.row2_col2 == AI or self.row1_col2 == AI):
            self.row3_col2 = AI
            return True
        else:
            return False

    def AI_justplay(self, AI):
        if self.row2_col2 == "n":
            self.row2_col2 = AI
            return True
        elif self.row1_col1 == "n":
            self.row1_col1 = AI
            return True
        elif self.row1_col3 == "n":
            self.row1_col3 = AI
            return True
        elif self.row3_col1 == "n":
            self.row3_col1 = AI
            return True
        elif self.row3_col3 == "n":
            self.row3_col3 = AI
            return True
        elif self.row1_col2 == "n":
            self.row1_col2 = AI
            return True
        elif self.row2_col1 == "n":
            self.row2_col1 = AI
            return True
        elif self.row2_col3 == "n":
            self.row2_col3 = AI
            return True
        elif self.row3_col2 == "n":
            self.row3_col2 = AI
            return True
        else:
            return False
