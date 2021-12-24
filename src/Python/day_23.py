from functools import total_ordering
from heapq import heappop, heappush
from sys import maxsize
from typing import Dict, Optional, Set, List, Tuple

from aoc import get_lines, Point

m_costs = {'A': 1,
           'B': 10,
           'C': 100,
           'D': 1000}

targets = {'A': 3,
           'B': 5,
           'C': 7,
           'D': 9}

MAX_X = 11
MIN_X = 1

holes = set()  # {3, 5, 7, 9}


@total_ordering
class CostPods(object):
    def __init__(self, costs: int, pods: Dict[Point, str]):
        self.costs = costs
        self.pods = pods

    def __lt__(self, other):
        return self.costs < other.costs

    def __eq__(self, other):
        return self.costs == other.costs

    def __repr__(self):
        return f"{self.costs} {self.pods}"

    def __hash__(self):
        return hash(frozenset(self.pods.items()))


def get_route(src: Point, dst: Point, pods: Dict[Point, str]) -> Optional[Set[Point]]:
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
        if p in pods:
            return None
        route.add(p)
    return route


def print_pods(pods: Dict[Point, str]):
    field = {Point(3, 1), Point(5, 1), Point(9, 2), Point(7, 1), Point(3, 3), Point(5, 3), Point(9, 1), Point(11, 1),
             Point(2, 1), Point(6, 1), Point(7, 3), Point(3, 2), Point(4, 1), Point(5, 2), Point(9, 3), Point(8, 1),
             Point(1, 1), Point(10, 1), Point(7, 2)}
    for y in range(0, 7):
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


def parse_input(lines: List[str]) -> Dict[Point, str]:
    global MIN_X, MAX_X
    free_points = set()
    pods = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '.':
                free_points.add(Point(x, y))
                MIN_X = min(x, MIN_X)
                MAX_X = max(x, MAX_X)
            elif c in "ABCD":
                free_points.add(Point(x, y))
                pods[Point(x, y)] = c
                holes.add(x)
    return pods


def part_1(pods: Dict[Point, str]) -> int:
    return solve(pods, max(pods.keys(), key=lambda p: p.y).y)


def part_2(pods: Dict[Point, str]) -> int:
    return solve(pods, max(pods.keys(), key=lambda p: p.y).y)


def solve(pods, y_max, d_print=False) -> int:
    queue = [CostPods(0, pods)]
    if d_print:
        print_pods(pods)
    best_costs = {}
    best = maxsize
    solution = None
    while len(queue) > 0:
        elem = heappop(queue)
        if elem.costs >= best:
            continue
        if elem in best_costs and elem.costs >= best_costs[elem]:
            continue
        else:
            best_costs[elem] = elem.costs
        if is_finished(elem.pods):
            if elem.costs < best:
                best = elem.costs
                solution = elem.pods.copy()
            continue
        moves = possible_moves(elem.pods, max_y=y_max)
        for mov in moves:
            new_pods = elem.pods.copy()
            new_pods[mov[1]] = elem.pods[mov[0]]
            del new_pods[mov[0]]
            heappush(queue, CostPods(mov[2] + elem.costs, new_pods))
    if d_print:
        print_pods(solution)
    return best


def possible_moves(pods: Dict[Point, str], max_y=5) -> List[Tuple[Point, Point, int]]:
    moves = []
    for k, v in pods.items():
        # is in hole, stay there or move to hallway
        if k.y > 1:
            already_at_target = True
            for y in range(k.y, max_y + 1):
                p = Point(k.x, y)
                if p not in pods:
                    already_at_target = False
                    break
                if k.x != targets[pods[p]]:
                    already_at_target = False
                    break
            # already at destiny:
            if already_at_target:
                continue
            # can possibly move up
            moves += move_to_hallway(k, v, pods)
        # in hallway, move to target
        else:
            for y in range(2, max_y + 1):
                if Point(targets[v], y) not in pods:
                    if y != max_y and not check_below(max_y, pods, v, y):
                        continue
                    route = get_route(k, Point(targets[v], y), pods=pods)
                    if route and route & pods.keys() == set():
                        moves.append((k, Point(targets[v], y), len(route) * m_costs[v]))
    return moves


def check_below(max_y: int, pods: Dict[Point, str], v: str, y: int) -> bool:
    for y_ in range(y + 1, max_y + 1):
        p = Point(targets[v], y_)
        if p not in pods:
            return False
        if pods[p] != v:
            return False
    return True


def move_to_hallway(point: Point, ptype, pods) -> List[Tuple[Point, Point, int]]:
    moves = []
    for x in range(MIN_X, MAX_X + 1):
        if x in holes:
            continue
        route = get_route(point, Point(x, 1), pods)
        if route and route & pods.keys() == set():
            moves.append((point, Point(x, 1), len(route) * m_costs[ptype]))
    return moves


def is_finished(pods: Dict[Point, str]) -> bool:
    for k, v in pods.items():
        if targets[v] != k.x:
            return False
    return True


def main():
    lines = get_lines("input_23_test.txt")
    pods = parse_input(lines)
    print("Part 1:", part_1(pods))
    lines = get_lines("input_23_part2.txt")
    pods = parse_input(lines)
    print("Part 2:", part_2(pods))


if __name__ == '__main__':
    main()
