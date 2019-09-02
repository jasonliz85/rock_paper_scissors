from enum import Enum
import random
import logging

logger = logging.getLogger(__name__)
logging.root.setLevel(logging.DEBUG)


RULES = '''
Welcome to the rock paper scissors game.
The rules:
    Paper beats (wraps) Rock
    Rock beats (blunts) Scissors
    Scissors beats (cuts) Paper.
    You are playing against a computer
    To select an object, please choose:
        Rock [1], Paper [2] or Scissors [3],
    To restart history [R], to exit [C] or [Q] and [S] for stats
'''


class Hand(Enum):
    R = 'ROCK'
    P = 'PAPER'
    S = 'SCISSORS'


class Outcomes(Enum):
    W = 'WIN'
    D = 'DRAW'
    L = 'LOSE'


class GameObject(object):

    def __init__(self, name, beats=None, loses=None):
        self._name = name
        self.beats = beats
        self.loses = loses

    def __repr__(self):
        return '<{} beats={}, loses={}>'.format(self.name, self.beats, self.loses)

    def winner(self, other):
        '''Compare this with another instance to determine who wins'''

        if other._name == self._name:
            logger.debug('{} draws with {}'.format(other.name, self.name))
            return Outcomes.D
        elif other._name in self.beats:
            logger.debug('{} beats {}'.format(self.name, other.name))
            return Outcomes.W
        elif other._name in self.loses:
            logger.debug('{} loses to {}'.format(other.name, self.name))
            return Outcomes.L

        msg = 'Something went wrong, we shouldn\'t get here', self.name, other.name, self.beats, self.loses
        raise Exception(msg)

    @property
    def name(self):
        '''As _name is an Enum, return the value'''
        return self._name.value


class Player(object):
    def __init__(self, choices):
        self.choices = choices

    def get_next_turn(self, choice):
        logger.info('You selected {0}'.format(choice))
        return self.choices[choice]


class AIPlayer(Player):
    '''
    Use this class to capture the AI player - At some point, this can be used to
    add more intelligence. i.e. possibly use ML techniques
    '''
    def get_next_turn(self):
        return random.choice(list(self.choices.values()))


def user_input():
    return input('Select a Rock[1], Paper[2], Scissors[3], Quit[Q], Reset[R], Stats[S]:\n')


class RPS(object):
    '''
    RPS class used to capture the play workflow.
    '''
    def __init__(self):
        self.choices = {
            Hand.R: GameObject(Hand.R, beats=(Hand.S,), loses=(Hand.P,)),
            Hand.P: GameObject(Hand.P, beats=(Hand.R,), loses=(Hand.S,)),
            Hand.S: GameObject(Hand.S, beats=(Hand.P,), loses=(Hand.R,))
        }
        self.player_1 = Player(self.choices)
        self.player_2 = AIPlayer(self.choices)
        self.history = []

    def _reset_history(self):
        ''' reset the history object'''
        self.history = []

    def log_outcome(self, player_1_choice, player_2_choice, result):
        '''
        Record the outcome of each play.
        __future__ -> log to a database and data structure that is better at handling stats (e.g. pandas)
        '''
        self.history.append((player_1_choice, player_2_choice, result))

    def print_stats(self):
        ''' Print the stats'''
        logger.info(self.history)

    def get_turn(self, choice):
        ''' Ask for input from the user to determine their choice'''
        logger.info('You selected {0}'.format(choice))

        if not isinstance(choice, str):
            return

        if choice.upper() in ['C', 'Q', 'R', 'S']:
            return choice.upper()

        # maybe make this r, p or s and the choices above 1-4?
        elif choice.upper() in ['1', '2', '3']:
            choice = int(choice)
            return list(self.choices.keys())[choice-1]

    def run(self):
        ''' Start the game'''

        ## print the rules
        logger.info(RULES)

        while(True):

            ## get the player choice
            choice = self.get_turn(user_input())

            ## ensure choices are dealt with
            if not choice:
                logger.info('Did not recognise this choice, try again')
            if choice in ['c', 'C', 'q', 'Q']:
                logger.info('Quitting game. Goodbye')
                break
            if choice in ['s', 'S']:
                self.print_stats()
                continue
            if choice in ['r', 'R']:
                logger.info('Resetting the game')
                self._reset_history()
                continue
            if choice not in self.choices:
                logger.error('Not a recognised selection, please try again')
                continue

            ## grab rock, paper or scissors for each player
            p1_turn = self.player_1.get_next_turn(choice)
            p2_turn = self.player_2.get_next_turn()
            logger.info('You chose: {}, opponent chose: {}'.format(
                p1_turn.name, p2_turn.name
            ))

            ## now get the results
            result = p1_turn.winner(p2_turn)
            logger.info('Results: You {}'.format(result.value))

            ## log outcome for
            self.log_outcome(p1_turn, p2_turn, result)


if __name__ == '__main__':

    RPS().run()
