from copy import deepcopy

class AlphaBetaSearch:

    def __init__(self, board):
        self.state = board

    def terminal_test(self):
        if self.state.has_moves(enough=True): 
            if self.state.is_terminal() : return True
            if self.state.is_full()     : return True
        return False

    def __switch_players(self, player, opponent):
        return opponent, player

    def __utility(self):
        return self.state.get_latest_move().get_score()

    def __max_value(self, depth, player, opponent, alpha, beta):

        best_score, best_move = float("-inf"), None

        if not depth or self.terminal_test(): return self.__utility()

        for move in self.state.get_empty_squares(sort=True, desc=True)[:1]:

            self.state.set_move(move, player)

            self.state.update_terminals(player, opponent)

            previous_best_score, best_score = best_score, max(best_score, self.__min_value(depth - 1, *self.__switch_players(player, opponent), alpha, beta))

            if not previous_best_score == best_score: best_move = move

            if best_score >= beta: alpha = max(alpha, best_score)

            self.state.undo(move)

        if self.state.has_moves(): return best_score

        return best_move


    def __min_value(self, depth, player, opponent, alpha, beta):

        worst_score, worst_move = float("inf"), None

        if not depth or self.terminal_test(): return self.__utility()

        for move in self.state.get_empty_squares(sort=True, desc=True)[:1]:
            
            self.state.set_move(move, player)
            
            self.state.update_terminals(player, opponent)

            previous_worst_score, worst_score = worst_score, min(worst_score, self.__max_value(depth - 1, *self.__switch_players(player, opponent), alpha, beta))
            
            if not previous_worst_score == worst_score: worst_move = move

            if worst_score <= alpha: beta = min(beta, worst_score)

            self.state.undo(move)

        if self.state.has_moves(): return worst_score

        return worst_move
        
        
    def start(self, player, opponent):
        return self.__max_value(depth=1, player=player, opponent=opponent, alpha=float('-inf'), beta=float('inf'))