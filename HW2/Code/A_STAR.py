from Algorithm import Algorithm
import heapq

class A_STAR(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def run_algorithm(self, snake):
        #################################################################################
        if len(self.path) > 0:
            return self.path.pop()
        init, goal = self.get_initstate_and_goalstate(snake)
        init.g = 0
        init.h = self.manhattan_distance(init, goal)
        init.f = init.g + init.h
        self.frontier = [init,]
        self.explored_set = []
        while self.frontier:
            current = heapq.heappop(self.frontier)
            self.explored_set.append(current)
            for neighbor in self.get_neighbors(current):
                if not self.outside_boundary(neighbor) and not self.inside_body(snake, neighbor) and neighbor not in self.explored_set:
                    neighbor.parent = current
                    if neighbor == goal:
                        return self.get_path(neighbor)
                    neighbor.g = current.g + 1
                    neighbor.h = self.manhattan_distance(neighbor, goal)
                    neighbor.f = neighbor.g + neighbor.h
                    heapq.heappush(self.frontier, neighbor)
        #################################################################################