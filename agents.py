import copy
import math

# 1. Value Iteration
class ValueIterationAgent:

    """Implement Value Iteration Agent using Bellman Equations."""

    def __init__(self, game, discount):
        """Store game object and discount value into the agent object,
        initialize values if needed.
        """
        self.game = game
        self.discount = discount
        self.elem = {}

        for i in self.game.states:
            self.elem[i] : 0

    def get_value(self, state):
        """Return value V*(s) correspond to state.
        State values should be stored directly for quick retrieval.
        """
        try:
            return self.elem[state]
        except KeyError:
            return 0    


    def get_q_value(self, state, action):
        """Return Q*(s,a) correspond to state and action.
        Q-state values should be computed using Bellman equation:
        Q*(s,a) = Σ_s' T(s,a,s') [R(s,a,s') + γ V*(s')]
        """
        sol = 0
        if action in self.game.get_actions(state):
            for j in self.game.get_transitions(state, action).items():
                sol = sol + (j[1] * (self.discount * self.get_value(j[0]) + self.game.get_reward(state, action, j[0])))
        return sol

    def get_best_policy(self, state):
        """Return policy π*(s) correspond to state.
        Policy should be extracted from Q-state values using policy extraction:
        π*(s) = argmax_a Q*(s,a)
        """
        n = None
        z = -(math.inf)
        if (state in self.game.states):
            for i in self.game.get_actions(state):
                temp = self.get_q_value(state, i)
                if z < temp:
                    z = temp
                    n = i
        return n
    def iterate(self):
        """Run single value iteration using Bellman equation:
        V_{k+1}(s) = max_a Q*(s,a)
        Then update values: V*(s) = V_{k+1}(s)
        """
        copied = dict(self.elem)
        for i in self.game.states:
            if self.get_best_policy(i) is not None:
                copied[i] = self.get_q_value(i, self.get_best_policy(i))
        self.elem = copied        

# 2. Policy Iteration
class PolicyIterationAgent(ValueIterationAgent):
    """Implement Policy Iteration Agent.

    The only difference between policy iteration and value iteration is at
    their iteration method. However, if you need to implement helper function or
    override ValueIterationAgent's methods, you can add them as well.
    """
    def helperIterate(self, isFalse = False):
        epsilon = 1e-6
        while (not isFalse):
            # print(isFalse)
            temp = 0
            for i in self.game.states:
                if self.get_best_policy(i) is not None:
                    x = self.get_q_value(i, self.get_best_policy(i))
                    y = ((x - self.get_value(i)) ** 2) ** 0.5
                    self.elem[i] = x

                    #assign it to the larger element
                    larger = lambda a, b: a if a > b else b
                    temp = larger(temp, y)

            if (temp < epsilon):
                isFalse = True            

    def iterate(self):
        """Run single policy iteration.
        Fix current policy, iterate state values V(s) until |V_{k+1}(s) - V_k(s)| < ε
        """
        self.helperIterate(False)

# 3. Bridge Crossing Analysis
def question_3():
    discount = 0.9
    noise = 0
    return discount, noise

# 4. Policies
def question_4a():
    discount = 0.3
    noise = 0
    living_reward = 0
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4b():
    discount = 0.3
    noise = 0.1
    living_reward = 0
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4c():
    discount = 0.9
    noise = .2
    living_reward = -1
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4d():
    discount = 0.9
    noise = 0.2
    living_reward = 0 
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4e():
    discount = 0.9
    noise = 0.2
    living_reward = 11
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'
