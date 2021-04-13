from functools import reduce
from square import Square
from helpers import *

class Board:
    def __init__(self, size, target):
        self.__size                 = size
        self.__moves                = []
        self.__round                = 0
        self.__winner               = None
        self.__target               = target
        self.__squares              = {(x, y): Square(x, y) for x in range(size) for y in range(size)}
        self.__compute_terminals()
        print(f'Board sized {size} with target {target} is set.')


    # PRIVATE METHODS
    def __compute_terminals(self):

        size                = self.__size
        target              = self.__target
        squares             = self.__squares

        # number of terminal states: size - target + 1 and +1 for upperbound
        num_of_terminals    = size - target + 1

        def set_to_squares(terminal):
            terminal = [squares[position] for position in terminal]
            for square in terminal: square.add_terminal(terminal)


        for i in range(size):
            for j in range(num_of_terminals):
                terminal_vertical   = []
                terminal_horizontal = []
                for k in range(j, target + j):
                    terminal_horizontal.append((i, k))
                    terminal_vertical.append((k, i))
                set_to_squares(terminal_horizontal)
                set_to_squares(terminal_vertical)


        for i in range(num_of_terminals):
            for j in range(num_of_terminals):
                terminal_diagonal_left   = []
                terminal_diagonal_right  = []
                x, y = i, j
                for _ in range(target):
                    terminal_diagonal_left.append((x, y))
                    terminal_diagonal_right.append((x, size - y - 1))
                    x += 1
                    y += 1
                set_to_squares(terminal_diagonal_left)
                set_to_squares(terminal_diagonal_right)

        print(f'Terminals calculated')
      

    # PUBLIC METHODS
    def set_move(self, move, player):
        move.set_assignee(player)
        self.__moves.append(move)
    
    def record_round(self):
        self.__round = len(self.__moves)

    def get_size(self):
        return self.__size
    
    def get_target(self):
        return self.__target
    
    def get_move(self, move):
        return self.__squares[move]

    def get_round(self):
        return self.__round

    def get_moves(self):
        return self.__moves

    def get_latest_move(self):
        return self.__moves[-1]
    
    def get_empty_squares(self, sort=False, desc=False):
        if sort:
            lsort= sorted(list(filter(lambda x: x.is_empty(), self.__squares.values())), key=lambda x: x.get_score(), reverse=desc)
            return lsort
        return list(filter(lambda x: x.is_empty(), self.__squares.values()))

    def has_moves(self, enough=None):
        if enough:
            return len(self.__moves) >= self.__target
        return not len(self.__moves[self.__round:]) == 0

    def is_full(self):
        return (self.__size ** 2) - len(self.__moves) == 0

    def is_terminal(self):
        for terminal in self.get_latest_move().get_terminals(): 
            terminal = [square.get_assignee() for square in terminal]
            if len(list(filter(lambda a: not a == terminal[0], terminal))) == 0:
                    return True
        return False
 
    def undo(self, move):
        move.reset()
        self.__moves.pop()

    def update_terminals(self, player, opponent):
        for square in self.get_empty_squares():
            terminals = square.get_terminals()
            for index, terminal in enumerate(terminals):
                cplayer, copponent =  [0] * 2
                for cell in terminal:
                    if cell.get_assignee() is player: 
                        cplayer += 1
                    elif cell.get_assignee() is opponent: 
                        copponent += 1
                    if cplayer and copponent: break
                if cplayer and copponent: del terminals[index]
        
        self.__calculate_square_scores(player, opponent)

    def __calculate_square_scores(self, player, opponent):
        for square in self.get_empty_squares():
            square.clear_score()
            terminals = square.get_terminals()
            for terminal in terminals:
                score    = 0
                count    = 0
                cfilled  = 0
                assignee = None
                # for cell in terminal:                
                #     if cell.is_empty():
                #         if count:
                #             if assignee is player:
                #                 score += (10.1 ** count)
                #             elif assignee is opponent:
                #                 score += (10 ** count)
                #             count = 0
                #     else:
                #         assignee = cell.get_assignee()
                #         count += 1
                # score += 1 * len(terminal) - cfilled
                # square.add_score(score) 
                for cell in terminal:                
                    if cell.is_empty(): count += 1
                    else: assignee = cell.get_assignee()
                score += count
                diff = len(terminal) - count
                if diff: score += 11 ** diff if assignee is player else 10 ** diff
                square.add_score(score) 
                
    def sketch_board(self):
        board   = self.__squares
        cnames  = [f'{i%10}' for i in range(self.__size)]
        print('  ' + '|'.join(cnames) + '|')
        for i in range(self.__size):
            print(f'{i%10}|', end='')
            for j in range(self.__size):
                print(f'{board[(i,j)].get_assignee().get_sign() if board[(i,j)].get_assignee() else "."}|', end='')
            print()

    def sketch_board_scores(self):
        board = self.__squares
        for i in range(self.__size):
            for j in range(self.__size):
                print(f'{board[(i,j)].get_score()}|', end='')
            print()