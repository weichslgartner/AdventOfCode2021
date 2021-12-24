from collections import namedtuple
from functools import total_ordering
from heapq import heappop, heappush, heapify
from sys import maxsize
from typing import Dict

from src.Python.aoc import get_lines, Point

field = {Point(3, 1), Point(5, 1), Point(9, 2), Point(7, 1), Point(3, 3), Point(5, 3), Point(9, 1), Point(11, 1),
         Point(2, 1), Point(6, 1), Point(7, 3), Point(3, 2), Point(4, 1), Point(5, 2), Point(9, 3), Point(8, 1),
         Point(1, 1), Point(10, 1), Point(7, 2)}

MAX_X = 11
MIN_X = 1

holes = [3, 5, 7, 9]

possible_hallways = {p for p in field if p.y not in holes}


@total_ordering
class KeyDict(object):
    def __init__(self, key, dct):
        self.key = key
        self.dct = dct

    def __lt__(self, other):
        return self.key < other.key

    def __eq__(self, other):
        return self.key == other.key

    def __repr__(self):
        return '{0.__class__.__name__}(key={0.key}, dct={0.dct})'.format(self)

def get_route(src, dst):
    route = set()
    p = src
    while p != dst:
        if p.y == 1:
            if p.x > dst.x:
                p = Point(p.x - 1, p.y)
            elif p.x < dst.x:
                p = Point(p.x + 1, p.y)
            elif p.x == dst.x and p.y < dst.y:
                p = Point(p.x, p.y + 1)
            else:
                print("ERROR in route")
                return None
        elif p.y < dst.y:
            p = Point(p.x, p.y + 1)
        elif p.y > dst.y:
            p = Point(p.x, p.y - 1)
        else:
            print("ERROR in route")
            return None
        route.add(p)
    return route


mcosts = {'A': 1,
          'B': 10,
          'C': 100,
          'D': 1000}

targets = {'A': 3,
           'B': 5,
           'C': 7,
           'D': 9}


class Pod(namedtuple('Pod', 'type point')):
    def __repr__(self):
        return f'{self.type} {self.point}'


class State(namedtuple('State', 'pods, points')):
    def __repr__(self):
        return f'{self.pods} {self.pods}'


def print_pods(pods):
    for y in range(0, 5):
        for x in range(0, 13):
            p = Point(x, y)
            if p in pods:
                print(pods[p], end="")
            elif p in field:
                print(".", end="")
            else:
                print("#", end="")
        print()
    print()


def parse_input(lines):
    x = 0
    y = 0
    free_points = set()
    pods = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '.':
                free_points.add(Point(x, y))
            elif c in "ABCD":
                free_points.add(Point(x, y))
                pods[Point(x, y)] = c
    return free_points, pods


def possible_moves(pods: Dict[Point, str]):
    moves = []
    for k, v in pods.items():
        if k.y == 3:
            # already at destiny:
            if targets[v] == k.x:
                continue
            # can move up
            if Point(k.x, k.y - 1) not in pods:
                moves += move_to_hallway(k,v, pods)
        elif k.y == 2:
            # already at destiny:
            if targets[v] == k.x and Point(k.x, k.y + 1) in pods and pods[Point(k.x, k.y + 1)] == v:
                continue
            else:
                moves += move_to_hallway(k,v, pods)
        # in hallway, move to target
        else:
            if Point(targets[v], 3) not in pods and Point(targets[v], 2) not in pods:
                route = get_route(k, Point(targets[v], 3))
                if route & pods.keys() == set():
                    moves.append((k,Point(targets[v], 3),len(route)*mcosts[v]))
            elif Point(targets[v], 2) not in pods and Point(targets[v], 3) in pods and pods[Point(targets[v], 3)] == v:
                route = get_route(k, Point(targets[v], 2))
                if route & pods.keys() == set():
                    moves.append((k,Point(targets[v], 2),len(route)*mcosts[v]))
    # sort by costs
    moves.sort(key=lambda x: x[2])
    return moves


def move_to_hallway(point, type, pods):
    moves = []
    for x in range(MIN_X, MAX_X + 1):
        if x in holes:
            continue
        route = get_route(point, Point(x, 1))
        if route & pods.keys() == set():
            moves.append((point,Point(x, 1),len(route)*mcosts[type]))
    return moves

def is_finished(pods: Dict[Point, str]):
    for k,v in pods.items():
        if targets[v] != k.x:
            return False
    return True

def part_1(free_points, pods):
    queue = [KeyDict(0, pods)]
    heapify(queue)
    print_pods(pods)
    best_costs = {}
    best = maxsize
    solution = None
    while len(queue) > 0:
        kdic = heappop(queue)
        costs, cur = kdic.key, kdic.dct
        key = hash(frozenset(cur.items()))
        if key in best_costs and costs >= best_costs[key]:
            continue
        else:
            best_costs[key] = costs
        if is_finished(cur):
            if costs < best:
                best=costs
                solution = cur
            continue

        moves = possible_moves(cur)
        for mov in moves:
            new_pods = cur.copy()
            new_pods[mov[1]] = cur[mov[0]]
            del new_pods[mov[0]]
            heappush(queue,KeyDict(mov[2]+costs,new_pods))
    print(tuple(free_points), tuple(pods))
    print_pods(solution)
    return best

def part_2(lines):
    pass


def tests():
    r = get_route(Point(10, 1), Point(7, 3))
    print(r)


def main():
    tests()
    lines = get_lines("input_23.txt")
    free_points, pods = parse_input(lines)
    print("Part 1:", part_1(free_points, pods))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
