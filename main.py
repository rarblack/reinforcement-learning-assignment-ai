from connection import Connection
from world import World
from player import Player
from helpers import *
import time

if __name__ == "__main__":

    connection = Connection(api_key='c9426ee5181dca77e9a2', user_id='1055')
    # 1256 1255 1248 1251

    # ENTER WORLD
    teamId = 1248
    w = World(0)
    p = Player(teamId)
    # resp = connection.get_me_located(teamId)
    # resp = connection.post_a_world(w.get_id(), p.get_id())
    # print(resp)

    # LEARN
    # learnEnvironment(connection, w, p)
    print(connection.get_my_teams_rl_score(teamId))

    # stateDict = w.get_stateDict()
    # for k in stateDict:
    # # k = 0
    #     st = stateDict[k]
    #     print(st.get_exploredActions())
    #     print(st.getReward())
    #     print("W")
    #     print(st.get_actionQvalue(1))
    #     print("E")
    #     print(st.get_actionQvalue(2))
    #     print("N")
    #     print(st.get_actionQvalue(3))
    #     print("S")
    #     print(st.get_actionQvalue(4))
    #     print("#####################")
    #resp = connection.get_my_team_last_x_runs(1248, 1)
    #print(resp)
    
