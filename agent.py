
class Agent:
    def __init__(self, id):
        self.__id = id

    def get_id(self):
        return self.__id

    def move(self, connection, action, world):
        return connection.make_a_move(teamId=self.__id, move=action, worldId=world.get_id())