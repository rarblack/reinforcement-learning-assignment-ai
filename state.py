class State:
    W = 1;
    E = 2;
    N = 3;
    S = 4;

    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__reward = 0
        self.__actionsQValue = {State.W: 0, State.E: 0, State.N: 0, State.S: 0} # float("-inf") ??
        self.__exploredActions = []

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

    def setReward(self, r):
        self.__reward = float(r)

    def getReward(self):
        return self.__reward

    def print(self):
        print("State coordinates: "+str(self.__x)+", "+str(self.__y))
        print(self.__actionsQValue)
