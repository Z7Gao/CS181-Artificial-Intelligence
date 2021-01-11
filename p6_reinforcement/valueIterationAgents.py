# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()


    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for i in range(self.iterations):
            values = {}
            for state in self.mdp.getStates():
                action = self.computeActionFromValues(state)
                if action and self.computeQValueFromValues(state, action):
                    values[state] = self.computeQValueFromValues(state, action)

            for state in values:
                self.values[state] = values[state]


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
         
        if action not in self.mdp.getPossibleActions(state):
            return None
        else:
            s_t = self.mdp.getTransitionStatesAndProbs(state, action)
            Q = 0
            for s_, t in s_t:
                r = self.mdp.getReward(state, action, s_)
                V_k = self.getValue(s_)
                Q += t*(r+self.discount*V_k)
            return Q



    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        V = []
        for action in self.mdp.getPossibleActions(state):
            Q = self.computeQValueFromValues(state, action)
            if Q != None:
                V.append((Q,action))
        if V:
            Q = V[0][0]
            action = V[0][1]
            for q, a in V:
                if q > Q:
                    Q = q
                    action = a
            return action   
        else:
            return None


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        num = len(self.mdp.getStates())
        for i in range(self.iterations):
            for ind, state in enumerate(self.mdp.getStates()):
                if i%num == ind:
                    action = self.computeActionFromValues(state)
                    if action and self.computeQValueFromValues(state, action):
                        self.values[state] = self.computeQValueFromValues(state, action)



class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        pred = {}
        for state in self.mdp.getStates():
            pred_ = []
            for s in self.mdp.getStates():
                for action in self.mdp.getPossibleActions(s):
                    flag = 0
                    s_t = self.mdp.getTransitionStatesAndProbs(s, action)
                    for s_, t in s_t:
                        if t != 0 and s_ == state:
                            flag = 1
                            break
                    if flag == 1:
                        pred_.append(s)
                        break
            pred[state] = pred_
    
        pq = util.PriorityQueue()
        for state in self.mdp.getStates():
            if state != "TERMINAL_STATE":
                diff = abs(self.values[state] - self.computeQValueFromValues(state, self.computeActionFromValues(state)))
                pq.push(state, -diff)

        for i in range(self.iterations):
            if pq.isEmpty():
                break
            s = pq.pop()
            if s != "TERMINAL_STATE":
                self.values[s] = self.computeQValueFromValues(s, self.computeActionFromValues(s))
            for p in pred[s]:
                diff = abs(self.values[p] - self.computeQValueFromValues(p, self.computeActionFromValues(p)))
                if diff > self.theta:
                    pq.update(p, -diff)
