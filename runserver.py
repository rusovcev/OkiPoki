"""
This script runs the OkiPoki application using a development server.
"""

from os import environ
from OkiPoki import app
from OkiPoki.models import db, Player

def init_db():
    db.init_app(app)
    db.app = app
    db.create_all()
    if not Player.query.get("AI"):
        db.session.add(Player("AI", "OkiPoki"))
        db.session.commit()

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5000
    print ("running...")
    init_db()
    #app.run(HOST, PORT, debug=True)
    app.run('0.0.0.0', PORT, debug=False)
