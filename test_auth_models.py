import unittest
from unittest import mock
from OkiPoki.mod_auth.models import Player, get_player_by_name

class Test_test_auth_models(unittest.TestCase):
    def test_new_player(self):
        test_player = Player("tester", "passwd")
        assert(test_player.name == "tester")

    @mock.patch("OkiPoki.mod_auth.models.Player")
    def test_get_player_by_nameid(self, mock_user):
        test_player = Player("Johnny", "DoeIsPass")
        mock_user.query.filter_by.return_value.first.return_value = test_player
        assert(get_player_by_name("Johnny") == test_player)

    def test_add_wins_to_winner_standing(self):
        test_player = Player("tester", "passwd")
        test_player.wins = 4 # old wins standings
        assert(test_player.add_win() == 5) 

if __name__ == '__main__':
    unittest.main()
