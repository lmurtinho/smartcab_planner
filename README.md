# Udacity's Machine Learning Nanodegree Capstone Project: Train a Smartcab Planner

This is my capstone project for Udacity's Machine Learning Engineer Nanodegree, in which I use reinforcement learning (Q-learning) to come up with a planner that learns which actions to perform in order to reach a point in a grid-like world.

This project was heavily inspired by the nanodegree's Project 4, Teach a Smartcab How to Drive. In fact, this project can be seen as using Q-learning to come up with the planner that is provided in that project.

To check the results of the project, run the notebook `smartcab_planner.ipynb`, which will use the functions and classes defined in the .py files:

- `PlannerWorld`: The class that implements the world (an $8\times6$ toroidal grid) in which the planner agent operates
- `RandomPlanner`, `PerfectPlanner`, `LeraningPlanner`: different types of planner that operate in the planner world
- `sim_all_planners`: a function that outputs the results of running the planner world with different planners, one at a time