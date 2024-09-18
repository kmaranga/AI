#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import math


# In[ ]:


student_name = "Lorenzo Castaneda"


# In[9]:


# 1. Q-Learning
class QLearningAgent:
    """Implement Q Reinforcement Learning Agent using Q-table."""

    def __init__(self, game, discount, learning_rate, explore_prob):
        """Store any needed parameters into the agent object.
        Initialize Q-table.
        """
        self.game = game
        self.discount = discount
        self.lr = learning_rate
        self.ep = explore_prob
        self.qvals = dict()

    def get_q_value(self, state, action):
        """Retrieve Q-value from Q-table.
        For an never seen (s,a) pair, the Q-value is by default 0.
        """
        if (state, action) in self.qvals.keys():
            return self.qvals[(state, action)]
        else:
            self.qvals[(state, action)] = 0
            return 0
            

    def get_value(self, state):
        """Compute state value from Q-values using Bellman Equation.
        V(s) = max_a Q(s,a)
        """
        if len(self.game.get_actions(state)) == 0:
            return 0
        return max(self.get_q_value(state,a) for a in self.game.get_actions(state))

    def get_best_policy(self, state):
        """Compute the best action to take in the state using Policy Extraction.
        π(s) = argmax_a Q(s,a)

        If there are ties, return a random one for better performance.
        Hint: use random.choice().
        """
        maxq = float("-inf")
        maxacts = []
        for action in self.game.get_actions(state):
            qval = self.get_q_value(state, action)
            if qval > maxq:
                maxq = qval
                maxacts = [action]
            elif qval == maxq:
                maxacts.append(action)
                
        return random.choice(maxacts)

    def update(self, state, action, next_state, reward):
        """Update Q-values using running average.
        Q(s,a) = (1 - α) Q(s,a) + α (R + γ V(s'))
        Where α is the learning rate, and γ is the discount.

        Note: You should not call this function in your code.
        """
        self.qvals[(state, action)] = (1 - self.lr) * self.get_q_value(state, action) + \
        self.lr * (reward + self.discount * self.get_value(next_state))

    # 2. Epsilon Greedy
    def get_action(self, state):
        """Compute the action to take for the agent, incorporating exploration.
        That is, with probability ε, act randomly.
        Otherwise, act according to the best policy.

        Hint: use random.random() < ε to check if exploration is needed.
        """
        if random.random() < self.ep:
            return random.choice(list(self.game.get_actions(state)))
        else:
            return self.get_best_policy(state)


# In[ ]:


# 3. Bridge Crossing Revisited
def question3():
    epsilon = 1
    learning_rate = 1
    return "NOT POSSIBLE"
    # If not possible, return 'NOT POSSIBLE'


# In[10]:


# 5. Approximate Q-Learning
class ApproximateQAgent(QLearningAgent):
    """Implement Approximate Q Learning Agent using weights."""

    def __init__(self, *args, extractor):
        """Initialize parameters and store the feature extractor.
        Initialize weights table."""

        super().__init__(*args)
        self.extractor = extractor
        self.weights = dict()

    def get_weight(self, feature):
        """Get weight of a feature.
        Never seen feature should have a weight of 0.
        """
        if feature in self.weights.keys():
            return self.weights[feature]
        else:
            self.weights[feature]  = 0
            return 0
        

    def get_q_value(self, state, action):
        """Compute Q value based on the dot product of feature components and weights.
        Q(s,a) = w_1 * f_1(s,a) + w_2 * f_2(s,a) + ... + w_n * f_n(s,a)
        """
        q = 0
        for f, v in self.extractor(state,action).items():
            q += self.get_weight(f) * v
        return q

    def update(self, state, action, next_state, reward):
        """Update weights using least-squares approximation.
        Δ = R + γ V(s') - Q(s,a)
        Then update weights: w_i = w_i + α * Δ * f_i(s, a)
        """
        delta = reward + self.discount * self.get_value(next_state) - \
        self.get_q_value(state, action)
        for f, v in self.extractor(state, action).items():
            self.weights[f] = self.get_weight(f) + self.lr * delta * v


# In[ ]:


# 6. Feedback
# Just an approximation is fine.
feedback_question_1 = 5


# In[ ]:


feedback_question_2 = """
Most challenging is defo just understanding the equations and hoq they work. 
"""


# In[ ]:


feedback_question_3 = """
I liked how there were questions that made you think and respond to based on understanding each of the parameters.
I think more little exercises like that would go a long way!
"""

