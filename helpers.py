from state import State
import random, time

alpha = 0.1;
gamma = 0.9

'''
Update Q-value of a given state

s - the state for which Q-value will be Ndated
action - the action taken on the state
nextState - the state on which the robot will land
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
        if (State.S not in s.get_exploredActions()):
            s.add_exploredAction(State.S)



'''
Get maximum Q-value of a given state

s - the state for which max Q-value will be found
'''
def getMaxQ(s):
    maxQ = max(
        s.get_actionQvalue(State.W), 
        max(s.get_actionQvalue(State.E), 
        max(s.get_actionQvalue(State.N), 
        s.get_actionQvalue(State.S)))
    )

    return maxQ
    
    
'''
Get action for a given state

s - the state for which action will be found

'''
def getAction(s):
    action = 0;
    possibleActions = []
    print(f'{s}\nExplored Actions:\n{s.get_exploredActions()}') # print state and explored actions

    for i in range(1,5):
        if (i not in s.get_exploredActions()):
            possibleActions.append(i)
    
    if (len(possibleActions) > 0):
        action = random.choice(possibleActions)
    else:
        action = getPolicy(s)

    print(f"Current action: {str(action)}")

    return action

    
'''
Get policy of a given state

s - the state for which policy will be found

'''
def getPolicy(s):
    action = State.W
    maxV = getMaxQ(s)
    maxActionCount = 0

    if (maxV == s.get_actionQvalue(State.W)):
        action = State.W
        maxActionCount+=1
    if (maxV == s.get_actionQvalue(State.E)):
        action = State.E
        maxActionCount+=1
    if (maxV == s.get_actionQvalue(State.N)):
        action = State.N
        maxActionCount+=1
    if (maxV == s.get_actionQvalue(State.S)):
        action = State.S;
        maxActionCount+=1

    if (maxActionCount == 4):
        action = random.choice([State.W, State.E, State.N, State.S])
    
    return action
    
'''
Get policy of a given state

s - the state for which policy will be found
maxQ - corresponding maximum Q value
'''
# def getPolicy(s, maxQ):
#     action = State.W
#     qValuesDict = s.get_actionQvalues()

#     for key in qValuesDict:
#         if (qValuesDict[key] == maxQ):
#             action = key
    
#     return action

'''
Learn environment

w - the world which will be learning
'''
def learnEnvironment(connection, w, p):
    
    p.set_currentState(w.get_state(0))

    while (w.get_isItEnd() == False):
        previousState   = p.get_currentState();                     # store your state
        action          = getAction(p.get_currentState());          # get a random direction/action
        
        p.move(connection, w, action);                              # make the move
        updateQ(previousState, action, p.get_currentState());       # update Q values
        time.sleep(15)                                              # wait before next move
