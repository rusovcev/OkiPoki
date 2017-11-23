"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, jsonify, redirect, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from OkiPoki import app
from OkiPoki.players import Player, get_player_by_name, signup_new_player, update_standings
from OkiPoki.games import *
from OkiPoki.forms import SignupForm

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

logged_users = ["AI", "bob", "tbb"] # reserved name AI
sent_invitations = []
accepted_invitations = []

@login_manager.user_loader
def load_user(name):
    return get_player_by_name(name)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = "no-cache"
    return response

@app.route('/')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """SignUp new player."""
    global logged_users
    form = SignupForm()
    if request.method == 'GET':
        return render_template('signup.html', form=form, title="sign up", year=datetime.now().year)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if get_player_by_name(form.name.data):
                return render_template('signup.html', form=form, title="sign up", year=datetime.now().year, message="player already exists?")
            else:
                new_user = signup_new_player(form.name.data, form.password.data)
                if new_user:
                    login_user(new_user)
                    logged_users.append(new_user.name)
                    return redirect("/")
                else:
                    return render_template('signup.html', form=form, title="sign up", year=datetime.now().year, message="error registering new player?")
        else:
            return render_template('signup.html', form=form, title="sign up", year=datetime.now().year, message="invalid credentials?")

@app.route('/login', methods=['GET', 'POST'])
def login():
    """SignIn existing user."""
    global logged_users
    form = SignupForm()
    if request.method == 'GET':
        return render_template('login.html', form=form, year=datetime.now().year)
    elif request.method == 'POST':
        if form.validate_on_submit():
            player = get_player_by_name(form.name.data)
            if player:
                if player in logged_users:
                    return render_template('login.html', form=form, title="Login", year=datetime.now().year, message="already signed?")
                if player.passwd == form.password.data:
                    login_user(player)
                    logged_users.append(player.name)
                    return redirect('/')
                else:
                    return render_template('login.html', form=form, title="Login", year=datetime.now().year, message="wrong credentials?")
            else:
                return redirect('/signup')
        else:
            return render_template('login.html', form=form, title='login', message="user doesn't exist?")

@app.route('/logout')
@login_required
def logout():
    """Logout the current user."""
    global logged_users
    print("logout user:", current_user.name)
    try:
        logged_users.remove(current_user.name)
    except ValueError:
        print("Oops! not in the list?")
    logout_user()
    return redirect('/')

@app.route("/logged/players", methods=["GET"])
def get_logged_players():
    logged = []
    print("invitations:", sent_invitations)
    print("accepted invitations: ", accepted_invitations)
    for p in logged_users:
        if not current_user.is_authenticated or p != current_user.name:
            invited_by = False
            invited_by_me = False
            for i in sent_invitations:
                # am I invited by another player?
                if i['from'] == p and i['to'] == current_user.name:
                    invited_by = True
                # did I invite another player?
                if i['from'] == current_user.name and i['to'] == p:
                    invited_by_me = True
            game_id = None
            accepted_by = False
            for a in accepted_invitations:
                # has player accepted my invitation?
                if a['from'] == p and a['to'] == current_user.name:
                    accepted_by = True
                    game_id = a['gameID']

            logged.append({"name" : p, "invited" : invited_by, "invitedByMe" : invited_by_me, "accepted" : accepted_by, "gameID" : game_id})
    return jsonify({"response" : logged})

@app.route("/standings", methods=["GET"])
def get_player_standings():
    standings = []
    players = Player.query.order_by(Player.wins.desc()).all()
    for p in players:
        standings.append({"name":p.name, "wins":p.wins, "loses":p.loses, "draws":p.draws})
    return jsonify({"response": standings})

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
    print(request.method)
    if request.method == "POST":
        data = request.get_json()
        current_game_board = current_game_get_board(int(data["gameID"]))
        if not current_game_update(int(data["gameID"]), data["move"], data["Iam"]):
            print("failed...")
            return jsonify({"response" : False})
        next_player = current_game_switch_players(int(data["gameID"]))
        return jsonify({"response" : {"board" : current_game_board, "gameOver" : False, "Won" : False, "Draw" : False, "toplay" : next_player}})
    elif request.method == "GET":
        data = request.args
        current_game_board = current_game_get_board(int(data["gameID"]))
        current_game = get_game(int(data["gameID"]))
        next_player = data["opponent"]
        game_won_flag = False
        game_over_flag = False
        game_draw_flag = False
        if not current_game.is_over:
            if check_game_won(current_game, data["Iam"]):
                game_over_flag = True
                game_won_flag = True
                player = get_player_by_name(current_user.name)
                player.add_win()
                update_standings()
            elif check_game_won(current_game, data["opponent"]):
                game_over_flag = True
                game_won_flag = False
                player = get_player_by_name(current_user.name)
                player.add_lose()
                update_standings()
            elif current_game.ai_to_play:
                if go_for_win_ai(current_game):
                    print("AI for win")
                    pass
                elif go_defense_ai(current_game, data["Iam"]):
                    print("AI in defense")
                    pass
                elif just_play_some_move_ai(current_game):
                    print("AI moved...")
                    pass
                else:
                    print("AI: Oops?")
                    return False
                next_player = current_game_switch_players(int(data["gameID"]))
                current_game_board = current_game_get_board(int(data["gameID"]))
        else:
            game_over_flag = True
            game_won_flag = False
            game_draw_flag = True
            player = get_player_by_name(current_user.name)
            player.add_draw()
            update_standings()
        return jsonify({"response" : {"board" : current_game_board, "gameOver" : game_over_flag, "Won" : game_won_flag, "Draw" : game_draw_flag, "toplay" : next_player}})

@app.route('/invitation', methods=['GET', 'POST'])
@login_required
def invitation():
    global sent_invitations, accepted_invitations
    if request.method == "POST":
        data = request.get_json()
        if data['message'] == 'invite':
            # send invitation
            if data["who"] == "AI":
                # send to AI
                game_id = new_game(3, "AI", current_user.name)
                accepted_invitations.append({"from" : "AI", "to" : current_user.name, "gameID" : game_id})
            else:
                # or to HUMAN
                sent_invitations.append({"from" : current_user.name, "to" : data['who']})
            return jsonify({"response" : {"message" : "invitation sent..."}})
        elif data['message'] == 'accepted':
            # invitation is ACCEPTED
            game_id = new_game(3, current_user.name, data['from'])
            sent_invitations.remove({"from" : data['from'], "to" : current_user.name})
            accepted_invitations.append({"from" : current_user.name, "to" : data['from'], "gameID" : game_id})
            return jsonify({"response" : {"message" : "invitation accepted...", "game" : {"gameID" : game_id, "playerX" : current_user.name, "playerO" : data["from"]}}})
        elif data['message'] == "rematch":
            # call for reMatch
            prevgame = get_game(int(data["gameID"]))
            if prevgame.player_x == "AI" or prevgame.player_o == "AI":
                game_id = new_game(1, prevgame.player_o, prevgame.player_x)
                return jsonify({"response" : {"message" : "re-match...", "game" : {"gameID" : game_id, "playerX" : prevgame.player_o, "playerO" : prevgame.player_x}}})
            return
    elif request.method == "GET":
        data = request.args
        accepted_invitations.remove({"from" : data['player'], "to" : current_user.name, "gameID" : int(data['gameID'])})
        return jsonify({"response" : {"message" : "go2play", "game" : {"gameID" : int(data['gameID']), "playerX" : data['player'], "playerO" : current_user.name}}})
