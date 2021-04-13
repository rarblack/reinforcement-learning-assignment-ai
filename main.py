from connection import Connection
from player import Player
from board import Board
from game import Game
import time

if __name__ == "__main__":

    game = Game(api_key='c9426ee5181dca77e9a2', user_id='1055')
    # 1256 1255

    # use in real gaming
    # game.create(player={'id':1248, 'sign':'O'},  opponent={'id':1251, 'sign':'X'}, board_size=6, target=4)
    game.connect(player={'id':1248, 'sign':'X'}, opponent={'id':1255, 'sign':'O'}, game_id=3087)

    winner = game.start()
    # winner = game.testing(20, 10)

    
    print(f'Game ended at the round {game.get_board().get_round()}')

    if winner:
        print(f'The winner is {winner.get_sign()}')
    else:
        print('There is no winner. Game is tie!')