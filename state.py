class State:
    def __init__(self, x, y):
        self.__x                = x
        self.__y                = y
        self.__q_values         = {'W': 0, 'N': 0, 'E': 0, 'S': 0}
        self.__actions          = {'W': 0, 'N': 0, 'E': 0, 'S': 0}
        self.__living_reward    = None
        self.__is_terminal      = False

    def update_q_value(self, action, value):
        # for terminal state we need all actions to have same values
        if self.__is_terminal:
            for action in self.__actions:
                self.__q_values[action] = value
        else:
            self.__q_values[action] = value

    def get_q_value(self, action):
        return self.__q_values[action]
    
    def set_living_reward(self, reward):
        self.__living_reward = reward

    def get_living_reward(self):
        return self.__living_reward

    def get_coordinates(self):
        return (self.__x, self.__y)

    def get_action_usage_count(self, action):
        return self.__actions[action]

    def increase_action_usage_count(self, action):
        self.__actions[action] += 1

    def set_q_values(self, new_q_values):
        self.__q_values = new_q_values

    def get_q_values(self):
        return self.__q_values

    def mark_as_terminal(self):
        self.__is_terminal = True

    def set_actions(self, actions):
        self.__actions = actions

    def get_actions(self):
        return self.__actions

    def get_max_q_value(self):
        return self.__q_values[max(self.__q_values, key=lambda action: self.__q_values[action])]

    def get_max_action(self):
        return max(self.__q_values, key=lambda action: self.__q_values[action])

    def is_terminal(self):
        return self.__is_terminal
        
    def __str__(self):
        return f"State coordinates: {self.__x}, {self.__y}\n \
                 State Q Values:    {self.__q_values}\n"
