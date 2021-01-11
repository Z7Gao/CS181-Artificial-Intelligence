# search.py
# ---------
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
import time

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):  
    """
    Input: type(problem) == searchAgents.PositionSearchProblem.
    Output: a list of actions that reaches the goal.
    Goal: Search the deepest nodes in the search tree first. A graph search algorithm.
    """

    "*** YOUR CODE HERE ***"
    explored = []
    curr_state =  problem.getStartState()
    if problem.isGoalState(curr_state): 
        return []
    fringe = util.Stack()
    fringe.push( (curr_state, [], 0) )
    while True:    
        if fringe.isEmpty(): 
            return False
        curr_state, action, cost = fringe.pop()
        if problem.isGoalState(curr_state): 
            return action
        explored.append(curr_state)
        for i in problem.getSuccessors(curr_state):
            state,dir,d_cost = i
            # if state not in explored and not [state == j[0] for j in fringe.list].count(True):
            if state not in explored:
                fringe.push((state, action+[dir], cost+d_cost))

                

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    explored = []
    curr_state =  problem.getStartState()
    if problem.isGoalState(curr_state): 
        return []
    fringe = util.Queue()
    fringe.push( (curr_state,[],0) )
    while True:    
        if fringe.isEmpty(): 
            return False
        curr_state, action, cost = fringe.pop()
        if problem.isGoalState(curr_state): 
            return action
        explored.append(curr_state)
        for i in problem.getSuccessors(curr_state):
            state,dir,d_cost = i
            if state not in explored and not [state == j[0] for j in fringe.list].count(True):
            # if state not in explored:
                fringe.push((state, action+[dir], cost+d_cost))


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    explored = []
    curr_state =  problem.getStartState()
    if problem.isGoalState(curr_state): 
        return []
    fringe = util.PriorityQueue()
    fringe.push( (curr_state,[],0), 0)
    while True:    
        if fringe.isEmpty(): 
            return False
        curr_state, action, cost = fringe.pop()
        if problem.isGoalState(curr_state): 
            return action
        explored.append(curr_state)
        for i in problem.getSuccessors(curr_state):
            state,dir,d_cost = i
            if state not in explored:
                if not [state == i[0] for p,c,i in fringe.heap].count(True):
                    fringe.push((state, action+[dir], cost+d_cost),cost + d_cost)
                elif [i[2] > cost+d_cost for p,c,i in fringe.heap].count(True):
                    fringe.update((state, action+[dir], cost+d_cost),cost + d_cost)



   
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    explored = []
    curr_state =  problem.getStartState()
    if problem.isGoalState(curr_state): 
        return []
    fringe = util.PriorityQueue()
    fringe.push( (curr_state,[],0), 0+heuristic(curr_state,problem))
    while True:    
        if fringe.isEmpty(): 
            return False
        curr_state, action, cost = fringe.pop()
        if problem.isGoalState(curr_state): 
            return action
        explored.append(curr_state)
        for i in problem.getSuccessors(curr_state):
            state,dir,d_cost = i
            if state not in explored:
                if not [state == i[0] for p,c,i in fringe.heap].count(True):
                    fringe.push((state, action+[dir], cost+d_cost),cost + d_cost + heuristic(state,problem))
                elif [i[2] > cost+d_cost for p,c,i in fringe.heap].count(True):
                    fringe.update((state, action+[dir], cost+d_cost),cost + d_cost)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
