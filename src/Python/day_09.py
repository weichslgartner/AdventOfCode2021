from collections import namedtuple
from functools import reduce
from pathlib import Path
from queue import SimpleQueue


class Point(namedtuple('Point', 'x y')):
    def __repr__(self):
        return f'{self.y} {self.x}'

def parse_input(lines):
    grid = []
    for line in lines:
        grid.append([int(x) for x in line.strip()])
    return grid


def get_neighbours(p :Point, ymax, xmax):
    points = []
    if p.x > 0:
        points.append(Point(p.x-1,p.y))
    if p.y > 0:
        points.append(Point(p.x,p.y-1))
    if p.x < xmax-1:
        points.append(Point(p.x+1,p.y))
    if p.y < ymax -1:
        points.append(Point(p.x,p.y+1))
    return points

def from_grid(p: Point, grid):
    return grid[p.y][p.x]

def part_1(grid):
    low_points = []
    for y,line in enumerate(grid):
        for x,val in enumerate(line):
            neighbors = get_neighbours(Point(x,y),len(grid),len(line))
            min_neigbor = min([from_grid(p,grid) for p in neighbors])
            if from_grid(Point(x,y),grid) < min_neigbor:
                low_points.append(Point(x,y))
    return sum(from_grid(p,grid) for p in low_points) + len(low_points), low_points


def part_2(grid, low_points):
    visited = set()
    basin_size = []
    for lp in low_points:
        basin_set = set()
        basin_set.add(lp)
        visited.add(lp)
        queue = SimpleQueue()
        queue.put(lp)
        while not queue.empty():
            to_check = set(get_neighbours(queue.get(), len(grid), len(grid[0]) )) - basin_set
            for p in to_check:
                if from_grid(p,grid ) != 9 and p not in visited:
                    queue.put(p)
                    visited.add(p)
                    basin_set.add(p)
        basin_size.append(len(basin_set))
    basin_size.sort(reverse=True)
    return reduce(lambda acc,x: acc*x ,basin_size[0:3] ,1)

def main():
    file = Path(__file__).parents[2] / "inputs" / "input_09.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    grid = parse_input(lines)
    result, low_points = part_1(grid)
    print("Part 1:", result)
    print("Part 2:", part_2(grid,low_points))


if __name__ == '__main__':
    main()
