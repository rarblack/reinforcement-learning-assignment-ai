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
def epsolon_select_action(state, e, limit):
    n = random.uniform(0, 1)

    action = state.get_max_action()

    if n < e:
        actions = list(filter(lambda a: state.get_action_usage_count(a) < limit, state.get_actions().keys()))
        if actions:
            action = random.choice(actions)

    # state.increase_action_usage_count(action)

    return action


import pickle
def save_object(object, filename):
    file = open(filename, 'wb')
    pickle.dump(object, file, pickle.HIGHEST_PROTOCOL)

def load_object(filename):
    file = open(filename, 'rb')
    return pickle.load(file)


from world import World
from state import State
from agent import Agent

def get_restructured_world(old_world, new_agent):
    if new_agent:
        world = World(old_world.get_id(), Agent(new_agent))
    else:
        world = World(old_world.get_id(), Agent(old_world.get_agent().get_id()))

    world.update_current_state(old_world.get_current_state())
    
    new_states = {}

    for i in map(str, range(40)):
        for j in map(str, range(40)):
            old_state   = old_world.get_state((i, j))
            new_state   = State(i, j)

            new_state.set_q_values(old_state.get_q_values())
            
            new_state.set_actions(old_state.get_actions())

            new_state.set_living_reward(old_state.get_living_reward())
            
            if old_state.is_terminal(): 
                new_state.mark_as_terminal()
            new_states[(i, j)] = new_state

    new_states[('terminal', 'terminal')] = State('terminal', 'terminal')

    world.set_states(new_states)
    return world