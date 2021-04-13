class Player:
    def __init__(self, id, sign, opponent=False):
        self.__id                  = id
        self.__sign                = sign
        self.__is_opponent         = opponent
        print(f'Player is set with {id} id and {sign.upper()} sign.')

    def get_id(self):
        return self.__id

    def get_sign(self):
        return self.__sign

    def is_opponent(self):
        return self.__is_opponent