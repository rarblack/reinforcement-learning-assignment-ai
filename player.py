from state import State
from world import World

class Player:
    def __init__(self, pid):
        self.__id                  = pid
        self.__x                   = 0
        self.__y                   = 0
        self.__currentState        = None

    def get_id(self):
        return self.__id

    def get_currentState(self):
        return self.__currentState

    def set_currentState(self, s):
        self.__currentState = s

    def move(self, connection, w, action):
        resp = connection.post_a_move(self.__id, action)
        # {'code': 'OK', 'worldId': 0, 'runId': '39', 'reward': -0.1, 'scoreIncrement': -0.1, 'newState': {'x': 0, 'y': '0'}}
        index = int(resp['newState']['x'])*40 + int(resp['newState']['y'])
        newState = w.get_state(index)   # new state

        self.__currentState = newState
        newState.setReward(resp['reward'])
            