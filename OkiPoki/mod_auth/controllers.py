"""Routes for player authentication and standings."""

from datetime import datetime
from flask import Blueprint, request, redirect, render_template, jsonify
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from OkiPoki import app
from OkiPoki.mod_auth.forms import SignupForm
from OkiPoki.mod_auth.models import get_standings, get_player_by_name, signup_new_player
from OkiPoki.mod_game.models import get_game, new_game

mod_auth = Blueprint("auth", __name__, url_prefix="/auth")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

logged_users = ["AI"] # reserved name AI
sent_invitations = []
accepted_invitations = []

@login_manager.user_loader
def load_user(name):
    return get_player_by_name(name)

@mod_auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """SignUp new player."""
    global logged_users
    form = SignupForm()
    if request.method == 'GET':
        return render_template('/auth/signup.html', form=form, title="sign up", year=datetime.now().year)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if get_player_by_name(form.name.data):
                return render_template('/auth/signup.html', form=form, title="sign up", year=datetime.now().year, message="player already exists?")
            else:
                new_user = signup_new_player(form.name.data, form.password.data)
                if new_user:
                    login_user(new_user)
                    logged_users.append(new_user.name)
                    return redirect("/")
                else:
                    return render_template('/auth/signup.html', form=form, title="sign up", year=datetime.now().year, message="error registering new player?")
        else:
            return render_template('/auth/signup.html', form=form, title="sign up", year=datetime.now().year, message="invalid credentials?")

@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    """SignIn existing user."""
    global logged_users
    form = SignupForm()
    if request.method == 'GET':
        return render_template('/auth/login.html', form=form, year=datetime.now().year)
    elif request.method == 'POST':
        if form.validate_on_submit():
            player = get_player_by_name(form.name.data)
            if player:
                if player in logged_users:
                    return render_template('/auth/login.html', form=form, title="Login", year=datetime.now().year, message="already signed?")
                if player.passwd == form.password.data:
                    login_user(player)
                    logged_users.append(player.name)
                    return redirect('/')
                else:
                    return render_template('/auth/login.html', form=form, title="Login", year=datetime.now().year, message="wrong credentials?")
            else:
                return redirect('/auth/signup')
        else:
            return render_template('/auth/login.html', form=form, title='login', message="user doesn't exist?")

@mod_auth.route('/logout')
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

@mod_auth.route("/logged/players", methods=["GET"])
def get_logged_players():
    """Path to get logged players from server."""
    logged = []
    for player in logged_users:
        if not current_user.is_authenticated or player != current_user.name:
            invited_by = False
            invited_by_me = False
            for i in sent_invitations:
                # am I invited by another player?
                if i['from'] == player and i['to'] == current_user.name:
                    invited_by = True
                # did I invite another player?
                if i['from'] == current_user.name and i['to'] == player:
                    invited_by_me = True
            game_id = None
            accepted_by = False
            for a in accepted_invitations:
                # has player accepted my invitation?
                if a['from'] == player and a['to'] == current_user.name:
                    accepted_by = True
                    game_id = a['gameID']

            logged.append({"name" : player, "invited" : invited_by, 
                           "invitedByMe" : invited_by_me, 
                           "accepted" : accepted_by, 
                           "gameID" : game_id})
    return jsonify({"response" : logged})

@mod_auth.route("/standings", methods=["GET"])
def get_player_standings():
    """Returns standings table."""
    standings = []
    players = get_standings()
    for player in players:
        standings.append({"name":player.name, 
                          "wins":player.wins, 
                          "loses":player.loses, 
                          "draws":player.draws})
    return jsonify({"response": standings})

@mod_auth.route('/invitation', methods=['GET', 'POST'])
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
            return jsonify({"response" : {"message" : "invitation accepted...", 
                                          "game" : {"gameID" : game_id, 
                                                    "playerX" : current_user.name, 
                                                    "playerO" : data["from"]}}})
        elif data['message'] == "rematch":
            # call for reMatch
            prevgame = get_game(int(data["gameID"]))
            if prevgame.player_x == "AI" or prevgame.player_o == "AI":
                game_id = new_game(3, prevgame.player_o, prevgame.player_x)
                return jsonify({"response" : {"message" : "re-match...", 
                                              "game" : {"gameID" : game_id, 
                                                        "playerX" : prevgame.player_o, 
                                                        "playerO" : prevgame.player_x}}})
            return
    elif request.method == "GET":
        data = request.args
        accepted_invitations.remove({"from" : data['player'], "to" : current_user.name, "gameID" : int(data['gameID'])})
        return jsonify({"response" : {"message" : "go2play", 
                                      "game" : {"gameID" : int(data['gameID']), 
                                                "playerX" : data['player'], 
                                                "playerO" : current_user.name}}})
