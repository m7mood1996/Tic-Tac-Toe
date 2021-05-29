from typing import Sequence
import math
import random

class Player:
    def __init__(self, letter) -> None:
        '''
        letter : is x or o
        '''
        self.letter = letter

    # all player should get their next move given a game
    def get_move(self, game):
        pass

class RandomComputerPlayer(Player):
    def __init__(self, letter) -> None:
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square
        #return super().get_move(game)

class HumanPlayer(Player):
    def __init__(self, letter) -> None:
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8):')
            # checking if the player gives a valid input
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again')
        
        return val
    #return super().get_move(game)
 
class GeniusComputerPlayer(Player):
    def __init__(self, letter) -> None:
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves()) # randomly choose one
        else:
            # get the squre based of the minimax algo
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter
        other_player = '0' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {'position' : None, 
                    'score' : 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() +1)
                    }
        elif not state.empty_squares():
            return {'position' : None,
                    'score' : 0
                    }
        if player == max_player:
            best = {'position': None, 'score' : -math.inf}
        else:
            best = {'position': None, 'score' : math.inf}

        for possible_move in state.available_moves():
            #step 1: make a wmove
            state.make_move(possible_move, player)
            #step2: recurse using minimax to simulate a game after making a move
            sim_score = self.minimax(state, other_player)
            #step 3: undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            #step4: update the dict if necssary
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best