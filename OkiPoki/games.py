﻿'''
game model v2.
'''

import json
from OkiPoki import db

class Game(db.Model):
    """TicTacToe game class"""
    game_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    player_x = db.Column(db.String(80))
    player_o = db.Column(db.String(80))
    your_move = db.Column(db.String(1), default="X")
    board_size = db.Column(db.Integer, default=3)
    board_blob = db.Column(db.Text)

    def __init__(self, size, player_x, player_o):
        '''
        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            size (int): board size.
            player_x (str): X player name.
            player_o (str): O player name
        '''
        self.board_size = size
        board = ['' for r in range(size * size)]
        self.board_blob = json.dumps(board)
        self.player_x = player_x
        self.player_o = player_o
    
    def __repr__(self):
        return "<Game %r>" % self.game_id
    
    @property
    def is_over(self):
        board = json.loads(self.board_blob)
        if board.count('') == 0:
            return True
        return False

    @property
    def ai_to_play(self):
        if self.your_move == "X" and self.player_x == "AI":
            return True
        elif self.your_move == "O" and self.player_o == "AI":
            return True
        return False

    def update_board(self, field_id, player):
        """class method to update player's move to the board.
        
        Args:
            field_id (int): board's field, represented by index.
            player (str): player sign to occupy board field.

        Returns:
            True on succeed, False on error.

        """
        board = json.loads(self.board_blob)
        if board[field_id] == '':
            board[field_id] = player
            return True
        return False

    def is_row_won(self, row_id, player):
        """class method to check if row is occupied by players sign."""
        board = json.loads(self.board_blob)
        row = [board[column + row_id * self.board_size] for column in range(self.board_size)]
        if row.count(player) == self.board_size:
            return True
        return False

    def is_column_won(self, col_id, player):
        """class method to check if board column is won by player."""
        board = json.loads(self.board_blob)
        column = [board[col_id + self.board_size * row] for row in range(self.board_size)]
        if column.count(player) == self.board_size:
            return True
        return False

    def is_main_diagonal_won(self, player):
        """class method to check if main diagonal is occupied by player."""
        board = json.loads(self.board_blob)
        diagonal = [board[(1 + self.board_size) * row] for row in range(self.board_size)]
        if diagonal.count(player) == self.board_size:
            return True
        return False

    def is_antidiagonal_won(self, player):
        """class method to check if antidiagonal is occupied by player."""
        board = json.loads(self.board_blob)
        diagonal = [board[(row + 1) * (self.board_size - 1)] for row in range(self.board_size)]
        if diagonal.count(player) == self.board_size:
            return True
        return False

    def is_row_in_danger(self, row_id, player):
        """class method to check if opponent is in danger.
        
        Returns:
            list of free fields if 1 or 2 fields occupied by player and,
                False if at least one occupied by opponent.
        
        """
        board = json.loads(self.board_blob)
        free_fields = []
        for column in range(self.board_size):
            if board[column + self.board_size * row_id] == player:
                pass
            elif board[column + self.board_size * row_id] == '':
                free_fields.append(column + self.board_size * row_id)
            else:
                return False
        return free_fields

    def is_column_in_danger(self, col_id, player):
        """class method to check if possible to win by column."""
        board = json.loads(self.board_blob)
        free_fields = []
        for row in range(self.board_size):
            if board[col_id + row * self.board_size] == player:
                pass
            elif board[col_id + row * self.board_size] == '':
                free_fields.append(col_id + row * self.board_size)
            else:
                return False
        return free_fields

    def is_main_diagonal_in_danger(self, player):
        """class method to check if possible to win in main diagonal

        Returns:
            field index list if there is one free field and rest is occupied by player, False otherwise.

        """
        board = json.loads(self.board_blob)
        free_fields = []
        for idx in range(self.board_size):
            if board[(self.board_size + 1) * idx] == player:
                pass
            elif board[(self.board_size + 1) * idx] == '':
                free_fields.append((self.board_size + 1) * idx) # save free field's index
            else:
                return False # there is at least one field occupied by other sign
        return free_fields

    def is_antidiagonal_in_danger(self, player):
        """class method to check antidiagonal, same as main."""
        board = json.loads(self.board_blob)
        free_fields = []
        for row in range(self.board_size):
            if board[(row + 1) * (self.board_size - 1)] == player:
                pass
            elif board[(row + 1) * (self.board_size - 1)] == '':
                free_fields.append((row + 1) * (self.board_size - 1))
            else:
                return False
        return free_fields

