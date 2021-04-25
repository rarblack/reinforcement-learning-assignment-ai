from connection import Connection
from world import World
from player import Player
from helpers import *
import time

if __name__ == "__main__":

    connection = Connection(api_key='c9426ee5181dca77e9a2', user_id='1055')
    # 1256 1255 1248 1251

    # EARLY SETUP
    world, player = World(id=0), Player(id=1248)

    # resp = connection.get_me_located(teamId)
    # resp = connection.enter_to_world(w.get_id(), p.get_id())
    # print(resp)

    # LEARN
    # learnEnvironment(connection, w, p)
    print(connection.get_my_teams_rl_score(player.get_id()))