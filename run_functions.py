# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 13:40:50 2016

@author: zsj7
"""

from planner_world import PlannerWorld

def sim_single_planner(grid, trials, deadline, planner, *args):
    return PlannerWorld(grid, trials, deadline).simulate(planner(*args))

def sim_all_planners(grid, trials, deadline, planners, planners_names):
    world = PlannerWorld(grid, trials, deadline)
    results = {}
    qvals = {}    
    for (planner, planner_name) in zip(planners, planners_names):
        planner_sim = world.simulate(planner)
        results[planner_name] = planner_sim[0]
        qvals[planner_name] = planner_sim[1]
    return results, qvals