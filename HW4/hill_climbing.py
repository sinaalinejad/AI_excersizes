from operator import ne
from NQueens import NQueens
def hill_climbing(problem: NQueens):
    ''' Returns a state as the solution of the problem '''
    neighbors = problem.neighbors(problem.current_state)
    max_value_state = neighbors[0]
    max_value = problem.value(max_value_state)
    neighbors = neighbors[1:]
    for neighbor in neighbors:
        neighbor_val = problem.value(neighbor)
        if neighbor_val >= max_value:
            max_value = neighbor_val
            max_value_state = neighbor
    return max_value_state


    

def hill_climbing_random_restart(problem, limit = 10):
    state = problem.initial()
    problem.current_state = state
    cnt = 0
    while problem.goal_test(state) == False and cnt < limit:
        state = hill_climbing(problem)
        problem.current_state = state
        cnt += 1
    return state
