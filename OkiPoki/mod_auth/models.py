"""
database model players V2.0

"""

from OkiPoki import db

class Player(db.Model):
    """description of PLAYER/USER class
    """
    name = db.Column(db.String(32), unique=True, primary_key=True)
    passwd = db.Column(db.String(32))
    wins = db.Column(db.Integer, default=0)
    loses = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)

    def __init__(self, player_name, player_passwd):
        """
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            name (str): unique player's name.
            passwd (str): player's login passwd.

        """
        self.name = player_name
        self.passwd = player_passwd

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
        """class method required by flask-login."""
        return str(self.name)

    def add_win(self):
        """Increase wins by 1."""
        self.wins += 1
        return self.wins

    def add_lose(self):
        self.loses += 1
        return self.loses

    def add_draw(self):
        self.draws += 1
        return self.draws

def get_player_by_name(name: str):
    """class method to get player by name.
    
    """
    return Player.query.filter_by(name=name).first()

def signup_new_player(name, password):
    """class method to add new player/user to database.
    
    Args:
        name (str): unique name/id of player.
        password (str): something to act as a password.

    Returns:
        new player instance, if succeed.

    """
    new_player = Player(name, password)
    db.session.add(new_player)
    db.session.commit()
    return new_player

def update_standings():
    """Actualy, commit changes to database."""
    db.session.commit()
    return

def get_standings():
    """Get standings table."""
    return Player.query.order_by(Player.wins.desc()).all()
