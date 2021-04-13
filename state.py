final left = 1;
final right = 2;
final up = 3;
final down = 4;

class State:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__actionsQValue = {}
        self.__exploredActions = []

    def add_action(self, action, value):
        self.__actionsQValue[action] = value

    def get_Qvalue(self, action):
        return self.__actionsQValue[action]
