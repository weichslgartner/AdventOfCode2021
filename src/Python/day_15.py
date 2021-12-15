import heapq

from aoc import get_lines, Point, get_neighbours_4, from_grid
from queue import PriorityQueue


def parse_input(lines):
    return [[int(x) for x in line.strip()] for line in lines]


def manhattan_dist(a : Point, b:Point):
    return abs(a.x - b.x) + abs(a.y - b.y)


def get_path(cur, cameFrom, grid):
    path = [from_grid(cur,grid)]
    while cur in cameFrom.keys():
        cur = cameFrom[cur]
        #print(cur)
        path.append(from_grid(cur,grid))
    return sum(path[:-1])


def part_1(grid):
    p_max = Point(len(grid[0]), len(grid))
    p_target = Point(p_max.x - 1, p_max.y - 1)
    start = Point(0, 0)
    q = []
    heapq.heappush(q,(0, start))
    in_queue = set()
    in_queue.add(start)
    cameFrom = {}
    costs = {}
    fcosts = {}
    for y in range(p_max.y):
        for x in range(p_max.x):
            costs[Point(x, y)] = 11111111111111111
            fcosts[Point(x, y)] = 11111111111111111
    costs[start] = 0
    fcosts[start] = manhattan_dist(start, p_target)
    while len(q) > 0:
        _,cur = heapq.heappop(q)
        in_queue.remove(cur)
        if cur == p_target:
            return get_path(cur, cameFrom,grid)
        for n in get_neighbours_4(cur, p_max):
            t_costs = costs[cur] + from_grid(n,grid)
            if t_costs < costs[n]:
                cameFrom[n] = cur
                costs[n] = t_costs
                fcosts[n] = t_costs + manhattan_dist(n, p_target)
                if n not in in_queue:
                    heapq.heappush(q,(fcosts[n], n))
                    in_queue.add(n)
    return -1


def part_2(lines):
    pass


def main():
    lines = get_lines("input_15.txt")
    lines = parse_input(lines)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
