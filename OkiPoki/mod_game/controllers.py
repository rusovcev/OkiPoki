"""
Routes and views for the game module.
"""

from datetime import datetime
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from OkiPoki.mod_auth.models import get_player_by_name, update_standings
from OkiPoki.mod_game.models import get_game, current_game_get_board, current_game_update, current_game_switch_players, check_if_game_won, play_winning_move, play_deffensive_move, play_offensive_move, play_free_move

mod_game = Blueprint("game", __name__, url_prefix="/game")

@mod_game.after_request
def add_header(response):
    response.headers['Cache-Control'] = "no-cache"
    return response

@mod_game.route('/board', methods=['GET'])
@login_required
def board():
    """Renders the board page."""
    return render_template(
        'game.html',
        title='Game',
        year=datetime.now().year,
        message='okipoki board.'
    )

@mod_game.route("/play", methods=["GET", "POST"])
@login_required
def play():
    """POST the move, or GET opponent's move."""
    if request.method == "POST":
        data = request.get_json()
        current_game_board = current_game_get_board(int(data["gameID"]))
        if not current_game_update(int(data["gameID"]), data["move"], data["Iam"]):
            print("failed...")
            return jsonify({"response" : False})
        next_player = current_game_switch_players(int(data["gameID"]))
        return jsonify({"response" : {"board" : current_game_board, 
                                      "gameOver" : False, 
                                      "Won" : False, 
                                      "Draw" : False, 
                                      "toplay" : next_player}})
    elif request.method == "GET":
        data = request.args
        current_game = get_game(int(data["gameID"]))
        current_game_board = current_game_get_board(int(data["gameID"]))
        next_player = data["opponent"]
        game_won_flag = False
        game_over_flag = False
        game_draw_flag = False

        if current_game.ai_to_play:
            if play_winning_move(current_game) is not False:
                print("AI for win!!!")
            elif play_deffensive_move(current_game, data["Iam"]) is not False:
                print("AI in deffense!")
            elif play_offensive_move(current_game) is not False:
                print("AI offensive move?")
            elif play_free_move(current_game) is not False:
                print("AI free move...")
            else:
                print("AI: Oops?")
            next_player = current_game_switch_players(int(data["gameID"]))
            current_game_board = current_game_get_board(int(data["gameID"]))

        if check_if_game_won(current_game, data["Iam"]):
            game_over_flag = True
            game_won_flag = True
            game_draw_flag = False
            player = get_player_by_name(current_user.name)
            player.add_win()
            if current_game.vs_ai:
                ai = get_player_by_name("AI")
                ai.add_lose()
            update_standings()
        elif check_if_game_won(current_game, data["opponent"]):
            game_over_flag = True
            game_won_flag = False
            game_draw_flag = False
            player = get_player_by_name(current_user.name)
            player.add_lose()
            if current_game.vs_ai:
                ai = get_player_by_name("AI")
                ai.add_win()
            update_standings()
        elif current_game.no_more_free_fields:
            game_over_flag = True
            game_won_flag = False
            game_draw_flag = True
            player = get_player_by_name(current_user.name)
            player.add_draw()
            if current_game.vs_ai:
                ai = get_player_by_name("AI")
                ai.add_draw()
            update_standings()
        else:
            game_draw_flag = False
            game_over_flag = False
            game_won_flag = False
        return jsonify({"response" : {"board" : current_game_board, 
                                      "gameOver" : game_over_flag, 
                                      "Won" : game_won_flag, 
                                      "Draw" : game_draw_flag, 
                                      "toplay" : current_game.your_move}})
