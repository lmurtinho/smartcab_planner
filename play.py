from get_next_point import get_next_point
from get_reward import get_reward

import pandas as pd
import random
#import time

GRID = (8, 6)
POSSIBLE_ACTIONS = (None, 'forward', 'left', 'right')
N_TRIALS = 100
DEADLINE = 100


def get_random_position(grid_size):
    return tuple([random.choice(range(number)) + 1
                  for number in grid_size])




#print location, destination, heading

trial_results = []

for i in range(N_TRIALS):
    location = get_random_position(GRID)
    destination = get_random_position(GRID)
    while destination == location:
        destination = get_random_position(GRID)        
    axis = random.choice(range(2))
    heading = tuple([0 if i != axis else random.choice([-1, 1])
                    for i in range(2)])
    result = [destination, location, heading]
    reward_sum = 0

    for i in range(DEADLINE):
        action = random.choice(POSSIBLE_ACTIONS)
        location, heading = get_next_point(location, heading, GRID, action)
        reward = get_reward(location, destination, GRID, 100-i)
        reward_sum += reward
        if location == destination:
            break
    result.extend([i+1, reward_sum])
    trial_results.append(result)

df = pd.DataFrame(trial_results)
df.columns = ['destination', 'initial_location', 'initial_heading',
              'n_steps', 'reward_sum']
print df.describe()