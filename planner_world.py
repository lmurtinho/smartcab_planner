# -*- coding: utf-8 -*-
"""
"""

import pandas as pd
import random

class PlannerWorld():
    
    def __init__(self, grid_size=(8, 6), trials=1000, deadline=100):
        self.grid_size = grid_size
        self.trials = trials
        self.deadline = deadline
    
    def get_delta(self, location, destination):
        """
        get the horizontal and vertical distance
        between location and destination.
        """
        delta = [0, 0]
        
        for i in range(2):
            # 1st option: destination to the east/south of location
            if destination[i] > location[i]:
                # two possible distances, going east/south or
                # going west/north
                possible_delta = [destination[i] - location[i], 
                                  location[i] + self.grid_size[i] - \
                                  destination[i]]
                # if the first distance is the smallest, pick it
                if min(possible_delta) == possible_delta[0]:
                    delta[i] = possible_delta[0]
                # if seconde distance is the smallest, pick minus it
                # (the agent will have to go west/north to get to a point
                #  to the east/south)
                else:
                    delta[i] = -possible_delta[1]
            # 2nd option: destination to the west/north of location
            else:
                # two possible distances, going west/north or
                # going east/south
                possible_delta = [location[i] - destination[i],
                                  destination[i] + self.grid_size[i] - \
                                  location[i]]
                # if the first distance is the smallest, pick minus it
                # (the agent will have to go west/north)
                if min(possible_delta) == possible_delta[0]:
                    delta[i] = -possible_delta[0]
                # if second distance is smallest, pick it
                else:
                    delta[i] = possible_delta[1]
        # return a tuple
        return tuple(delta)
        
    def get_distance(self, delta):
        """
        Returns the overall distance.
        """
        return sum([abs(i) for i in delta])

    def get_reward(self, steps_left):
        """
        Returns a negative reward proportional to distance if
        the agent has not reached its destination, and a negative
        reward proportional to the time left if the agent has
        reached its destination.
        """
        delta = self.get_delta(self.planner.location, 
                               self.planner.destination)
        distance = self.get_distance(delta)
        reward = -distance if distance else steps_left
        return reward
    
    def move_agent(self, action):
        """
        Modifies the position and heading of the agent.
        """
        location = self.planner.location
        heading = self.planner.heading
        next_point = list(location) # to be modified below
        next_heading = list(heading) # to be modified below
        if action == 'forward': # just move according to the heading
            next_point = [(next_point[i] + next_heading[i]) % \
                            self.grid_size[i]
                          for i in range(2)]
        elif action == 'right':
            if heading[0]: #turned to EW axis
                next_point[1] = (next_point[1] + heading[0]) % \
                        self.grid_size[1]
                next_heading = [heading[1], heading[0]]
            else: # turned to NS axis
                next_point[0] = (next_point[0] - heading[1]) % \
                        self.grid_size[0]
                next_heading = [-heading[1], heading[0]]
        elif action == 'left':
            if heading[0]: # turned to EW axis
                next_point[1] = (next_point[1] - heading[0]) % \
                        self.grid_size[1]
                next_heading = [heading[1], -heading[0]]
            else: # turned to NS axis
                next_point[0] = (next_point[0] + heading[1]) % \
                        self.grid_size[0]
                next_heading = [heading[1], heading[0]]
        else:
            raise ValueError('Invalid action.')
        
        # check if agent has gone to the other side of the world
        next_point = [self.grid_size[i] if next_point[i] == 0 \
                        else next_point[i]
                      for i in range(2)]
                          
        # change agent's position and heading
        self.planner.location = tuple(next_point)
        self.planner.heading = tuple(next_heading)
    
    def get_random_position(self):
        """
        Returns a random position in a grid-like world.
        """
        return tuple([random.choice(range(number)) + 1
                      for number in self.grid_size])

    def simulate(self, planner):
        self.planner = planner
        trial_results = [] # to be populated
        t = 0 # to keep track of the number of actions taken by the agent
    
        for i in range(self.trials):
            # define the agent's location, destination and heading
            self.planner.location = self.get_random_position()
            self.planner.destination = self.get_random_position()
            while self.planner.destination == self.planner.location:
                self.planner.destination = self.get_random_position()        
            axis = random.choice(range(2))
            self.planner.heading = tuple(0 if i != axis else \
                                             random.choice([-1, 1])
                                         for i in range(2))

            # initialize the sum of rewards
            reward_sum = 0

            # for each step in the trial
            for i in range(self.deadline):
                t += 1 # count the time
                # get the delta between location and destination
                delta = self.get_delta(self.planner.location, 
                                       self.planner.destination)
                # set up the agent's state
                state = (delta, self.planner.heading)
                # use the planner to come up with an action
                action = self.planner.policy(state)
                # update the agent's location and heading
                self.move_agent(action)
                # get the next state and the reward associated to it
                next_delta = self.get_delta(self.planner.location,
                                            self.planner.destination)                
                next_state = (next_delta, self.planner.heading)
                reward = self.get_reward(self.deadline - i)
                # use the qval function to update the state's Q-value
                experience = (state, action, reward, next_state)
                self.planner.update_qval(experience, t)
                # update the sum of rewards
                reward_sum += reward
                # check if the agent has reached its destination
                if self.planner.location == self.planner.destination:
                    break
            # store the results of the trial
            trial_results.append((i+1, reward_sum))

        # return a dataframe with the trial results and
        # the dict with Q-values
        df = pd.DataFrame(trial_results)
        df.columns = ['n_steps', 'reward_sum']
        return df, self.planner.qvals