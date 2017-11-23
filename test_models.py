import unittest, json
from unittest import mock
from OkiPoki.players import Player
from OkiPoki.games import Game, get_game

class Test_test_model_player(unittest.TestCase):
    @mock.patch("OkiPoki.players.Player")
    def test_new_player(self, mock_player):
        test_player = Player("tester", "passwd")
        assert(test_player.name == "tester")

    @mock.patch("OkiPoki.players.Player")
    def test_add_wins(self, mock_player):
        test_player = Player("tester", "passwd")
        test_player.wins = 4
        assert(test_player.add_win() == 5)

class Test_model_game(unittest.TestCase):
    @mock.patch("OkiPoki.games.Game")
    def test_get_game(self, mock_game):
        test_new_game = Game(3, "playerX", "playerO")
        #test_new_game.game_id = 0
        test_new_game.board_size = 3
        test_new_game.player_x = "playerX"
        test_new_game.player_o = "playerO"
        test_new_game.your_move = "X"
        test_new_game.board_blob = json.dumps(['', '', 'X'])
        mock_game.query.filter_by.return_value.first.return_value = test_new_game
        assert(get_game(0) == test_new_game)
        assert(test_new_game.update_board(1, 'X') == True)

    @mock.patch("OkiPoki.games.Game")
    def test_won_column_or_row(self, mock_game):
        test_game = Game(3, "playerX", "playerO")
        test_game.game_id = 1
        test_game.board_size = 3
        test_game.player_x = "playerX"
        test_game.player_o = "playerO"
        test_game.your_move = "X"
        test_game.board_blob = json.dumps(['X', 'X', 'X', 'X', '', 'O', 'X', 'O', ''])
        assert(test_game.is_row_won(0, 'X') == True)
        assert(test_game.is_row_won(1, 'O') == False)
        assert(test_game.is_row_won(2, 'O') == False)
        assert(test_game.is_row_won(2, 'X') == False)
        assert(test_game.is_column_won(0, test_game.your_move) == True)
        assert(test_game.is_column_won(1, 'O') == False)
        assert(test_game.is_column_won(2, 'X') == False)

    @mock.patch("OkiPoki.games.Game")
    def test_won_diagonal(self, mock_game):
        test_game = Game(3, "playerX", "playerO")
        test_game.game_id = 1001
        test_game.board_size = 3
        test_game.your_move = "O"
        test_game.board_blob = json.dumps(['O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', ''])
        assert(test_game.is_main_diagonal_won(test_game.your_move) == False)
        assert(test_game.is_antidiagonal_won(test_game.your_move) == True)

    @mock.patch("OkiPoki.games.Game")
    def test_danger(self, mock_game):
        test_game = Game(3, "playerX", "playerO")
        test_game.game_id = 1002
        test_game.board_size = 3
        test_game.your_move = "X"
        test_game.board_blob = json.dumps(['X', '', 'O', 'X', '', '', 'X', 'X', ''])
        assert(test_game.is_row_in_danger(0, "X") == False)
        assert(test_game.is_row_in_danger(1, "X") == [4, 5])
        assert(test_game.is_row_in_danger(2, "X") == [8])
        assert(test_game.is_column_in_danger(0, "X") == [])
        assert(test_game.is_main_diagonal_in_danger("X") == [4, 8])
        assert(test_game.is_antidiagonal_in_danger("O") == False)
        assert(test_game.is_antidiagonal_in_danger("X") == False)

if __name__ == '__main__':
    unittest.main()
