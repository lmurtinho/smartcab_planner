# -*- coding: utf-8 -*-
from planner_world import PlannerWorld

def sim_all_planners(grid, trials, deadline, planners, planners_names):
    """
    For each planner, simulates the planner world and returns
    the results data frame and q-table.
    """
    world = PlannerWorld(grid, trials, deadline)
    results = {}
    qvals = {}    
    for (planner, planner_name) in zip(planners, planners_names):
        planner_sim = world.simulate(planner)
        results[planner_name] = planner_sim[0]
        qvals[planner_name] = planner_sim[1]
    return results, qvals