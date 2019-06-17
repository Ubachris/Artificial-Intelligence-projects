import operator
import ast
import random
import numpy
import time 

"""a dictionary list indicating the possible actions an agent can perform in a state where U= Up,
D= Down, L= Left, R= Right. The values of the actions are gotten relative to the grid""" 
action_List= { 'U': (-1,0), 'D': (1,0), 'L': (0,-1), 'R': (0,1) }

start_time= time.time()

#ensures that the execution doesn't execute for more than 25 seconds before returning an optimal policy
max_allowable_time_limit= 25.00

with open('input.txt', 'r') as file:
    """Extracts information from the given file such as grid size, wall states number and positions,
    terminal states number and positions, transition model probability which indicates the probablity of
    moving in the intended direction, rewards and discount factor within the range [0, 1]"""


    gridSize= int(file.readline())
    numWalls= file.readline()
    numWalls= int (numWalls)
    walls= set()

    for i in range(numWalls):
        wallPositions= file.readline()
        wallCoord= wallPositions.replace(",", " ")
        wallCoord= wallCoord.split()
        wallCoord= map(int, wallCoord)
        wallLocation= tuple(wallCoord)
        walls.add(wallLocation)

    terminalStates= int(file.readline())
    tStates= {}

    for i in range(terminalStates):
        state= file.readline()
        state= state.replace(",", " ").split()
        state= map(int, state)
        tStates[state[0], state[1]]= state[2]

    Probability= ast.literal_eval(file.readline())
    Reward= ast.literal_eval(file.readline())
    Gamma= ast.literal_eval(file.readline())



class MDP:
    """Creates an mdp with states, actions, rewards and transition models for each state. Also includes a
    discount factor which makes the agent prefer present rewards to rewards in the future by assigning less
    value to them""" 


    def __init__(self, actlist, terminals, transitions, reward, states, gamma):
        self.states = states
        self.actlist= actlist
        self.terminals= terminals
        self.transitions= transitions
        self.reward= reward
        self.gamma= gamma

    def R(self, state):
        """Returns the rewards for each state"""

        return self.reward[state]

    def T(self, state, action):
        """Returns a list of possible transitions for performing the given action at the given state
        in (probability, resultant-state) tuple"""

        return self.transitiona[state][action]

    def actions(self, state):
        """Returns a list of actions that can be performed in each state, which are obtained from the keys in
        an action list dictionary. returns no action in terminal state"""

        if state in self.terminals:
            return ['E']

        else:
            list_of_actions= action_List.keys()
            return list_of_actions

def printGrid(grid):
    """Prints a string representation of the grid"""

    copy_grid= grid
    #copy_grid.reverse()
    for row in copy_grid:
        str_row= []
        for col in row:
            col = str(col)
            str_row.append(col)
        print " ".join(str_row)


def makeGrid(gridSize):
    """Takes the information from the input file (grid size, walls, terminal states, transition probability,
    rewards and discount factor) and creates a 2 dimensional grid which is a list of lists with tuples 
    representing the row and column of each state in the mdp with the rows increasing vertically downwards, 
    and the columns increasing horizontally to the left"""

    grid= []
    for row in range(1, gridSize+1):
        gridRow= []
        for col in range(1, gridSize+1):
            validState= (row, col)

            if validState in walls:
                gridRow.append(None)

            else:
                if validState in tStates:
                    terminalReward= tStates.get(validState)
                    gridRow.append(terminalReward)

                else: 
                    gridRow.append(Reward)
        grid.append(gridRow)

    return grid

def vector_add(a,b):
    return tuple( map(operator.add, a,b) )

"""printGrid(newGrid)"""

