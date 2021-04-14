
class State:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__actionsQValue = {}
        self.__exploredActions = []

    left = 1;
    right = 2;
    up = 3;
    down = 4;

    def add_actionQValue(self, action, value):
        self.__actionsQValue[action] = value

    def get_actionQvalue(self, action):
        return self.__actionsQValue[action]

    def get_actionQvalues(self):
        return self.__actionsQValue

    def add_exploredAction(self, action):
        self.__exploredActions.append(action)

    def get_exploredActions(self):
        return self.__exploredActions

    def getReward(self):
        return 1
