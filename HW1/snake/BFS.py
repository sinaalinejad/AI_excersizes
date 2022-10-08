# References:
#   https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/

from collections import deque
from Utility import Node
from Algorithm import Algorithm
from Snake import Snake


class BFS(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def run_algorithm(self, snake: Snake):
        #################################################################################
        if self.path:
            return self.path.pop()
        # Create a queue for BFS
        # Mark the source node as
        # visited and enqueue it
        self.frontier, self.explored_set = [], []
        init_state, goal_state = self.get_initstate_and_goalstate(snake)
        self.frontier.append(init_state) 
        while self.frontier:
            # Dequeue a vertex from
            # queue and print it
            s = self.frontier.pop(0)
            if s == goal_state:
                return self.get_path(s)
            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it
            for neighbor in self.get_neighbors(s):
                if neighbor not in self.explored_set and neighbor not in self.frontier and not self.inside_body(snake, neighbor) and not self.outside_boundary(neighbor):
                    self.frontier.append(neighbor)
                    neighbor.parent = s
            self.explored_set.append(s)
        if len(self.path) == 0:
            for neighbor in self.get_neighbors(init_state):
                if not self.inside_body(snake, neighbor) and not self.outside_boundary(neighbor):
                    return neighbor
        #################################################################################