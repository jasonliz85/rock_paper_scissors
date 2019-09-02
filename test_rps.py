import unittest
from unittest.mock import patch, MagicMock

from rps import RPS, GameObject, AIPlayer, Hand


class RpsTest(unittest.TestCase):

    def setUp(self):
        self.rps = RPS()
        self.choices = self.rps.choices
        self.rock = self.choices[Hand.R]
        self.paper = self.choices[Hand.P]
        self.scissors = self.choices[Hand.S]

    def test_winner(self):
        '''test the outcomes of each of the game object choices'''
        testCases = [
            (self.rock, self.paper, 'LOSE'),
            (self.rock, self.scissors, 'WIN'),
            (self.rock, self.rock, 'DRAW'),
            (self.paper, self.paper, 'DRAW'),
            (self.paper, self.scissors, 'LOSE'),
            (self.paper, self.rock, 'WIN'),
            (self.scissors, self.paper, 'WIN'),
            (self.scissors, self.scissors, 'DRAW'),
            (self.scissors, self.rock, 'LOSE'),
        ]
        for player_1, player_2, outcome in testCases:
            actual = player_1.winner(player_2)
            self.assertEqual(actual.value, outcome)

    def test_input_args(self):
        testCases = [
            ('1', Hand.R),
            ('2', Hand.P),
            ('3', Hand.S),
            ('0', None),
            ('A', None),
            ('r', 'R'),
            ('s', 'S'),
            ('q', 'Q'),
            ('c', 'C'),
            (1, None),
            (2, None),
            (3, None),
        ]

        for user_input, expected in testCases:
            actual = self.rps.get_turn(user_input)
            self.assertEqual(actual, expected)

    @patch("builtins.input")
    def test_run(self, input_m):
        cases = [
            's', 'q'
        ]

        input_m.side_effects = cases
        # DOESN'T WORK
        # self.rps.run(input_m)


if __name__ == '__main__':
    unittest.main()

