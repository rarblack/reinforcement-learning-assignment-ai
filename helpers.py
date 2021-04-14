import random
from state import State

def increase(variable, amount=1):
    variable += amount

def decrease(variable, amount=1):
    variable -= amount

def fib(n):    # write Fibonacci series up to n
    a, b = 0, 1
    while a < n:
        a, b = b, a + b

    return b

def parse_board_string(string):
    moves = {}
    splitted = string.split('\n')
    size  = len(splitted[0])

    for x, row in enumerate(splitted):
        for y, sign in enumerate(row):
            if not sign.__eq__('-'): 
                moves[(x,y)] = sign

    return (size, moves)

alpha = 0.1;
gamma = 0.9
stateMatrix = [] #store all explored states

'''
Update Q-value of a given state

@param s - the state for which Q-value will be updated
@param action - the action taken on the state
@param nextState - the state on which the robot will land
'''
def updateQ(State s, int action, State nextState):
    #the FORMULA of Q-learning updates
    value = (1 - alpha) * s.get_actionQvalue(action) + alpha * (nextState.getReward(s) + gamma * getMaxQ(nextState));

    if (action == State.left):
        s.add_actionQValue(State.left, value)
        if (State.left not in s.get_exploredActions()):
            s.add_exploredAction(State.left)
        
    elif (action == State.right):
        s.add_actionQValue(State.right, value)
        if (State.right not in s.get_exploredActions()):
            s.add_exploredAction(State.right)
        
    elif (action == State.up):
        s.add_actionQValue(State.up, value)
        if (State.up not in s.get_exploredActions()):
            s.add_exploredAction(State.up)
        
    elif (action == State.down):
        s.add_actionQValue(State.down, value)
        if (State.up not in s.get_exploredActions()):
            s.add_exploredAction(State.up)

'''
Get maximum Q-value of a given state

@param s - the state for which max Q-value will be found
'''
def getMaxQ(State s):
    maxQ = max(s.get_actionQvalue(State.left), 
                max(s.get_actionQvalue(State.right), 
                max(s.get_actionQvalue(State.up), s.get_actionQvalue(State.down))));
    return maxQ
    
    
'''
Get action for a given state

@param s - the state for which action will be found

'''
def getAction(State s):
    int action = 0;
    possibleActions = []

    for i in range(1,4):
        if (i is not in s.get_exploredActions()):
            possibleActions.append(i)
    
    if (len(possibleActions) > 0):
        action = random.choice(possibleActions)
    else:
        action = getPolicy(s)

    return action

    
'''
Get policy of a given state

@param s - the state for which policy will be found

'''
def getPolicy(State s):
    action = State.left
    maxV = getMaxQ(s)

    if (maxV == s.get_actionQvalue(State.left)):
        action = State.left
    elif (maxV == s.get_actionQvalue(State.right)):
        action = State.right
    elif (maxV == s.get_actionQvalue(State.up)):
        action = State.up
    else:
        action = State.down;
    
    return action
    
'''
Get policy of a given state

@param s - the state for which policy will be found
@param maxQ - corresponding maximum Q value
'''
def getPolicy(State s, double maxQ):
    action = State.left
    qValuesDict = s.get_actionQvalues()

    for key in qValuesDict:
        if (qValuesDict[key] == maxQ):
            action = key
    
    return action
                
            
