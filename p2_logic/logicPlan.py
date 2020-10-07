# logicPlan.py
# ------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game
from itertools import permutations, product


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** YOUR CODE HERE ***"
    A, B, C = logic.Expr('A'), logic.Expr('B'), logic.Expr('C')

    L1 = A | B
    L2 = (~A) % ((~B)|C)
    L3 = logic.disjoin((~A),(~B),C)

    return logic.conjoin(L1,L2,L3)
    

def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    A, B, C, D = logic.Expr('A'), logic.Expr('B'), logic.Expr('C'), logic.Expr('D')

    L1 = C % (B|D)
    L2 = A >> ((~B)&(~D))
    L3 = (~(B & (~C))) >> A
    L4 = (~D) >> C

    return logic.conjoin(L1,L2,L3,L4)


def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    WumpusAlive_0 = logic.PropSymbolExpr('WumpusAlive[0]')
    WumpusAlive_1 = logic.PropSymbolExpr('WumpusAlive[1]')
    WumpusBorn_0 = logic.PropSymbolExpr('WumpusBorn[0]')
    WumpusKilled_0 = logic.PropSymbolExpr('WumpusKilled[0]')

    L1 = WumpusAlive_1 % ( ( WumpusAlive_0 & (~WumpusKilled_0) ) | ( (~WumpusAlive_0) & WumpusBorn_0) )
    L2 = ~(WumpusAlive_0 & WumpusBorn_0)
    L3 = WumpusBorn_0

    return logic.conjoin(L1,L2,L3)

def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    return logic.pycoSAT(logic.to_cnf(sentence))

def atLeastOne(literals) :
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single 
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    return logic.disjoin(literals)
        


def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    literals = [~(literal) for literal in literals]
    literals = map(logic.disjoin, permutations(literals, 2))
    return logic.conjoin(literals)


def exactlyOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    return logic.conjoin(atMostOne(literals), atLeastOne(literals))


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    return list(map(lambda x: x[0], sorted([pair for pair in [logic.PropSymbolExpr.parseExpr(key) for key, value in model.items() if value] if pair[0] in actions], key = lambda x: int(x[1]))))



def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"
    P_x_y_t = logic.PropSymbolExpr(pacman_str, x, y, t)

    neighbor = [(i,j) for i,j in zip([(x,y-1),(x,y+1),(x-1,y),(x+1,y)],['North', 'South', 'East', 'West']) if not walls_grid[i[0]][i[1]]]

    return P_x_y_t % logic.disjoin([ (logic.PropSymbolExpr(pacman_str, i[0][0], i[0][1], t-1) & logic.PropSymbolExpr(i[1], t-1)) for i in neighbor ])


def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """

    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    start = problem.getStartState()
    end = problem.getGoalState()
    actions = ['North', 'South', 'East', 'West']
    not_walls = [(x,y) for x,y in product(range(1,width+1), range(1,height+1)) if not walls[x][y]]

    # init^0
    init = logic.PropSymbolExpr(pacman_str, start[0], start[1], 0)
    for i in range(1, width+1):
        for j in range(1, height+1):
            if (i,j) != start:
                init = logic.conjoin(init,(~logic.PropSymbolExpr(pacman_str,i,j,0)))
    
    t = 1
    assertion = lambda t: logic.PropSymbolExpr(pacman_str, end[0], end[1], t)
    transition = lambda t: logic.conjoin([pacmanSuccessorStateAxioms(x, y, t, walls) for x, y in not_walls])
    constraint_action  = lambda t: exactlyOne([logic.PropSymbolExpr(action, t-1) for action in actions])
    constraint_position = lambda t: exactlyOne([logic.PropSymbolExpr(pacman_str, x, y, t-1) for x, y in not_walls])
    
    transition_all = transition(1)
    constraint_action_all = constraint_action(1)
    constraint_position_all = constraint_position(1)
    
    while True:         
        if t != 1:
            transition_all = logic.conjoin(transition_all, transition(t))
            constraint_action_all = logic.conjoin(constraint_action_all, constraint_action(t))
            constraint_position_all = logic.conjoin(constraint_position_all, constraint_position(t))
        model = findModel(logic.conjoin(init, transition_all, assertion(t), constraint_action_all, constraint_position_all))
        # print(model)
        if model is not False:
            # print(extractActionSequence(model, actions))
            return extractActionSequence(model, actions)
        else:
            t += 1
    

def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """

    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    start, food = problem.getStartState()
    food = food.asList()

    actions = ['North', 'South', 'East', 'West']
    not_walls = [(x,y) for x,y in product(range(1,width+1), range(1,height+1)) if not walls[x][y]]
    

    # init^0
    init = logic.PropSymbolExpr(pacman_str, start[0], start[1], 0)
    for i in range(1, width+1):
        for j in range(1, height+1):
            if (i,j) != start:
                init = logic.conjoin(init,(~logic.PropSymbolExpr(pacman_str,i,j,0)))
    
    t = 1
    # assertion = lambda t: logic.conjoin([logic.disjoin([logic.PropSymbolExpr(pacman_str, x, y, t) for i in range(t)]) for x, y in food])

    transition = lambda t: logic.conjoin([pacmanSuccessorStateAxioms(x, y, t, walls) for x, y in not_walls])
    constraint_action  = lambda t: exactlyOne([logic.PropSymbolExpr(action, t-1) for action in actions])
    constraint_position = lambda t: exactlyOne([logic.PropSymbolExpr(pacman_str, x, y, t-1) for x, y in not_walls])
    
    transition_all = transition(1)
    constraint_action_all = constraint_action(1)
    constraint_position_all = constraint_position(1)

    while True: 
        assertion = logic.PropSymbolExpr(pacman_str, start[0], start[1], 0) # just to create something in Expr form
        for x, y in food:
            tmp = logic.PropSymbolExpr(pacman_str, x, y, 0)
            for i in range(1,t+1):
                tmp = logic.disjoin(logic.PropSymbolExpr(pacman_str, x, y, i), tmp)
            assertion = logic.conjoin(assertion, tmp)        
        if t != 1:
            transition_all = logic.conjoin(transition_all, transition(t))
            constraint_action_all = logic.conjoin(constraint_action_all, constraint_action(t))
            constraint_position_all = logic.conjoin(constraint_position_all, constraint_position(t))
        model = findModel(logic.conjoin(init, transition_all, assertion, constraint_action_all, constraint_position_all))
        # print(model)
        if model is not False:
            # print(extractActionSequence(model, actions))
            return extractActionSequence(model, actions)
        else:
            t += 1


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
    
