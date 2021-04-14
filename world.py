class World:
    def __init__(self, wid):
        self.__id               		   = wid
        self.__stateMatrix                 = []

    def get_id(self):
    	return self.__id

    def add_state(self, state):
    	self.__stateMatrix.append(state)

    def pop_state(self):
    	return self.__stateMatrix.pop(0)

    def isItEnd(self):
    	return len(self.__stateMatrix) == 0
