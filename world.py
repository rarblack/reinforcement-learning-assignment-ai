from state import State

class World:
    def __init__(self, id):
        self.__id           = id
        self.__states       = {}
        self.__is_terminal  = False
        
        self.__generate_state()

    def get_id(self):
    	return self.__id

    def get_state(self, key):
    	return self.__states[key]

    def get_stateDict(self):
        return self.__states

    def set_isItEnd(self):
        self.__is_terminal = True

    def get_isItEnd(self):
        return self.__is_terminal

    def __generate_state(self,):
        for x in range(40):
            for y in range(40):
                index = 40 * x + y
                self.__states[index] = State(x, y)

        print(f"All states: {len(self.__states)}")
