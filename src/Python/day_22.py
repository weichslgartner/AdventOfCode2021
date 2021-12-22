from functools import reduce

from aoc import get_lines,  Point3
import re

X_MIN = 0
X_MAX = 1
Y_MIN = 2
Y_MAX = 3
Z_MIN = 4
Z_MAX = 5


def calc_volume(points):
    return reduce(lambda acc, x: acc * x, map(lambda a: abs(a[1] - a[0]) + 1, zip(points[:-1:2], points[1::2])), 1)


def parse_input(lines):
    return [True if line.startswith("on") else False for line in lines], [list(map(int, re.findall(r"-?\d+", line))) for
                                                                          line in lines]


def part_1(on_off, cubes):
    points = set()
    for turn_on, cube in zip(on_off, cubes):
        if abs(cube[0]) > 50:
            continue
        cube_points = to_points(cube)
        if turn_on:
            points |= cube_points
        else:
            points -= cube_points
    return len(points)


def to_points(cube):
    points = set()
    for x in range(cube[0], cube[1] + 1):
        for y in range(cube[2], cube[3] + 1):
            for z in range(cube[4], cube[5] + 1):
                points.add(Point3(x, y, z))
    return points


def part_2(lines):
    pass


def get_overlap(cube1, cube2):
    x_overlap = None
    y_overlap = None
    z_overlap = None
    # x overlap 1
    if cube1[X_MIN] <= cube2[X_MIN] <= cube1[X_MAX]:
        x_overlap = [cube2[X_MIN], min(cube1[X_MAX], cube2[X_MAX])]
    if cube1[X_MIN] <= cube2[X_MAX] <= cube1[X_MAX]:
        x_overlap = [max(cube1[X_MIN], cube2[X_MIN]), cube2[X_MAX]]
    if cube1[Y_MIN] <= cube2[Y_MIN] <= cube1[Y_MAX]:
        y_overlap = [cube2[Y_MIN], min(cube1[Y_MAX], cube2[Y_MAX])]
    if cube1[Y_MIN] <= cube2[Y_MAX] <= cube1[Y_MAX]:
        y_overlap = [max(cube1[Y_MIN], cube2[Y_MIN]), cube2[Y_MAX]]
    if cube1[Z_MIN] <= cube2[Z_MIN] <= cube1[Z_MAX]:
        z_overlap = [cube2[Z_MIN], min(cube1[Z_MAX], cube2[Z_MAX])]
    if cube1[Z_MIN] <= cube2[Z_MAX] <= cube1[Z_MAX]:
        z_overlap = [max(cube1[Z_MIN], cube2[Z_MIN]), cube2[Z_MAX]]
    if x_overlap is not None and y_overlap is not None and z_overlap is not None:
        return x_overlap + y_overlap + z_overlap
    return None


def tests():
    assert calc_volume([10, 12, 10, 12, 10, 12]) == 27
    assert calc_volume([11, 13, 11, 13, 11, 13]) == 27
    assert calc_volume([10, 10, 10, 10, 10, 10]) == 1
    assert calc_volume([-10, -10, -10, -10, -10, -10]) == 1
    assert get_overlap([10, 10, 10, 10, 10, 10], [10, 10, 10, 10, 10, 10]) == [10, 10, 10, 10, 10, 10]
    assert get_overlap([10, 12, 10, 12, 10, 12], [11, 13, 11, 13, 11, 13]) == [11, 12, 11, 12, 11, 12]
    assert get_overlap([10, 10, 10, 10, 10, 10], [-10, -10, -10, -10, -10, -10]) is None
    assert get_overlap([10, 11, 10, 11, 10, 11], [10, 12, 10, 12, 10, 12]) == [10, 11, 10, 11, 10, 11]


def main():
    tests()
    lines = get_lines("input_22.txt")
    on_off, cubes = parse_input(lines)
    print("Part 1:", part_1(on_off, cubes))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
