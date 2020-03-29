from snake.solver.base import BaseSolver
from snake.base.direc import Direc
from collections import deque


class AlmightySolver(BaseSolver):
    i = -1

    def __init__(self, snake):
        super().__init__(snake)

    def _build_almighty_path(self):
        path = []
        for _ in range(4):
            path.append(Direc.RIGHT)
        for _ in range(7):
            path.append(Direc.DOWN)
        path.append(Direc.LEFT)
        for _ in range(3):
            for _ in range(6):
                path.append(Direc.UP)
            path.append(Direc.LEFT)
            for _ in range(6):
                path.append(Direc.DOWN)
            path.append(Direc.LEFT)
        for _ in range(7):
            path.append(Direc.UP)
        for _ in range(3):
            path.append(Direc.RIGHT)
        return path


    def next_direc(self):
        head = self.snake.head()
        path = self._build_almighty_path()
        self.i = (self.i + 1) % len(path)
        return path[self.i]
