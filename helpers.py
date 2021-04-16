import random
from state import State

alpha = 0.1;
gamma = 0.9

'''
Update Q-value of a given state

@param s - the state for which Q-value will be Ndated
@param action - the action taken on the state
@param nextState - the state on which the robot will land
'''
def updateQ(s, action, nextState):
    #the FORMULA of Q-learning Ndates
    value = (1 - alpha) * s.get_actionQvalue(action) + alpha * (nextState.getReward() + gamma * getMaxQ(nextState));

    if (action == State.W):
        s.add_actionQValue(State.W, value)
        if (State.W not in s.get_exploredActions()):
            s.add_exploredAction(State.W)
        
    elif (action == State.E):
        s.add_actionQValue(State.E, value)
        if (State.E not in s.get_exploredActions()):
            s.add_exploredAction(State.E)
        
    elif (action == State.N):
        s.add_actionQValue(State.N, value)
        if (State.N not in s.get_exploredActions()):
            s.add_exploredAction(State.N)
        
    elif (action == State.S):
        s.add_actionQValue(State.S, value)
        if (State.N not in s.get_exploredActions()):
            s.add_exploredAction(State.N)

'''
Get maximum Q-value of a given state

@param s - the state for which max Q-value will be found
'''
def getMaxQ(s):
    maxQ = max(s.get_actionQvalue(State.W), 
                max(s.get_actionQvalue(State.E), 
                max(s.get_actionQvalue(State.N), s.get_actionQvalue(State.S))));
    return maxQ
    
    
'''
Get action for a given state

@param s - the state for which action will be found

'''
def getAction(s):
    action = 0;
    possibleActions = []

    for i in range(1,4):
        if (i not in s.get_exploredActions()):
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
def getPolicy(s):
    action = State.W
    maxV = getMaxQ(s)

    if (maxV == s.get_actionQvalue(State.W)):
        action = State.W
    elif (maxV == s.get_actionQvalue(State.E)):
        action = State.E
    elif (maxV == s.get_actionQvalue(State.N)):
        action = State.N
    else:
        action = State.S;
    
    return action
    
'''
Get policy of a given state

@param s - the state for which policy will be found
@param maxQ - corresponding maximum Q value
'''
def getPolicy(s, maxQ):
    action = State.W
    qValuesDict = s.get_actionQvalues()

    for key in qValuesDict:
        if (qValuesDict[key] == maxQ):
            action = key
    
    return action

'''
Learn environment

@param w - the world which will be learning
'''
def learnEnvironment(connection, w, p):
    # for i in range(5001):
    for s_id in range(10):
        p.set_currentState(w.get_state(s_id))

        # while (w.isItEnd() == False):
        action = getAction(p.get_currentState());
        previousState = p.get_currentState();
        p.move(connection, w, action);
        updateQ(previousState, action, p.get_currentState());
