import math

from snake.base import Direc, Pos, Map, Point
from snake.solver.base import BaseSolver
from snake.solver.path import PathSolver


class AStarSolver(BaseSolver):
    def __init__(self, snake):
        super().__init__(snake)
        self._path_solver = PathSolver(snake)
        self.open_ = [Node(self.snake.head(), 0, 0, 0, self.snake.head())]
        self.closed_ = []
        self.closed_dict = {}
        self.flag_new = True
        self.path = []

    def g(self, parent):
        return parent.g + 1

    def h(self, pos):
        # Manhattan distance between pos and food
        return abs(pos.x - self.map.food.x) + abs(pos.y - self.map.food.y)

        # Euclidean distance between pos and food
        # return math.sqrt(abs(pos.x - self.map.food.x) ** 2 + abs(pos.y - self.map.food.y) ** 2)

    def append_(self, node, list_):
        for i in range(len(list_)):
            if node.f < list_[i].f:
                list_.insert(i, node)
                return 1
            elif node.f == list_[i].f and node.g + self.euclidean_dist(node.pos, self.map.food) <= list_[i].g + self.euclidean_dist(list_[i].pos, self.map.food):
                list_.insert(i, node)
                return 1
        list_.append(node)
        return 1

    def euclidean_dist(self, pos1, pos2):
        return math.sqrt(abs(pos1.x - pos2.x) ** 2 + abs(pos1.y - pos2.y) ** 2)

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

    def get_path(self, pos1, pos2):
        path = []
        while pos1.x != pos2.x or pos1.y != pos2.y:
            path.insert(0, pos2)
            pos2 = self.closed_dict[pos2].parent
        return path

    def next_direc(self):
        head = self.snake.head()
        if self.flag_new:
            self.open_ = [Node(self.snake.head(), 0, 0, 0, self.snake.head())]
            self.closed_ = []
            self.closed_dict = {}
            self.path = []
        else:
            if len(self.path) == 0:
                print(self.snake.direc)
                return self.snake.direc
            elif len(self.path) > 1:
                next_pos = self.path[0]
                self.path.pop(0)
                print(head.direc_to(next_pos))
                return head.direc_to(next_pos)
            else:
                next_pos = self.path[0]
                self.path.pop(0)
                print(head.direc_to(next_pos))
                print()
                self.flag_new = True
                return head.direc_to(next_pos)
        self.flag_new = False
        while self.open_:
            least_node = self.open_[0]
            self.open_.remove(least_node)
            print("head (%d, %d), least_node %d(%d, %d)" % (head.x, head.y, least_node.f, least_node.pos.x, least_node.pos.y))
            self.print_list_f(self.open_)
            self.print_list(self.closed_)
            for adj in least_node.pos.all_adj():
                print("(" + str(adj.x) + ", " + str(adj.y) + ")", end=" ")
                if not self.map.is_safe(adj):
                    print("not safe")
                    continue
                g = self.g(least_node)
                h = self.h(adj)
                f = g + h
                print("%d = %d + %d" % (f, g, h), end=" ")
                adj_node = Node(adj, g, h, f, least_node.pos)
                if self.map.food.x == adj.x and self.map.food.y == adj.y:
                    self.append_(least_node, self.closed_)
                    self.closed_dict[least_node.pos] = least_node
                    least_node = adj_node
                    print("FOOD")
                    print("head (%d, %d), least_node %d(%d, %d)" % (head.x, head.y, least_node.f, least_node.pos.x, least_node.pos.y))
                    self.print_list_f(self.open_)
                    self.print_list(self.closed_)
                    self.append_(least_node, self.closed_)
                    self.closed_dict[least_node.pos] = least_node
                    self.path = self.get_path(head, adj)
                    print(self.path)
                    if len(self.path) > 1:
                        next_pos = self.path[0]
                        self.path.pop(0)
                        print(head.direc_to(next_pos))
                        return head.direc_to(next_pos)
                    else:
                        next_pos = self.path[0]
                        self.path.pop(0)
                        print(head.direc_to(next_pos))
                        print()
                        self.flag_new = True
                        return head.direc_to(next_pos)
                flag = False
                for i in range(len(self.open_)):
                    node = self.open_[i]
                    if node.pos.x == adj.x and node.pos.y == adj.y:
                        if node.f < f:
                            flag = True
                        else:
                            self.open_.pop(i)
                        break
                for i in range(len(self.closed_)):
                    node = self.closed_[i]
                    if node.pos.x == adj.x and node.pos.y == adj.y:
                        if node.f < f:
                            flag = True
                        else:
                            self.closed_dict[node.pos] = adj_node
                            # self.closed_.pop(i)
                        break
                if flag:
                    print("flag")
                    continue
                self.append_(adj_node, self.open_)
                print("appended")
            self.append_(least_node, self.closed_)
            self.closed_dict[least_node.pos] = least_node
        print("No path")
        self.flag_new = True
        self._path_solver.snake = self.snake
        path_to_tail = self._path_solver.longest_path_to_tail()
        if len(path_to_tail) > 0:
            print(path_to_tail[0])
            return path_to_tail[0]
        else:
            for adj in head.all_adj():
                if self.map.is_safe(adj):
                    print(head.direc_to(adj))
                    return head.direc_to(adj)
            print(self.snake.direc)
            return self.snake.direc


class Node:
    def __init__(self, pos, g, h, f, parent):
        self.pos = pos
        self.g = g
        self.h = h
        self.f = f
        self.parent = parent
