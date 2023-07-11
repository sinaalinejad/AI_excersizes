from random import randrange


class NQueens:
    def __init__(self, N):
        self.N = N
        self.current_state = None

    def initial(self):
        ''' Returns a random initial state '''
        return tuple(randrange(self.N) for i in range(self.N))

    def goal_test(self, state):
        ''' Returns True if the given state is a goal state '''
        for i in range(self.N):
            for j in range(i+1, self.N):
                if self.threatening_states((i, state[i]),(j, state[j])):
                    return False
        return True


    def threatening_states(self, s1, s2):
        if s1[1] == s2[1] or abs(s1[0]-s2[0]) == abs(s1[1]-s2[1]):
            return True
        return False


    def value(self, state):
        ''' Returns the value of a state. The higher the value, the closest to a goal state '''
        cnt = 0
        for i in range(self.N):
            for j in range(i+1, self.N):
                if not self.threatening_states((i, state[i]), (j, state[j])):
                    cnt += 1
        return cnt
    def neighbors(self, state):
        ''' Returns all possible neighbors (next states) of a state '''
        states = []
        result = []
        state_copy = list(state)
        for i in range(self.N):
            for j in range(self.N):
                states.append([])
                states[i*self.N + j] = state_copy.copy()
                states[i*self.N + j][i] = j
        for item in states:
            if not item in result:
                result.append(item)
        return result
                    
                

