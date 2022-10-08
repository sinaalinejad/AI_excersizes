import random

#################################################################################
# Functions
#################################################################################

def find_conditions_for_i(ind, condition):
    conditions = []
    for cond in condition:
        if ind in cond:
            conditions.append(cond)
    return conditions

def find_empty_states(game_state):
    emptyStates = []
    for i in range(0,25):     
        if game_state[i] is None:
            emptyStates.append(i)
    return emptyStates

def find_count_of_element_in_cond(game_state, cond, element):
    count = 0
    for i in cond:
        if game_state[i] == element:
            count += 1
    return count

def ai_action(game_state):
    ''' Generate and play move from tic tac toe AI'''
    #################################################################################
    # "*** YOUR CODE HERE ***"
    if game_state.count(2) > 0:
        return
    condition = [
            # horizontal
            (0, 1, 2, 3),
            (1, 2, 3, 4),
            (5, 6, 7, 8),
            (6, 7, 8, 9),
            (10, 11, 12, 13),
            (11, 12, 13, 14),
            (15, 16, 17, 18),
            (16, 17, 18, 19),
            (20, 21, 22, 23),
            (21, 22, 23, 24),

            # vertical
            (0, 5,  10, 15),
            (5, 10, 15, 20),
            (1, 6,  11, 16),
            (6, 11, 16, 21),
            (2, 7,  12, 17),
            (7, 12, 17, 22),
            (3, 8,  13, 18),
            (8, 13, 18, 23),
            (4, 9,  14, 19),
            (9, 14, 19, 24),

            # diagonal
            (0, 6,  12, 18),
            (6, 12, 18, 24),
            (4, 8,  12, 16),
            (8, 12, 16, 20),
            (1, 7,  13, 19),
            (5, 11, 17, 23),
            (3, 7,  11, 15),
            (9, 13, 17, 21),
        ]
    emptyStates = find_empty_states(game_state)
    prevent_p1_win = []
    prevent_2_way_win = []
    maximum_0s_in_game_state = 0
    maximum_0s_in_game_state_index = -1
    for i in emptyStates:
        conditions = find_conditions_for_i(i, condition)
        for cond in conditions:
            cond_index = condition.index(cond)
            count_0 = find_count_of_element_in_cond(game_state, cond, 0)
            count_1 = find_count_of_element_in_cond(game_state, cond, 1)
            if count_0 == 3:
                return i
            if count_0 > maximum_0s_in_game_state and count_1 == 0:
                maximum_0s_in_game_state = count_0
                maximum_0s_in_game_state_index = i
            if count_1 == 3:
                prevent_p1_win.append(i)
            if cond_index < len(condition)-1 and condition[cond_index][1] == condition[cond_index+1][0]:
                count = find_count_of_element_in_cond(game_state, condition[cond_index][1:], 1)
                if count == 2:
                    for j in condition[cond_index][1:]:
                        if game_state[j] == None:
                            prevent_2_way_win.append(j)
            
    if len(prevent_p1_win) > 0:
        return prevent_p1_win[0]
    if len(prevent_2_way_win) > 0:
        return prevent_2_way_win[0]
    if maximum_0s_in_game_state_index != -1:
        return maximum_0s_in_game_state_index
    return random.choice(emptyStates)
    #################################################################################
    