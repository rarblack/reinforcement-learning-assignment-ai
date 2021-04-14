from state import State

class Player:
    def __init__(self):
        self.__x                   = 0
        self.__y                   = 0
        self.__currentState        = State(x,y)

    def get_currentState(self):
        return self.__currentState

    def set_currentState(self, s):
        self.__currentState = s

    def move(self):
        self.__currentState = newState
    