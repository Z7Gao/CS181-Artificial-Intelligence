# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """

        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def min_val(curr_state, curr_depth, agent_index):
            ghost_num = curr_state.getNumAgents() - 1
            if curr_depth == self.depth or curr_state.isWin() or curr_state.isLose():
                return self.evaluationFunction(curr_state)
            val = 2333333
            for action in curr_state.getLegalActions(agent_index):
                succ_state = curr_state.generateSuccessor(agent_index, action)
                if agent_index == ghost_num:
                    val = min(val,max_val(succ_state, curr_depth+1))
                else:
                    val = min(val,min_val(succ_state, curr_depth, agent_index+1))
            return val  

        def max_val(curr_state, curr_depth):
            if curr_depth == self.depth or curr_state.isWin() or curr_state.isLose():
                return self.evaluationFunction(curr_state)
            val = -2333333
            for action in curr_state.getLegalActions(0):   
                val = max(min_val(curr_state.generateSuccessor(0, action), curr_depth, 1), val)
            return val
         
        result = -2333333
        Action = 0
        for action in gameState.getLegalActions(0):
            tmp = min_val(gameState.generateSuccessor(0, action), 0, 1)
            if tmp > result:
                Action = action
                result = tmp
        return Action
        
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def min_val(curr_state, curr_depth, agent_index, a, b):
            ghost_num = curr_state.getNumAgents() - 1
            if curr_depth == self.depth or curr_state.isWin() or curr_state.isLose():
                return self.evaluationFunction(curr_state)
            val = float("+inf")
            for action in curr_state.getLegalActions(agent_index):
                succ_state = curr_state.generateSuccessor(agent_index, action)
                if agent_index == ghost_num:
                    val = min(val,max_val(succ_state, curr_depth+1, a, b))
                    if val < a:
                        return val
                    b = min(b, val)
                else:
                    val = min(val,min_val(succ_state, curr_depth, agent_index+1, a, b))
                    if val < a:
                        return val
                    b = min(b, val)

            return val  

        def max_val(curr_state, curr_depth, a, b):
            if curr_depth == self.depth or curr_state.isWin() or curr_state.isLose():
                return self.evaluationFunction(curr_state)
            val = float("-inf")
            for action in curr_state.getLegalActions(0):   
                val = max(min_val(curr_state.generateSuccessor(0, action), curr_depth, 1, a, b), val)
                if val > b:
                    return val
                a = max(a, val)
            return val
         
        result = float("-inf")
        Action = "Still"
        a = float("-inf")
        b = float("+inf")
        for action in gameState.getLegalActions(0):
            tmp = min_val(gameState.generateSuccessor(0, action), 0, 1, a, b)
            if tmp > result:
                Action = action
                result = tmp
            if result > b:
                return result
            a = max(a, result)
        return Action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def exp_val(curr_state, curr_depth, agent_index):
            ghost_num = curr_state.getNumAgents() - 1
            if curr_depth == self.depth or curr_state.isWin() or curr_state.isLose():
                return self.evaluationFunction(curr_state)
            val = 0
            p = 1.0/len(curr_state.getLegalActions(agent_index))
            for action in curr_state.getLegalActions(agent_index):
               
                succ_state = curr_state.generateSuccessor(agent_index, action)
                if agent_index == ghost_num:
                    val += p*max_val(succ_state, curr_depth+1)
                else:
                    val += p*exp_val(succ_state, curr_depth, agent_index+1)
            return val  

        def max_val(curr_state, curr_depth):
            if curr_depth == self.depth or curr_state.isWin() or curr_state.isLose():
                return self.evaluationFunction(curr_state)
            val = -2333333
            for action in curr_state.getLegalActions(0):   
                val = max(exp_val(curr_state.generateSuccessor(0, action), curr_depth, 1), val)
            return val
         
        result = -2333333
        Action = 0
        for action in gameState.getLegalActions(0):
            tmp = exp_val(gameState.generateSuccessor(0, action), 0, 1)
            if tmp > result:
                Action = action
                result = tmp
        return Action

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 4).

    DESCRIPTION: <write something here so we know what you did>
    1. zfood: the less distance to food, the better. So I use the sum of reciprocal of distance to every food.
    2. zghost: if they are scared, the less distance to it, the better; 
               if they are not scared, the more distance to them, the better.
    3. zcapsule: capsule is good! try to eat them.
    4. score goes down as time goes by. So current score needs to be considered.

    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghost_states = currentGameState.getGhostStates()
    scared_times = [ghostState.scaredTimer for ghostState in ghost_states]
    capsule_states = currentGameState.getCapsules()

    manhattan = lambda x: abs(pos[0] - x[0]) + abs(pos[1]-x[1])
    zfood = sum([1.0/manhattan(i) for i in food.asList()])

    zghost = 0
    for ind, val in enumerate(scared_times):
        if val > 0:
            zghost += 1/manhattan(ghost_states[ind].getPosition())
        else:
            zghost -= manhattan(ghost_states[ind].getPosition())
    
    zcapsule = sum([1.0/manhattan(i) for i in capsule_states])
    
    return zfood + zghost + zcapsule + currentGameState.getScore()


    

# Abbreviation
better = betterEvaluationFunction
