"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, jsonify, redirect, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from OkiPoki import app
from OkiPoki.models import Player, Game, db
from OkiPoki.forms import SignupForm

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

loggedUsers = ["AI", "bob","tbb"]
invitations = []
accepted_invitations = []

@login_manager.user_loader
def load_user(name):
    return Player.query.filter_by(name=name).first()

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = "no-cache, no-store"
    return response

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global loggedUsers
    form = SignupForm()
    if request.method == 'GET':
        return render_template('signup.html', form = form, title = "sign up", year = datetime.now().year)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if Player.query.filter_by(name=form.name.data).first():
                return render_template('signup.html', form = form, title = "sign up", year = datetime.now().year, message = "player already exists?")
                #return jsonify({"response" : {"message" : "user already exist"}})
            else:
                newPlayer = Player(form.name.data, form.password.data)
                db.session.add(newPlayer)
                db.session.commit()
                login_user(newPlayer)
                loggedUsers.append(newPlayer.name)
                return redirect ("/")
                #return jsonify({"response" : {"message" : "new player added..."}})
        else:
            return render_template('signup.html', form = form, title = "sign up", year = datetime.now().year, message = "invalid credentials?")

@app.route('/login', methods=['GET', 'POST'])
def login():
    global loggedUsers
    form = SignupForm()
    if request.method == 'GET':
        return render_template('login.html', form = form, year = datetime.now().year)
    elif request.method == 'POST':
        if form.validate_on_submit():
            player = Player.query.filter_by(name=form.name.data).first()
            if player:
                if player in loggedUsers:
                    return render_template('login.html', form=form, title="Login", year=datetime.now().year, message="already signed?")
                    #return jsonify({"response": {"message" : "already logged?"}})
                if player.password == form.password.data:
                    player.logged = True
                    db.session.commit()
                    login_user(player)
                    loggedUsers.append(player.name)
                    return redirect('/')
                    #return jsonify({"response" : {"message" : "player logged..."}})
                else:
                    return render_template('login.html', form=form, title="Login", year=datetime.now().year, message="wrong password?")
                    #return jsonify({"response" : {"message" : "wrong password?"}})
            else:
                return redirect('/signup')
                #return jsonify({"response" : {"message" : "player doesnt exist?"}})
        else:
            return render_template('login.html', form = form, title = 'login', message = 'invalid?')

@app.route('/logout')
@login_required
def logout():
    global loggedUsers
    print ("logout user:", current_user.name)
    player = Player.query.filter_by(name=current_user.name).first()
    player.logged = False
    db.session.commit()
    try:
        loggedUsers.remove(current_user.name)
    except ValueError:
        print ("Oops! not in the list?")
        pass
    logout_user()
    return redirect('/')

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/invitation', methods=['GET', 'POST'])
@login_required
def invitation():
    global invitations, accepted_invitations
    if request.method == "POST":
        data = request.get_json()
        if data['message'] == 'invite':
            """ send invitation """
            if data["who"] == "AI":
                """ AI """
                newGame = gameplay("new", "AI", current_user.name)
                accepted_invitations.append({ "from" : "AI", "to" : current_user.name, "gameID" : newGame.id })
                """ AI """
            else:
                """ HUMAN """
                invitations.append({ "from" : current_user.name, "to" : data['who']})
                """ HUMAN """
            return jsonify({"response" : {"message" : "invitation sent..."}})
            """ send invitation """
        elif data['message'] == 'accepted':
            """ invitation is ACCEPTED """
            newGame = gameplay('new', current_user.name, data['from'])
            invitations.remove({ "from" : data['from'], "to" : current_user.name })
            accepted_invitations.append({ "from" : current_user.name, "to" : data['from'], "gameID" : newGame.id })
            return jsonify({ "response" : {"message" : "invitation accepted...", "game" : { "gameID" : newGame.id, "playerX" : newGame.playerX, "playerO" : newGame.playerO}}})
            """ invitation is ACCEPTED """
        elif data['message'] == "rematch":
            """ reMatch """
            prevgame = Game.query.get(int(data["gameID"]))
            if prevgame.playerX == "AI" or prevgame.playerO == "AI":
                newGame = gameplay("new", prevgame.playerO, prevgame.playerX)
                return jsonify({ "response" : {"message" : "re-match...", "game" : { "gameID" : newGame.id, "playerX" : newGame.playerX, "playerO" : newGame.playerO}}})
            return
            """ reMatch """
    elif request.method == "GET":
        data = request.args
        accepted_invitations.remove({ "from" : data['player'], "to" : current_user.name, "gameID" : int(data['gameID']) })
        return jsonify({"response" : {"message" : "go2play", "game" : {"gameID" : int(data['gameID']), "playerX" : data['player'], "playerO" : current_user.name}}})

@app.route('/board', methods=['GET'])
@login_required
def board():
    """Renders the board page."""
    return render_template(
        'game.html',
        title='Game',
        year=datetime.now().year,
        message='okipoki board.'
    )

@app.route("/play", methods=["GET", "POST"])
@login_required
def play():
    print (request.method)
    if request.method == "POST":
        data = request.get_json()

        game = Game.query.filter_by(id=int(data['gameID'])).first()

        """ update board """
        if not game.gameUpdate(data["move"], data["Iam"]):
            print ("failed...")
            return jsonify({"response" : False})

        print("HUMAN:")
        print("playerX:",game.playerX)
        print("playerO:",game.playerO)
        print("I am:   ",data["Iam"])

        gameWinner = game.gameWon()
        print("winner  :", gameWinner)
        gameOver = game.gameOver()
        print("gameover:", gameOver)
        if gameWinner:
            """ We have a WINNER (and loser) """
            if gameWinner == "X":
                winnerName = game.playerX
                loserName = game.playerO
            else:
                winnerName = game.playerO
                loserName = game.playerX
            """ result WIN-LOSE """
            winner = Player.query.filter_by(name=winnerName).first()
            winner.wins += 1
            loser = Player.query.filter_by(name=loserName).first()
            loser.loses += 1
            """ result WIN-LOSE """
            gWon = True
            gOver = True
            gDraw = False
        elif gameOver:
            """ result DRAW """
            drawX = Player.query.filter_by(name=game.playerX).first()
            drawX.draws += 1
            drawO = Player.query.filter_by(name=game.playerO).first()
            drawO.draws += 1
            """ result DRAW """
            gWon = False
            gOver = True
            gDraw = True
        else:
            gWon = False
            gOver = False
            gDraw = False
            """ switch players """
            game.switchPlayer()
            
        db.session.commit()

        return jsonify({"response" : {"board" : [game.f1,game.f2,game.f3,game.f4,game.f5,game.f6,game.f7,game.f8,game.f9], "gameOver" : gOver, "Won" : gWon, "Draw" : gDraw, "toplay" : game.player2move}})

    elif request.method == "GET":
        data = request.args
        game = Game.query.filter_by(id=int(data['gameID'])).first()

        print("playerX:",game.playerX)
        print("playerO:",game.playerO)
        print("I am:   ",data["Iam"])

        if (game.player2move == "X" and game.playerX == "AI") or (game.player2move == "O" and game.playerO == "AI"):
            if not game.gameWon() and not game.gameOver():
                if game.playerX == "AI" and data["Iam"] == "O":
                    AI = "X"
                elif game.playerO == "AI" and data["Iam"] == "X":
                    AI = "O"
                print("AI to play...")
                if game.AI_finish(AI):
                    print ("AI wins!")
                elif game.AI_deffensive(AI, data["Iam"]):
                    print("defense!")
                elif game.AI_offensive(AI):
                    print("offensive?")
                elif game.AI_justplay(AI):
                    print("just played something...")
                else:
                    print("FAILED!")
                    return jsonify({"response" : {"board":[]}})
                """ switch players """
                game.switchPlayer()
                db.session.commit()
                print("AI has moved...")
        
        gameWinner = game.gameWon()
        print("winner  :", gameWinner)
        gameOver = game.gameOver()
        print("gameover:", gameOver)
        if gameWinner:
            if gameWinner == data["Iam"]:
                gWon = True
            else:
                gWon = False
            gOver = True
            gDraw = False
        elif gameOver:
            gWon = False
            gOver = True
            gDraw = True
        else:
            gWon = False
            gOver = False
            gDraw = False
            
        return jsonify({"response" : {"board" : [game.f1,game.f2,game.f3,game.f4,game.f5,game.f6,game.f7,game.f8,game.f9], "gameOver" : gOver, "Won" : gWon, "Draw" : gDraw, "toplay" : game.player2move}})

def gameplay(id, playerX, playerO):
    if id is "new":
        if playerO is None:
            playerO = "AI"
        newGame = Game(playerX, playerO)
        db.session.add(newGame)
        db.session.commit()
        return newGame
    else:
        game = Game.query.filter_by(id=id).first()
        return game

@app.route("/logged/players", methods=["GET"])
def get_logged_players():
    logged = []
    print ("invitations:", invitations)
    print ("accepted invitations: ", accepted_invitations)
    for p in loggedUsers: #players:
        if not current_user.is_authenticated or p != current_user.name:

            invited = False
            invitedByMe = False
            for i in invitations:
                # am I invited by another player?
                if i['from'] == p and i['to'] == current_user.name: 
                    invited = True
                if i['from'] == current_user.name and i['to'] == p:
                    invitedByMe = True

            gameid = None
            accepted = False
            for a in accepted_invitations:
                # has player accepted my invitation?
                if a['from'] == p and a['to'] == current_user.name:
                    accepted = True
                    gameid = a['gameID']

            logged.append({ "name" : p, "invited" : invited, "invitedByMe" : invitedByMe, "accepted" : accepted, "gameID" : gameid })

    #print ("logged: ", logged);
    return jsonify({"response" : logged})

@app.route("/standings", methods=["GET"])
def standings():
    standings = []
    players = Player.query.order_by(Player.wins.desc()).all()
    for p in players:
        standings.append({"name":p.name, "wins":p.wins, "loses":p.loses, "draws":p.draws})
    return jsonify({"response": standings})
