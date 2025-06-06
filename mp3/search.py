import heapq
# You do not need any other imports

def best_first_search(starting_state):
    '''
    Implementation of best first search algorithm

    Input:
        starting_state: an AbstractState object

    Return:
        A path consisting of a list of AbstractState states
        The first state should be starting_state
        The last state should have state.is_goal() == True
    '''
    # we will use this visited_states dictionary to serve multiple purposes
    # - visited_states[state] = (parent_state, distance_of_state_from_start)
    #   - keep track of which states have been visited by the search algorithm
    #   - keep track of the parent of each state, so we can call backtrack(visited_states, goal_state) and obtain the path
    #   - keep track of the distance of each state from start node
    #       - if we find a shorter path to the same state we can update with the new state 
    # NOTE: we can hash states because the __hash__/__eq__ method of AbstractState is implemented

    #                     cur       parent, dis from start
    visited_states = {starting_state: (None, 0)}

    # The frontier is a priority queue
    # You can pop from the queue using "heapq.heappop(frontier)"
    # You can push onto the queue using "heapq.heappush(frontier, state)"
    # NOTE: states are ordered because the __lt__ method of AbstractState is implemented
    frontier = []
    heapq.heappush(frontier, starting_state)
    # TODO(III): implement the rest of the best first search algorithm
    # HINTS:
    #   - add new states to the frontier by calling state.get_neighbors()
    #   - check whether you've finished the search by calling state.is_goal()
    #       - then call backtrack(visited_states, state)...
    # Your code here ---------------
    while frontier:
        cur_state = heapq.heappop(frontier)
        if cur_state.is_goal():
            return backtrack(visited_states, cur_state)
        neighbor_state = cur_state.get_neighbors()
        #print(f"current: {cur_state.state}")
        for n_state in neighbor_state:
            #print(f"neighbors: {n_state.state}")
            n_distance = n_state.dist_from_start
            if n_state not in visited_states or n_distance < visited_states[n_state][1]:
                visited_states[n_state] = (cur_state,n_distance)
                heapq.heappush(frontier, n_state)
#            print(f"prev state: {cur_state.state} next state: {n_state.state}")

    # ------------------------------
    
    # if you do not find the goal return an empty list
    return []

# TODO(III): implement backtrack method, to be called by best_first_search upon reaching goal_state
# Go backwards through the pointers in visited_states until you reach the starting state
# NOTE: the parent of the starting state is None
def backtrack(visited_states, goal_state):
    path = []
    # Your code here ---------------
#    return path
    cur_state = goal_state
    while cur_state is not None:
        path.append(cur_state)
        cur_state = visited_states[cur_state][0]
    path.reverse()
    # ------------------------------
    return path