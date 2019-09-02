from enum import Enum
import random
import logging

logger = logging.getLogger(__name__)

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
        '''
        Logic used to determine who the winner is. Each class instance has a list to determine who it can win (beat)
        or defeat (loses). It compares itself with another class instance.
        '''
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


class AIPlayer(object):
    '''
    Use this class to capture the AI player - At some point, this can be used to add more intelligence.
    i.e. possibly use ML techniques
    '''
    def __init__(self, choices):
        self.history = []
        self.choices = choices

    def get_next_choice(self):
        return random.choice(self.choices)


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
        self.player_ai = AIPlayer(list(self.choices.keys()))
        self._reset_history()

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

    def get_ai_choice(self):
        ''' Use the ai object to get the next choice'''
        return self.player_ai.get_next_choice()

    def get_human_choice(self, choice):
        ''' Ask for input from the user to determine their choice'''
        logger.info('You selected {0}'.format(choice))

        if not isinstance(choice, str):
            return

        if choice.upper() in ['C', 'Q', 'R', 'S']:
            return choice.upper()
        elif choice.upper() in ['1', '2', '3']:
            choice = int(choice)
            return list(self.choices.keys())[choice-1]

    def run(self):
        ''' Start the game'''

        ## print the rules
        logger.info(RULES)

        while(True):

            ## get the human choice
            choice = self.get_human_choice(input('Select a Rock[1], Paper[2], Scissors[3], Quit[Q], Reset[R], Stats[S]:\n'))

            ## ensure choices are dealt with
            if not choice:
                logger.info('Did not recognise this choice, try again')
            if choice in ['C', 'Q']:
                logger.info('Quitting game. Goodbye')
                break
            if choice in ['S']:
                self.print_stats()
                continue
            if choice in ['R']:
                logger.info('Resetting the game')
                self._reset_history()
                continue
            if choice not in self.choices.keys():
                logger.error('Not a recognised selection, please try again')
                continue

            ## grab rock, paper or scissors for each player
            player_1 = self.choices[choice]
            player_2 = self.choices[self.get_ai_choice()]
            logger.info('You chose: {}, AI chose: {}'.format(player_1.name, player_2.name))

            ## now get the results
            result = player_1.winner(player_1)
            logger.info('Results: You {}'.format(result.value))

            ## log outcome for
            self.log_outcome(player_1, player_2, result)


if __name__ == '__main__':

    RPS().run()
