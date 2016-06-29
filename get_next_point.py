def get_next_point(position, heading, grid_size, action):
    next_point = list(position)
    next_heading = list(heading)
    if action == 'forward':
        next_point = [(next_point[i] + heading[i]) % grid_size[i]
                      for i in range(2)]
    elif action == 'right':
        if heading[0]: #turned to EW axis
            next_point[1] = (next_point[1] + heading[0]) % grid_size[1]
            next_heading = [heading[1], heading[0]]
        else: # turned to NS axis
            next_point[0] = (next_point[0] - heading[1]) % grid_size[0]
            next_heading = [-heading[1], heading[0]]
    elif action == 'left':
        if heading[0]:
            next_point[1] = (next_point[1] - heading[0]) % grid_size[1]
            next_heading = [heading[1], -heading[0]]
        else:
            next_point[0] = (next_point[0] + heading[1]) % grid_size[0]
            next_heading = [heading[1], heading[0]]
    elif action != None:
        raise ValueError('Invalid action.')
    
    next_point = [grid_size[i] if next_point[i] == 0 else next_point[i]
                  for i in range(2)]

    return tuple(next_point), tuple(next_heading)