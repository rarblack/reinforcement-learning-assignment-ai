from state import State

class World:
    def __init__(self, id, agent):
        self.__id               = id
        self.__states           = self.generate_states()
        self.__current_state    = None
        self.__agent            = agent

    def update_current_state(self, state):
        self.__current_state = state

    def get_id(self):
    	return self.__id

    def set_states(self, states):
        self.__states = states

    def get_states(self):
        return self.__states

    def get_state(self, key):
    	return self.__states[key]

    def get_current_state(self):
        return self.__current_state

    def get_agent(self):
        return self.__agent

    def enter(self, connection):
        connection.enter_to_world(self.__id, self.__agent.get_id())        

    def generate_states(self):
        states = {(str(x), str(y)): State(str(x), str(y)) for x in range(40) for y in range(40)}

        # for terminal states, because api return none as a new state
        states[('terminal', 'terminal')] = State('terminal', 'terminal')
        return states

    def print_neighbors(self, action, reward, next_state, new_q_value):
        print(''.center(45, '+'))
        for i in [-1, 0, 1]:
            for j in [1, 0, -1]:
                try:
                    # we only need to have 5 states like a plus sign
                    if all([i,j]): raise

                    x, y = self.__current_state.get_coordinates()

                    # find neighbors
                    x, y = (str(int(x) + i), str(int(y) + j))

                    state = self.get_state((x, y))
                except:
                    continue
                
                print(''.center(25, '-'))

                # to detect correct labeling
                if state == self.__current_state: 
                    print('CURRENT STATE')
                    print(f'ACTION: {action}')
                    print(f'NEW Q VALUE: {new_q_value}')
                    print(f'ACTIONS: {state.get_actions()}')
                    print(f'LIVING REWARD: {reward}')
                elif state == next_state: print('NEXT STATE')
                else: print('STATE')

                print(f'COORDINATES: {state.get_coordinates()}')

                # print 4 action q values
                print(f"{str(round(state.get_q_value('N'), 5))}".center(25, ' '))
                print(f"{round(state.get_q_value('W'), 5)}+++++{round(state.get_q_value('E'), 5)}".center(25, ' '))
                print(f"{round(state.get_q_value('S'), 5)}".center(25, ' '))

                print(''.center(25, '-'))
            print(''.center(35, '-'))
        print(''.center(45, '+'))


    def extract_policy(self):
        pass

    def is_disconnected(self, connection):
        """
        Here we check whether local world has connected to API world or not
        """
        return connection.get_me_located(teamId=self.__agent.get_id())['world'] == '-1'
