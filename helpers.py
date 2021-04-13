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
stateMatrix = [] #store all explored states

'''
Update Q-value of a given state

@param s - the state for which Q-value will be updated
@param action - the action taken on the state
@param nextState - the state on which the robot will land
'''
def updateQ(State s, int action, State nextState):
    if (!s.isIsFinalState()):
        #the FORMULA of Q-learning updates
        #value = (1 - alpha) * s.actionsQValue.get(action) + alpha * (nextState.getReward(s) + getMaxQ(nextState));
        value = (1 - alpha) * s.get_Qvalue(action) + alpha * (nextState.getReward(s) + getMaxQ(nextState));

        if (action == State.left):
            s.actionsQValue.put(State.left, value)
            if (!s.exploredActions.contains(State.left)):
                s.exploredActions.add(State.left)
            
        if (action == State.right):
            s.actionsQValue.put(State.right, value)
            if (!s.exploredActions.contains(State.right)):
                s.exploredActions.add(State.right)
            
        if (action == State.up):
            s.actionsQValue.put(State.up, value)
            if (!s.exploredActions.contains(State.up)):
                s.exploredActions.add(State.up)
            
        if (action == State.down):
            s.actionsQValue.put(State.down, value)
            if (!s.exploredActions.contains(State.down)):
                s.exploredActions.add(State.down)

'''
Get maximum Q-value of a given state

@param s - the state for which max Q-value will be found
'''
def getMaxQ(State s):
    maxQ = Math.max(s.actionsQValue.get(State.left), 
                Math.max(s.actionsQValue.get(State.right), 
                Math.max(s.actionsQValue.get(State.up), s.actionsQValue.get(State.down))));
    return maxQ;
    

'''
Get policy of a given state

@param s - the state for which policy will be found
@param maxQ - corresponding maximum Q value
'''
def getPolicy(State s, double maxQ):
    action = 1;
    if (!s.isIsFinalState()) 
        for (Entry<Integer, Double> entry : s.actionsQValue.entrySet()) 
            if (Objects.equals(maxQ, entry.getValue())) 
                action = entry.getKey();
    
    return action;
    
'''
Get action for a given state

@param s - the state for which action will be found

'''
def getAction(State s):
    int action = 0;
    ArrayList<Integer> possibleActions = new ArrayList();

    for (int i = 1; i <= 4; i++) 
        if (!s.exploredActions.contains(i)) 
            possibleActions.add(i);
        
    
    if (!possibleActions.isEmpty()) 
        rnd = new Random().nextInt(possibleActions.size());
        action = possibleActions.get(rnd);
     else 
        action = getPolicy(s);
    

    return action;

    
'''
Get policy of a given state

@param s - the state for which policy will be found

'''
def getPolicy(State s):
    action = 0;
    double max = getMaxQ(s);
    if (max == s.actionsQValue.get(State.left)) 

        action = State.left;
     else if (max == s.actionsQValue.get(State.right)) 

        action = State.right;
     else if (max == s.actionsQValue.get(State.up)) 

        action = State.up;
     else 

        action = State.down;
    
    return action;
    
'''
Print Q values of states
'''
def printQ():
    for (int v = 0; v < Main.windowWidth; v = v + Robot.rectWidth) 
        for (int j = 0; j < Main.windowHeight; j = j + Robot.rectHeight) 
            State state = ReInforcementLearning.stateMatrix[v][j];
            if (state != null) 
                System.out.println("From state " + state.id + ": x, y " + state.x + " " + state.y + " ");
                System.out.println("left " + (state.actionsQValue.get(State.left)));
                System.out.println("right " + (state.actionsQValue.get(State.right)));
                System.out.println("down " + (state.actionsQValue.get(State.down)));
                System.out.println("up " + (state.actionsQValue.get(State.up)));
                System.out.println("");
                
            
        
    