class GridMDP(MDP):
    """Creates a gridd MDP class from the given grid received from the input file""" 
    
    def __init__(self, grid, terminals, gamma):

        grid_copy= grid
        reward= {}
        states= set()
        terminals= {}
        self.rows= len(grid_copy)
        self.cols= len(grid_copy[0])
        self.grid= grid_copy
        
        for x in xrange(self.rows):
            for y in xrange(self.cols):
                if grid_copy[x][y] is not None:
                    states.add((x,y))
                    reward[(x,y)]= grid_copy[x][y]

                    if grid_copy[x][y] != Reward and grid_copy[x][y] != None:
                        terminals[(x,y)]= grid_copy[x][y]

        self.states= states
        self.terminals= terminals

        #transitions is a list of lists showing a state and the probability of performing all actions in it
        transitions= {}

        for s in states:
            transitions[s]= {}

            for a in action_List:
                transitions[s][a]= self.getTranstitionModel(s, a)

        MDP.__init__(self, actlist= action_List, terminals= terminals, transitions= transitions,
         reward= reward, states= states, gamma= gamma )


    def getTranstitionModel(self, state, action):
        """Returns a list of tuples indicating the probability of ending up in the intended state and
        the probabilities of veering away from the intended state in a 45 deg. clockwise direction and
        45 deg. counter clockwise direction due to the stochastic nature of the mdp"""

        unintended_Probability= (1-Probability)/2
        action_vector= action_List[action]
        off_clockwise= (0,0)
        off_cclockwise= (0,0)

        if state in self.terminals:
            return []

        if (action == 'U'):
            off_clockwise= (-1,1)
            off_cclockwise= (-1,-1)

        elif (action == 'D'):
            off_clockwise= (1,-1)
            off_cclockwise= (1,1)

        elif (action == 'L'):
            off_clockwise= (-1,-1)
            off_cclockwise= (1,-1)
        
        elif(action == 'R'):
            off_clockwise= (1,1)
            off_cclockwise= (-1,1)


        intended_movement= (Probability, self.go(state, action_vector)) 
        unintended_movement_clockwise= (unintended_Probability, self.go(state, off_clockwise))
        unintended_movement_cclockwise= (unintended_Probability, self.go(state, off_cclockwise))

        return [intended_movement, unintended_movement_clockwise, unintended_movement_cclockwise]

    
    def go(self, state, new_direction):
        """resultant vector addition of going in a new direction from the present state
        it returns the new state if it is present in the set of states, otherwise it returns current state"""

        result_state= vector_add(state, new_direction)

        return result_state if result_state in self.states else state

    def T(self, state, action):
        """returns the transition model for performing the given certain action at the given certain state
        it returns probability of 0 for terminal state, and remains in the same state"""

        if action is 'E':
            return [(0.0, state)]
        else:
            return self.transitions[state][action]

    def printStates(self):
        """Prints the set of states in the mdp"""

        print "States: "
        print self.states
        print "\n"

    def printRewards(self):
        """Prints the rewards for each state in the mdp"""  

        print "Rewards: "
        print self.reward
        print "\n"

    def printTerminalStates(self):
        """Prints the termo=inal states of the mdp received from the input file""" 

        print "Terminal States: "
        print self.terminals
        print "\n"

    def printTransitionModels(self):
        """For each state, it prints the transition model which represents the probability of performing
        all possible actions in the given states while accounting for unintended movements"""

        print "Transition models: "
        print self.transitions
        print "\n"


def argmax(seq, fn):
    """Returns an element from a list, which when applied to a function fn has the largest
    value obtained"""

    """best= seq[0]
    best_score= fn(best)
    for x in seq:
        new_score= fn(x)
        if new_score > best_score:
            best = x
            best_score = new_score
    return best"""


    action_list= numpy.array(seq)
    utilities_list= numpy.array([fn(x) for x in seq])

    index= numpy.argmax(utilities_list)

    return action_list[index]


# Initializing a new grid based on the grid size
newGrid= makeGrid(gridSize)
#printGrid(newGrid)

#Creating an instance of the GRIDMDP
markov_decision_process= GridMDP(newGrid, tStates, Gamma)
#markov_decision_process.printTerminalStates()
#markov_decision_process.printRewards()
#markov_decision_process.printStates()
#markov_decision_process.printTransitionModels()

def policy_iteration(mdp):
    """ Using the policy iteration method to find the optimal policy of an mdp, where U is a dictionary of 
    utilities mapping states to their utility values, and pi is a dictionary mapping states to actions which
    maximize their values. It alternates between policy evaluation and policy improvement"""

    U= {s:0 for s in mdp.states}
    pi= {s: random.choice(list(mdp.actions(s))) for s in mdp.states}
    #print U
    #print pi

    while True:

        elapsed_time= time.time() - start_time

        U= policy_evaluation(pi, U, mdp)
        unchanged= True
        #print U
        #print "\n"

        for s in mdp.states:
            a = argmax(mdp.actions(s), lambda a: expected_utility(a, s, U, mdp))

            if a!= pi[s]:
                pi[s]= a
                unchanged= False

        if unchanged:
            print "Total time elapsed: %s seconds" %elapsed_time
            return pi

        """if elapsed_time > max_allowable_time_limit:
            return pi"""


def policy_evaluation(pi, U, mdp, K=5):
    """ Uses modified policy iteration to return an updated utility that maps each
    state in the mdp to its utility """

    R= mdp.R
    T= mdp.T
    gamma= mdp.gamma

    #print "New Evaluation"

    for i in range(K):
        #print "Evaluation: " + str(i)
        #print "\n"
        #print U
        #print "\n"
        for s in mdp.states:
            U[s]= R(s) + gamma * sum(p * U[s1] for (p, s1) in T(s, pi[s]))

    #print "End of Evaluation"
    return U

def expected_utility(a, s, U, mdp):
    """expected utility of performing action a in state s, according to the MDP and U."""

    return sum(p * U[s1] for (p, s1) in mdp.T(s, a))


def OptimalActionGrid(grid_size, policy):
    """Returns a grid representation of the actions obtained from the optimal policy. Size of the grid
    is the same as the size of the original grid"""
    
    optimal_actions= []

    for x in xrange(grid_size):
        action_row= []
        for y in xrange(grid_size):
            new_state= (x, y)

            if new_state in policy:
                action= policy[new_state] 
                action_row.append(action)

            else:
                action_row.append('N')

        optimal_actions.append(action_row)

    return optimal_actions


optimal_policy= policy_iteration(markov_decision_process)

action_grid= OptimalActionGrid(gridSize, optimal_policy)

#printGrid(action_grid)

with open('output.txt', 'w') as output_file:

    for rows in action_grid:
        count= 0
        for col in rows:
            output_file.write(str(col))

            if count < gridSize-1:
                output_file.write(",")


            count+= 1


        output_file.write('\n')

#transition= markov_decision_process.T((4,2), 'R')
#print transition

#Reward= markov_decision_process.R((72,73))
#print Reward



    