from state import State

class World:
    def __init__(self, wid):
        self.__id               		   = wid
        self.__stateDict                   = {}

        for x in range(40):
            for y in range(40):
                s = State(x,y)
                index = x*40 + y
                self.__stateDict[index] = s

        print("All states: "+str(len(self.__stateDict)))

    def get_id(self):
    	return self.__id

    def get_state(self, key):
    	return self.__stateDict[key]

    def get_stateDict(self):
        return self.__stateDict

    # to do
    # def isItEnd(self):
    # 	return len(self.__stateDict) == 0
