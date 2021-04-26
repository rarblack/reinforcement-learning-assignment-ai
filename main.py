from connection import Connection
from world import World
from player import Player
from helpers import *
import time
import os.path

def loadQvalues(world):
    fileName = str(world.get_id())+".txt"
    if os.path.isfile(fileName):
        print ("World information is found.")
        f = open(fileName, "r")
        lines = f.readlines()

        for line in lines:
            info = line.split("State:")[1].strip()
            if (len(info.split("{")) > 1):
                # Fetch state
                stId = int(info.split("{")[0].strip())
                state = world.get_state(stId)

                Qinfo = (info.split("{")[1][0:-1]).strip().split(",") # delete last symbols
                for comp in Qinfo:
                    action = int(comp.split(" ")[0].strip())
                    value = float(comp.split(" ")[1].strip())
                    state.add_actionQValue(action, value)
                    state.add_exploredAction(action)
        f.close()
    else:
        print ("World information has not been found.")

def storeQvalues(world):
    fileName = str(world.get_id())+".txt"
    f = open(fileName, "w")
    
    stateDict = world.get_stateDict()
    for k in stateDict:
        state = stateDict[k]
        f.write("State: "+str(k))
        exploredActions = state.get_exploredActions()
        f.write("{")
        for a in exploredActions:
            f.write(str(a)+" "+str(state.get_actionQvalue(a))+",")
        f.write("}")

    f.close()

if __name__ == "__main__":

    connection = Connection(api_key='c9426ee5181dca77e9a2', user_id='1055')
    # 1256 1255 1248 1251

    # EARLY SETUP
    world, player = World(id=0), Player(id=1248)
    resp = connection.get_me_located(player.get_id())
    # respond = connection.enter_to_world(world.get_id(), player.get_id())
    # print(respond)

    # LEARN
    loadQvalues(world)
    # stateDict = world.get_stateDict()
    # for k in stateDict:
    #     st = stateDict[k]
    #     print(st.get_exploredActions())
    #     print("W")
    #     print(st.get_actionQvalue(1))
    #     print("E")
    #     print(st.get_actionQvalue(2))
    #     print("N")
    #     print(st.get_actionQvalue(3))
    #     print("S")
    #     print(st.get_actionQvalue(4))

    learnEnvironment(connection, world, player)
    print(connection.get_my_teams_rl_score(player.get_id()))
    print(connection.get_me_located(teamId=player.get_id()))
    storeQvalues(world)