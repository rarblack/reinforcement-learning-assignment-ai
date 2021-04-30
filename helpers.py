def calculate_q_value(state, action, new_state, reward):
    """
    Update Q-value of a given state

    state - the state for which Q-value will be Ndated
    action - the action taken on the state
    new_state - the state on which the robot will land
    reward  - the living reward of the current state
    """
    alpha, gamma = 0.1, 0.9

    return (1 - alpha) * state.get_q_value(action) + alpha * (reward + gamma * new_state.get_max_q_value())

import random
def epsolon_select_action(state, e):
    n = random.uniform(0, 1)

    if n < e:
        return random.choice(state.get_actions())
    return state.get_max_action()


import pickle
def save_object(object, filename):
    file = open(filename, 'wb')
    pickle.dump(object, file, pickle.HIGHEST_PROTOCOL)

def load_object(filename):
    file = open(filename, 'rb')
    return pickle.load(file)