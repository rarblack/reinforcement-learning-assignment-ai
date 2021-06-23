from connection import Connection
from state import State
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

    def create_a_team(self, name):
        return self.__connection.create_a_team(name)

    def add_a_member_to_team(self, team_id, user_id):
        return self.__connection.add_a_member(team_id, user_id)

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
        print(f'MY LOCATION: {response}')
        # we check whether we are in any world or not
        if response['world'] == '-1':
            # if not we enter to a world
            self.__enter_to_world()
            
            # and set agent state to 0 0
            self.__world.update_current_state(self.__world.get_state(('0', '0')))
        else:
            # get current state coordintates from api
            x, y = response['state'].split(':')

            # and set state to the currently gotten one from api
            self.__world.update_current_state(self.__world.get_state((x, y)))
    
    def apply_new_structure_to_world(self, new_agent=None):
        self.__world = get_restructured_world(self.__world, new_agent)
        self.save_world()

    def print_score(self):
        print(f'Score: {self.__connection.get_my_teams_rl_score(self.__world.get_agent().get_id())["score"]}')

    def print_terminal_states(self):
        terminal_states = list(filter(lambda x: x.is_terminal(), self.__world.get_states().values()))

        if terminal_states:
            for terminal in terminal_states:
                print(f'{terminal.get_coordinates()} - {terminal.get_q_values()}')
        else:
            print("There is no any found terminal states, yet.")

    def print_unvisited_states(self):
        unvisited_states = list(filter(lambda state: not any(state.get_q_values().values()), self.__world.get_states().values()))

        if unvisited_states:
            print(f'Count of unvisited states: {len(unvisited_states)}')
            if (input('Type y to see the states: ') == 'y'):
                for state in unvisited_states:
                    print(state.get_coordinates())
        else:
            print("All states has been visited!")


    def train(self, epsolon=0.5, manually=False, direction=None, visit_limit=5):

        # if terminal state is reached then end recursion
        if self.__found_terminal: return None 

        if direction:
            action = direction
        elif manually:
            print(self.__world.get_current_state().get_coordinates())
            action = input('Choose any of the 4 actions: W N E S:\n')
        else:
            action = epsolon_select_action(self.__world.get_current_state(), epsolon, visit_limit)
                                     
        # make the move on API
        response    = self.__world.get_agent().move(self.__connection, action, self.__world)                      

        print(f'MOVE ON API: {response}')
        if response:

            # check whether we are in the terminal state or not
            if response['newState']:
                new_state_coordinates       = list(response['newState'].values())

                # we need to find what direction actually agent went and increase amount
                current_state_coordinates   = self.__world.get_current_state().get_coordinates()

                state_differences           =  (int(new_state_coordinates[0]) - int(current_state_coordinates[0]), int(new_state_coordinates[1]) - int(current_state_coordinates[1]))

                if state_differences == (-1, 0):
                    action = 'W'
                elif state_differences == (0, 1):
                    action = 'N'
                elif state_differences == (1, 0):
                    action = 'E'    
                elif state_differences == (0, -1):
                    action = 'S'
                self.__world.get_current_state().increase_action_usage_count(action)
            else:
                # if it is then turn on terminal flag and set new state to -1 -1 because None value cannot be processed
                self.__found_terminal = True

                # we mark the current state as terminal for latter easy reference
                self.__world.get_current_state().mark_as_terminal()

                # Terminal state
                print(f'Terminal State: {self.__world.get_current_state().get_coordinates()}')

                # since None value for the next state will create err therefore, we define default value which is a uniquely created state for terminals
                new_state_coordinates = ['terminal', 'terminal']

            # get new state x y coordinates
            x, y = new_state_coordinates

            # get new state and living reward from API response. API has a bug, x and y are returned as different types. we make all str typed
            new_state, living_reward = self.__world.get_state((str(x), str(y))), response['reward']

            # set living rewar to the new state
            self.__world.get_current_state().set_living_reward(living_reward)

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
            self.train(epsolon, manually, direction, visit_limit)


if __name__ == "__main__":

    main = Main()
    # 1256 1255 1248 1251

    # if you want to start a new world which you have never tried, then uncomment
    # main.make_a_fresh_start(world_id=4, agent_id=1248)

    # if you have trained already in the world and want to improve it, then uncommnet
    main.load_world('world_9.pkl')

    # if there is any change in the structure this should be run and the pkl will be updated
    # main.apply_new_structure_to_world(new_agent=1248)

    # print(main.get_world().get_state(('20', '30')).get_q_values())

    main.print_score()
    main.print_terminal_states()
    # main.print_unvisited_states()

    # training k times
    k = 1
    for _ in range(k):
        main.get_agent_located()
        main.train(epsolon=0, manually=False, direction=None, visit_limit=10)