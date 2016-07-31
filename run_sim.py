# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 13:40:50 2016

@author: zsj7
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['figure.figsize'] = [15, 10]
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 12

from planner_world import PlannerWorld
from planner_agents import RandomPlanner, PerfectPlanner, LearningPlanner

GRID = (8, 6)
N_TRIALS = 2000
DEADLINE = 100

def learn_rate_func(t):
    return 1.0 / np.log(t + 1)

random_planner = RandomPlanner()
perfect_planner = PerfectPlanner()
final_learner = LearningPlanner(learn_rate_func=learn_rate_func)
original_learner = LearningPlanner()

world = PlannerWorld(GRID, N_TRIALS, DEADLINE)

df_random, qvals_random = world.simulate(random_planner)
df_perfect, qvals_perfect = world.simulate(perfect_planner)
df_final, qvals_final = world.simulate(final_learner)
df_original, qvals_original = world.simulate(original_learner)

results = {'perfect': df_perfect, 'random': df_random, 
           'original_learner': df_original, 'final_learner': df_final}

panel = pd.Panel(results)

for column in df_perfect.columns:
    sns.boxplot(data=panel.minor_xs(column))
    plt.title(column)
    plt.savefig("{}.png".format(column))
    plt.close()

df_learners = pd.concat([df_final['reward_sum'],
                         df_original['reward_sum']],
                        axis=1)
                        
df_learners.columns = ['final_learner', 'original_learner']

panel.minor_xs('reward_sum').rolling(window=100, center=False).mean().plot()
plt.title("sum of rewards per trial")
plt.xlabel('trial number')
plt.ylabel('sum of rewards')
plt.savefig('planners_progress.png')
plt.close()