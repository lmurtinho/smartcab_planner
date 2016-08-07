# -*- coding: utf-8 -*-
import random

POSSIBLE_ACTIONS = ('forward', 'left', 'right')

class Planner():
    """
    Basic Planner class.
    """
    def __init__(self, initial_val=0, disc_rate=0.5, 
                 learn_rate_func= lambda x: 1.0 / (x + 1)):
        self.initial_val = initial_val
        self.disc_rate = disc_rate
        self.learn_rate_func = learn_rate_func
        self.qvals = {}
        self.possible_actions = POSSIBLE_ACTIONS

    def update_qval(self, experience, t):
        """
        Returns an updated version of the dict
        with Q-values for (state, action) pairs.
        """
        # learning rate decreases over time
        # according to a predefined function
        learn_rate = self.learn_rate_func(t)

        state, action, reward, next_state = experience
        # get the current Q-value for the (state, action) pair    
        current_qval = self.qvals.get((state, action), 0)
        # get the best action for the next state
        # given the information in the qvals dict
        next_action = self.policy(next_state)
        # update the Q-value for the (state, action) pair    
        update_qval = (1-learn_rate) * current_qval + \
        learn_rate * (reward + self.disc_rate * \
            self.qvals.get((next_state, next_action), 
                           self.initial_val))
        self.qvals[(state, action)] = update_qval

class RandomPlanner(Planner):
    """
    A planner that takes actions at random.
    """
    
    def policy(self, state):
        return random.choice(self.possible_actions)
 
class PerfectPlanner(Planner):
    """
    A planner that always takes the best possible action.
    """

    def policy(self, state):
        """
        Returns the best action given the agent's
        position relative to its destination as well as
        its heading.
        """
        delta, heading = state
        # if agent is turned to the east/west axis
        if heading[0]:
            # if it needs to go forward, do it
            if delta[0] * heading[0] > 0:
                return 'forward'
            # else check if it needs to go right or left
            elif delta[1] * heading[0] > 0:
                return 'right'
            else:
                return 'left'
        # if agent is turned to the north/south axis
        else:
            # if it needs to go forward, do it
            if delta[1] * heading[1] > 0:
                return 'forward'
            # else check if it needs to go righ or left
            elif delta[0] * heading[1] < 0:
                return 'right'
            else:
                return 'left'

class LearningPlanner(Planner):
    """
    A planner that learns a policy over time.
    """
    
    def policy(self, state):
        # get the value of each action given the
        # current state
        possible_vals = {action: self.qvals.get((state, action), 
                                                self.initial_val)
                         for action in self.possible_actions}
    
        # find the actions that yield the largest value
        best_actions = [action for action in possible_vals.keys()
                        if possible_vals[action] == \
                            max(possible_vals.values())]
    
        # randomly pick one of the best actions
        return random.choice(best_actions)