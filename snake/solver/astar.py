import math

from snake.base import Direc, Pos, Map, Point
from snake.solver.base import BaseSolver
from snake.solver.path import PathSolver


class AStarSolver(BaseSolver):
    def __init__(self, snake):
        super().__init__(snake)
        # self._path_solver = PathSolver(snake)
        self.open_ = [Node(self.snake.head(), 0, self.snake.head())]
        self.closed_ = []
        self.least_node = self.open_[0]
        self.flag_new = True
        self.path_len = -1

    def astar(self):
        self.open_ = [Node(self.snake.head(), 0, self.snake.head())]
        self.closed_ = []
        self.least_node = self.open_[0]
        self.path_len = -1

    def g(self, pos):
        return self.path_len + 1
        # return len(self._path_solver.shortest_path_to_food())

    def h(self, pos):
        # create virtual snake with head at pos and create PathSolver for that snake
        # return length of shortest_path_to_food

        # Manhattan distance between pos and food
        # return abs(pos.x - self.map.food.x) + abs(pos.y - self.map.food.y)

        # Euclidean distance between pos and food
        return math.sqrt(abs(pos.x - self.map.food.x) ** 2 + abs(pos.y - self.map.food.y) ** 2)

    def print_list(self, list_):
        print("[", end = "")
        for node in list_:
            print("(%d, %d)" % (node.pos.x, node.pos.y), end = " ")
        print("\b]")

    def print_list_f(self, list_):
        print("[", end="")
        for node in list_:
            print("%d(%d, %d)" % (node.f, node.pos.x, node.pos.y), end=" ")
        print("\b]")

    def next_direc(self):
        # head = self.snake.head()
        self.path_len + 1
        if self.flag_new:
            self.astar()
        self.flag_new = False
        if self.open_:
            self.open_.remove(self.least_node)
            for adj in self.least_node.pos.all_adj():
                print("(" + str(adj.x) + ", " + str(adj.y) + ")", end = " ")
                if not self.map.is_safe(adj):
                    print("not safe")
                    continue
                if self.map.food.x == adj.x and self.map.food.y == adj.y:
                    self.least_node = Node(adj, 1, self.least_node)
                    print("FOOD")
                    print("head (%d, %d), least_node %d(%d, %d)" % (self.snake.head().x, self.snake.head().y, self.least_node.f, self.least_node.pos.x, self.least_node.pos.y))
                    print(self.snake.head().direc_to(adj))
                    self.print_list_f(self.open_)
                    self.print_list(self.closed_)
                    print()
                    self.flag_new = True
                    return self.snake.head().direc_to(adj)
                flag = False
                open_dupe = -1
                f = self.g(adj) + self.h(adj)
                for i in range(len(self.open_)):
                    node = self.open_[i]
                    if node.pos.x == adj.x and node.pos.y == adj.y:
                        if node.f < f:
                            flag = True
                        else:
                            open_dupe = i
                        break
                for node in self.closed_:
                    if node.pos.x == adj.x and node.pos.y == adj.y and node.f < f:
                        flag = True
                        break
                if flag:
                    print("flag")
                    continue
                if open_dupe != -1:
                    self.open_.pop(open_dupe)
                self.open_.append(Node(adj, self.g(adj) + self.h(adj), self.least_node))
                print("appended")
            self.closed_.append(self.least_node)
            if self.open_:
                self.least_node = self.open_[0]
                for node in self.open_:
                    if node.f < self.least_node.f:
                        self.least_node = node
                print("head (%d, %d), least_node %d(%d, %d)" % (self.snake.head().x, self.snake.head().y, self.least_node.f, self.least_node.pos.x, self.least_node.pos.y))
                print(self.snake.head().direc_to(self.least_node.pos))
                self.print_list_f(self.open_)
                self.print_list(self.closed_)
                if self.snake.head().direc_to(self.least_node.pos) == Direc.NONE:
                    print(self.snake.direc)
                    return self.snake.direc
                    # direc = Direc.RIGHT
                    # flag_safe = True
                    # if self.least_node.pos.x < head.x:
                    #     for i in range(1, abs(self.least_node.pos.x - head.x) + 1):
                    #         x = self.head.x - i
                    #         y = self.head.y
                    #         # if snake will run into its tail
                    #         if Map.is_snake(Map.point(Pos(x, y)).type) and i - Pos.manhattan_dist(Pos(x, y), self.snake.tail()) <= 0:
                    #             flag_safe = False
                    #             break;
                    #     if flag_safe:
                    #         direc = Direc.UP
                    #     elif self.least_node.pos.y < head.y:
                    #         direc = Direc.LEFT
                    # else:
                    #     flag_safe = True
                    #     if flag_safe:
                    #         direc = Direc.DOWN
                    #     elif self.least_node.pos.y < head.y:
                    #         direc = Direc.LEFT
                    # print(direc)
                    # return direc
                return self.snake.head().direc_to(self.least_node.pos)
            else:
                print("Default to ", end = "")
                print(self.snake.direc)
                return self.snake.direc


class Node:
    def __init__(self, pos, f, parent):
        self.pos = pos
        self.f = f
        self.parent = parent
