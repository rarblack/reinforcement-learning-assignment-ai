from connection import Connection
from world import World
from agent import Agent
from helpers import *
import sys
import time


class Main:
    def __init__(self, connection=['c9426ee5181dca77e9a2','1055']):
        self.__connection       = Connection(*connection)
        self.__world            = None
        self.__found_terminal   = False

    def make_a_fresh_start(self, world_id, agent_id):
        self.__world  = World(world_id, agent=Agent(agent_id))

    def get_world(self):
        return self.__world

    def load_world(self, filename=None):
        if not filename: 
            filename=f'world_{self.__world.get_id()}.pkl'
        self.__world = load_object(filename)

    def save_world(self, filename=None):
        if not filename: 
            filename=f'world_{self.__world.get_id()}.pkl'
        save_object(self.__world, filename)

    def __enter_to_world(self):
        self.__world.enter(self.__connection)

    def get_agent_located(self):
        response = self.__connection.get_me_located(teamId=self.__world.get_agent().get_id())

        # we check whether we are in any world or not
        if response['world'] == -1:
            # if not we enter to a world
            self.__enter_to_world()
            
            # and set agent state to 0 0
            self.__world.update_current_state(self.__world.get_state(('0', '0')))
        else:
            # get current state coordintates from api
            x, y = response['state'].split(':')

            # and set state to the currently gotten one from api
            self.__world.update_current_state(self.__world.get_state((x, y)))

    def training_has_ended(self):
        return self.__world.is_disconnected(self.__connection)

    def prepare_to_train(self):
        self.__found_terminal = False
        self.__world.update_current_state(self.__world.get_state(('0', '0')))
        self.__enter_to_world()

    def train(self, epsolon=0.5):

        # if terminal state is reached then end recursion
        if self.__found_terminal: return None 

        action = epsolon_select_action(self.__world.get_current_state(), epsolon)
                                     
        # make the move on API
        response    = self.__world.get_agent().move(self.__connection, action, self.__world)                      

        if response:

            # check whether we are in the terminal state or not
            if response['newState']:
                new_state_coordinates = list(response['newState'].values())
            else:
                # if it is then turn on terminal flag and set new state to -1 -1 because None value cannot be processed
                self.__found_terminal = True

                # we mark the current state as terminal for latter easy reference
                self.__world.get_current_state().mark_as_terminal()

                # since None value for the next state will create err therefore, we define default value which is a uniquely created state for terminals
                new_state_coordinates = ['terminal', 'terminal']

            # get new state x y coordinates
            x, y = new_state_coordinates

            # get new state and living reward from API response. API has a bug, x and y are returned as different types. we make all str typed
            new_state, living_reward = self.__world.get_state((str(x), str(y))), response['reward']

            # set living rewar to the new state
            new_state.set_living_reward(living_reward)

            # calculate new q value
            new_q_value = calculate_q_value(self.__world.get_current_state(), action, new_state, living_reward) 

            # to visually see, we print current state and neighbors
            self.__world.print_neighbors(action, living_reward, new_state, new_q_value) 

            # update current state q value
            self.__world.get_current_state().update_q_value(action, new_q_value)   
            
            # make the move on local
            self.__world.update_current_state(new_state)                                                                                                

            # save the current world
            self.save_world()

            # wait before next move
            time.sleep(15)                                                                                          

            # continue training until terminal state
            self.train()


if __name__ == "__main__":

    main = Main()
    # 1256 1255 1248 1251
    
    # if you want to start a new world which you have never tried, then uncomment
    # main.make_a_fresh_start(world_id=0, agent_id=1255)

    # if you have trained already in the world and want to improve it, then uncommnet
    main.load_world('world_0.pkl')

    main.get_agent_located()

    # training k times
    for _ in range(1000):
        if main.training_has_ended(): 
            main.prepare_to_train()
        main.train()

    # when all is done re-save
    main.save_world()
    