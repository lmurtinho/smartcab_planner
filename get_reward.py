from get_delta import get_delta

def get_reward(location, destination, grid_size, deadline):
    delta = get_delta(location, destination, grid_size)
    distance = sum([abs(i) for i in delta])
    if distance:
        reward = -distance
    else:
        reward = deadline
    return reward