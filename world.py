from state import State

class World:
    def __init__(self, wid):
        self.__id               		   = wid
        self.__stateMatrix                 = []

        for x in range(41):
        	for y in range(41):
        		s = State(x,y)
        		self.__stateMatrix.append(s)

    def get_id(self):
    	return self.__id

    def pop_state(self):
    	return self.__stateMatrix.pop(0)

    def isItEnd(self):
    	return len(self.__stateMatrix) == 0
