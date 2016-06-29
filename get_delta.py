def get_delta(location, destination, grid_size):
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
                              location[i] + grid_size[i] - destination[i]]
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
                              destination[i] + grid_size[i] - location[i]]
            # if the first distance is the smallest, pick minus it
            # (the agent will have to go west/north)
            if min(possible_delta) == possible_delta[0]:
                delta[i] = -possible_delta[0]
            # if second distance is smallest, pick it
            else:
                delta[i] = possible_delta[1]
    # return a tuple
    return tuple(delta)