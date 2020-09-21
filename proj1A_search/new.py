
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
    Search the deepest nodes in the search tree first.
    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    from game import Directions
    init_node=(state,action,cost)=(problem.getStartState(),[],0)
    if problem.isGoalState(state): return action

    dfs_frontier = util.Stack()
    dfs_frontier.push(init_node)
    explored = set()

    while True:
        if dfs_frontier.isEmpty(): return 'Failure'
        (state,action,cost)=dfs_frontier.pop()
        if problem.isGoalState(state): 
            print(action)
            return action
        explored.add(state)

        for child_node in problem.getSuccessors(state):
            if (child_node[0] not in explored):
                # if problem.isGoalState(child_node[0]): return action+[child_node[1]]
                dfs_frontier.push((child_node[0], action+[child_node[1]], child_node[2]+cost))

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    from game import Directions
    init_node=(state,action,cost)=(problem.getStartState(),[],0)
    if problem.isGoalState(state): return action

    bfs_frontier = util.Queue()
    bfs_frontier.push(init_node)
    explored=[]

    while True:
        if bfs_frontier.isEmpty(): return 'Failure'
        (state,action,cost)=bfs_frontier.pop()
        if problem.isGoalState(state): return action
        explored.append(state)

        for child_node in problem.getSuccessors(state):
            if (child_node[0] not in explored) and (not any(s==child_node[0] for (s,a,c) in bfs_frontier.list)):
                # if problem.isGoalState(child_node[0]): return action+[child_node[1]]
                bfs_frontier.push((child_node[0], action+[child_node[1]], child_node[2]+cost))

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    from game import Directions
    init_node=(state,action,cost) = (problem.getStartState(),[],0)
    if problem.isGoalState(state): return action

    ucs_frontier = util.PriorityQueue()
    ucs_frontier.push(init_node, 0)
    explored = set()

    while True:
        if ucs_frontier.isEmpty(): return 'Failure'
        (state,action,cost)=ucs_frontier.pop()
        if problem.isGoalState(state): return action
        explored.add(state)

        for child_node in problem.getSuccessors(state):
            if (child_node[0] not in explored) and (not any(i[0]==child_node[0] for (p,c,i) in ucs_frontier.heap)):
                ucs_frontier.push( (child_node[0], action+[child_node[1]], child_node[2]+cost), child_node[2]+cost)
            elif (any( (i[0]==child_node[0]) and (i[2]>(child_node[2]+cost)) for (p,c,i) in ucs_frontier.heap)):
                ucs_frontier.update((child_node[0], action+[child_node[1]], child_node[2]+cost), child_node[2]+cost)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    from game import Directions
    init_node=(state,action,cost) = (problem.getStartState(),[],0)
    if problem.isGoalState(state): return action

    ucs_frontier = util.PriorityQueue()
    ucs_frontier.push(init_node, 0+heuristic(state,problem))
    explored=[]

    while True:
        if ucs_frontier.isEmpty(): return 'Failure'
        (state,action,cost)=ucs_frontier.pop()
        if problem.isGoalState(state): return action
        explored.append(state)

        for child_node in problem.getSuccessors(state):
            if (child_node[0] not in explored) and (not any(i[0]==child_node[0] for (p,c,i) in ucs_frontier.heap)):
                ucs_frontier.push( (child_node[0], action+[child_node[1]], child_node[2]+cost), child_node[2]+cost + heuristic(child_node[0],problem))
            elif (any( (i[0]==child_node[0]) and (i[2]>(child_node[2]+cost)) for (p,c,i) in ucs_frontier.heap)):
                ucs_frontier.update((child_node[0], action+[child_node[1]], child_node[2]+cost), child_node[2]+cost)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch