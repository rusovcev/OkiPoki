import unittest, json
from unittest import mock
from OkiPoki.mod_game.models import Game, get_game, play_winning_move, play_deffensive_move, play_offensive_move

class Test_model_game(unittest.TestCase):
    @mock.patch("OkiPoki.mod_game.models.Game")
    def test_get_game(self, mock_game):
        test_new_game = Game(3, "playerX", "playerO")
        test_new_game.board_size = 3
        test_new_game.player_x = "playerX"
        test_new_game.player_o = "playerO"
        test_new_game.your_move = "X"
        test_new_game.board_blob = json.dumps(['', '', 'X',
                                               '', '', '',
                                               '', '', ''])
        mock_game.query.filter_by.return_value.first.return_value = test_new_game
        assert(get_game(0) == test_new_game)

    @mock.patch("OkiPoki.mod_game.models.Game")
    def test_if_proper_move_by_player(self, mock_game):
        test_new_game = Game(3, "playerX", "playerO")
        test_new_game.board_size = 3
        test_new_game.player_x = "playerX"
        test_new_game.player_o = "playerO"
        test_new_game.your_move = "X"
        test_new_game.board_blob = json.dumps(['', '', 'X',
                                               '', 'O', '',
                                               'X', '', ''])
        assert(test_new_game.save_player_move(1, 'X') is True)
        assert(test_new_game.save_player_move(2, 'O') is False)

    @mock.patch("OkiPoki.mod_game.models.Game")
    def test_case_if_3_in_row(self, mock_game):
        test_game = Game(3, "playerX", "playerO")
        test_game.game_id = 1
        test_game.board_size = 3
        test_game.player_x = "playerX"
        test_game.player_o = "playerO"
        test_game.your_move = "X"
        test_game.board_blob = json.dumps(['X', 'X', 'X',
                                           'X', '', 'O',
                                           'X', 'O', ''])
        assert(test_game.is_row_won(0, 'X') is True)
        assert(test_game.is_row_won(1, 'O') is False)
        assert(test_game.is_row_won(2, 'O') is False)
        assert(test_game.is_row_won(2, 'X') is False)

    @mock.patch("OkiPoki.mod_game.models.Game")
    def test_case_if_3_in_column(self, mock_game):
        test_game = Game(3, "Foo", "Bar")
        test_game.your_move = "O"
        test_game.board_blob = json.dumps(['O', 'X', '',
                                           'O', '', 'X',
                                           'O', 'X', ''])
        assert(test_game.is_column_won(0, test_game.your_move) is True)
        assert(test_game.is_column_won(1, 'O') is False)
        assert(test_game.is_column_won(2, 'X') is False)

    @mock.patch("OkiPoki.mod_game.models.Game")
    def test_case_if_3_in_diagonal(self, mock_game):
        test_game = Game(3, "Jackie", "Brown")
        test_game.game_id = 1001
        test_game.board_size = 3
        test_game.your_move = "O"
        test_game.board_blob = json.dumps(['O', 'X', 'O',
                                           'X', 'O', 'X',
                                           'O', 'X', ''])
        assert(test_game.is_main_diagonal_won(test_game.your_move) is False)
        assert(test_game.is_antidiagonal_won(test_game.your_move) is True)

    @mock.patch("OkiPoki.mod_game.models.Game")
    def test_case_if_row_is_about_to_be_foobar(self, mock_game):
        """Test if game is to be won/lost by player."""
        test_game = Game(3, "playerX", "playerO")
        test_game.game_id = 1002
        test_game.board_size = 3
        test_game.your_move = "X"
        test_game.board_blob = json.dumps(['X', '', 'O',
                                           'X', '', '',
                                           'X', 'X', ''])
        assert(test_game.is_row_in_danger(0, "X") is False)
        assert(test_game.is_row_in_danger(1, "X") == [4, 5])
        assert(test_game.is_row_in_danger(2, "X") == [8])

    @mock.patch("OkiPoki.mod_game.models.Game")
    def test_case_if_column_is_about_to_be_jam(self, mock_game):
        test_game = Game(3, "player", "dancer")
        test_game.board_blob = json.dumps(['X', '', 'O',
                                           'X', '', '',
                                           'X', 'X', ''])
        assert(test_game.is_column_in_danger(0, "X") == [])
        assert(test_game.is_column_in_danger(1, "O") == False)
        assert(test_game.is_column_in_danger(2, "O") == [5, 8])

    @mock.patch("OkiPoki.mod_game.models.Game")
    def test_case_if_diagonal_is_about_to_be_full(self, mock_game):
        test_game = Game(3, "playerX", "playerO")
        test_game.board_blob = json.dumps(['X', '', 'O',
                                           'X', '', '',
                                           'X', 'X', ''])
        assert(test_game.is_main_diagonal_in_danger("X") == [4, 8])
        assert(test_game.is_antidiagonal_in_danger("O") is False)
        assert(test_game.is_antidiagonal_in_danger("X") is False)

class Test_model_functions(unittest.TestCase):
    @mock.patch("OkiPoki.mod_game.models.Game")
    def test_ai_winner_logic(self, mock_game):
        test_game = Game(3, "AI", "Human")
        test_game.game_id = 42
        test_game.your_move = "O"
        test_game.board_blob = json.dumps(['O', '', 'O', 
                                           '', 'X', '', 
                                           '', '', ''])
        assert(play_winning_move(test_game) == 1)

    @mock.patch("OkiPoki.mod_game.models.Game")
    def test_ai_deffensive_logic(self, mock_game):
        test_game = Game(3, "AI", "Human")
        test_game.game_id = 42
        test_game.your_move = "X"
        test_game.board_blob = json.dumps(['O', '', 'O', 
                                           '', 'O', '', 
                                           '', '', ''])
        assert(play_deffensive_move(test_game, "O") == 8)

    @mock.patch("OkiPoki.mod_game.models.Game")
    def test_ai_offensive_logic(self, mock_game):
        test_game = Game(3, "AI", "Human")
        test_game.game_id = 42
        test_game.your_move = "X"
        test_game.board_blob = json.dumps(["O", "X", "X", 
                                           "", "", "O", 
                                           "", "", ""])
        assert(play_offensive_move(test_game) == 4)

if __name__ == '__main__':
    unittest.main()
