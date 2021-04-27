from state import State
from world import World

class Player:
    def __init__(self, id):
        self.__id                  = id
        self.__x                   = 0
        self.__y                   = 0
        self.__current_state       = None

    def get_id(self):
        return self.__id

    def get_currentState(self):
        return self.__current_state

    def set_currentState(self, s):
        self.__current_state = s

    def move(self, connection, w, action):
        actionName = "W"
        if action == 1:
            actionName = "W"
        elif action == 2:
            actionName = "E"
        elif action == 3:
            actionName = "N"
        elif action == 4:
            actionName = "S"

        respond = connection.make_a_move(self.__id, actionName, w.get_id())

        # {'code': 'OK', 'worldId': 0, 'runId': '39', 'reward': -0.1, 'scoreIncrement': -0.1, 'newState': {'x': 0, 'y': '0'}}
        print(f"New State: {respond['newState']}")

        if respond['newState'] != None:
            index = int(respond['newState']['x'])*40 + int(respond['newState']['y'])
            newState = w.get_state(index)   # new state

            self.__current_state = newState
            newState.setReward(respond['reward'])
            print(f"Reward: {respond['reward']}")
        else:
            w.set_isItEnd()
            