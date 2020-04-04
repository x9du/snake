from snake.solver.base import BaseSolver
from snake.solver.path import PathSolver


class AStarSolver(BaseSolver):
    def __init__(self, snake):
        super().__init__(snake)
        self._path_solver = PathSolver(snake)
        self.open_ = [Node(self.snake.head(), 0, self.snake.head())]
        self.closed_ = []
        self.least_node = self.open_[0]

    def astar(self):
        self.open_ = [Node(self.snake.head(), 0, self.snake.head())]
        self.closed_ = []
        self.least_node = self.open_[0]

    def g(self, pos):
        return 1
        # return len(self._path_solver.shortest_path_to_food())

    def h(self, pos):
        # create virtual snake with head at pos and create PathSolver for that snake
        # return length of shortest_path_to_food

        # Manhattan distance between pos and food
        return abs(pos.x - self.map.food.x) + abs(pos.y - self.map.food.y)

    def next_direc(self):
        if self.open_:
            self.open_.remove(self.least_node)
            for adj in self.least_node.pos.all_adj():
                print("(" + str(adj.x) + ", " + str(adj.y) + ")")
                if not self.map.is_safe(adj):
                    print("not safe")
                    continue
                if self.map.food.x == adj.x and self.map.food.y == adj.y:
                    self.astar()
                    return self.snake.head().direc_to(adj)
                flag = False
                f = self.g(adj) + self.h(adj)
                for node in self.open_:
                    if node.pos.x == adj.x and node.pos.y == adj.y and node.f < f:
                        flag = True
                        break
                for node in self.closed_:
                    if node.pos.x == adj.x and node.pos.y == adj.y and node.f < f:
                        flag = True
                        break
                if flag:
                    print("flag")
                    continue
                self.open_.append(Node(adj, self.g(adj) + self.h(adj), self.least_node))
                print("appended")
            self.closed_.append(self.least_node)
            if self.open_:
                self.least_node = self.open_[0]
                for node in self.open_:
                    if node.f < self.least_node.f:
                        self.least_node = node
                print("head (" + str(self.snake.head().x) + ", " + str(self.snake.head().y) + "), least_node (" + str(
                    self.least_node.pos.x) + ", " + str(self.least_node.pos.y) + ")")
                print(self.snake.head().direc_to(self.least_node.pos))
                return self.snake.head().direc_to(self.least_node.pos)
            else:
                return self.snake.direc


class Node:
    def __init__(self, pos, f, parent):
        self.pos = pos
        self.f = f
        self.parent = parent
