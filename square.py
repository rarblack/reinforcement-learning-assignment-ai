class Square:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__terminals = []
        self.__assignee  = None
        self.__score     = 0

    def add_terminal(self, terminal):
        self.__terminals.append(terminal)
    
    def add_score(self, score):
        self.__score += score

    def set_assignee(self, player):
        self.__assignee = player

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y
        
    def get_score(self):
        return self.__score

    def get_assignee(self):
        return self.__assignee

    def get_terminals(self):
        return self.__terminals

    def get_position(self):
        return (self.__x, self.__y)

    def clear_score(self):
        self.__score = 0
    
    def reset(self):
        self.__assignee = None
        self.__score    = 0
        
    def is_empty(self):
        return self.__assignee == None