def get_game(game_id):
    """function to retrive game by ID."""
    game = Game.query.filter_by(game_id=game_id).first()
    return game

def new_game(board_size, player_x, player_o):
    """Function to create new game and store it in db.
    
    Returns:
        new game id on success, otherwise False

    """
    game = Game(board_size, player_x, player_o)
    db.session.add(game)
    db.session.commit()
    if game is None:
        return False
    print (game.game_id)
    return game.game_id

def current_game_get_board(game_id):
    game = Game.query.filter_by(game_id=game_id).first()
    return json.loads(game.board_blob)

def current_game_update(game_id, field_index, player):
    game = Game.query.filter_by(game_id=game_id).first()
    board = json.loads(game.board_blob)
    board[field_index] = player
    game.board_blob = json.dumps(board)
    db.session.commit()
    return True

def current_game_switch_players(game_id):
    game = Game.query.filter_by(game_id=game_id).first()
    if game.your_move == "X":
        game.your_move = "O"
    else:
        game.your_move = "X"
    db.session.commit()
    return game.your_move

def check_game_won(game:Game, player):
    if game.is_main_diagonal_won(player) or game.is_antidiagonal_won(player):
        return True
    else:
        for row_or_column in range(game.board_size):
            if game.is_row_won(row_or_column, player) or game.is_column_won(row_or_column, player):
                return True
    return False

def go_for_win_ai(game):
    ai = game.your_move
    possible_moves = game.is_main_diagonal_in_danger(ai)
    if possible_moves and len(possible_moves) == 1:
        game.update_board(possible_moves[0], ai)
        db.session.commit()
        return possible_moves[0]
    possible_moves = game.is_antidiagonal_in_danger(ai)
    if possible_moves and len(possible_moves) == 1:
        game.update_board(possible_moves[0], ai)
        db.session.commit()
        return possible_moves[0]
    for row_or_column in range(game.board_size):
        possible_moves = game.is_row_in_danger(row_or_column, ai)
        if possible_moves and len(possible_moves) == 1:
            game.update_board(possible_moves[0], ai)
            db.session.commit()
            return possible_moves[0]
        possible_moves = game.is_column_in_danger(row_or_column, ai)
        if possible_moves and len(possible_moves) == 1:
            game.update_board(possible_moves[0], ai)
            db.session.commit()
            return possible_moves[0]
    return False

def go_defense_ai(game, opponent):
    ai = game.your_move
    possible_moves = game.is_main_diagonal_in_danger(opponent)
    if possible_moves and len(possible_moves) == 1:
        game.update_board(possible_moves[0], ai)
        db.session.commit()
        return possible_moves[0]
    possible_moves = game.is_antidiagonal_in_danger(opponent)
    if possible_moves and len(possible_moves) == 1:
        game.update_board(possible_moves[0], ai)
        db.session.commit()
        return possible_moves[0]
    for row_or_column in range(game.board_size):
        possible_moves = game.is_row_in_danger(row_or_column, opponent)
        if possible_moves and len(possible_moves) == 1:
            game.update_board(possible_moves[0], ai)
            db.session.commit()
            return possible_moves[0]
        possible_moves = game.is_column_in_danger(row_or_column, opponent)
        if possible_moves and len(possible_moves) == 1:
            game.update_board(possible_moves[0], ai)
            db.session.commit()
            return possible_moves[0]
    return False

def just_play_some_move_ai(game):
    ai = game.your_move
    for row in range(game.board_size):
        possible_moves = game.is_row_in_danger(row, ai)
        if possible_moves:
            game.update_board(possible_moves[0], ai)
            db.session.commit()
            return possible_moves[0]
    return False