from snake.solver.base import BaseSolver
from snake.solver.path import PathSolver
from random import random


class RandomSolver(BaseSolver):

    def __init__(self, snake):
        super().__init__(snake)
        self._path_solver = PathSolver(snake)

    def next_direc(self):
        self._path_solver.snake = self.snake
        head = self.snake.head()
        rand = int(random() * 4)
        for _ in range(4):
            adj = head.all_adj()[rand]
            if self.map.is_safe(adj):
                break;
            rand = (rand + 1) % 4

        return head.direc_to(adj)
