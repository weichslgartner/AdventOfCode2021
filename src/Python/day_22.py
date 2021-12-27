from functools import reduce
from itertools import product

from aoc import get_lines, Point3
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
    return [True if line.startswith("on") else False for line in lines], \
           [list(map(int, re.findall(r"-?\d+", line))) for line in lines]


class Cube:
    def __init__(self, on=True, next_cube=None):
        self.on = on
        self.next = next_cube


def part_1(on_off, cubes):
    points = set()
    for turn_on, cube in zip(on_off, cubes):
        if abs(cube[0]) > 50:
            continue
        cube_points = to_points(cube)
        if turn_on:
            points |= cube_points
        else:
           # print(points - cube_points)
            points -= cube_points
        print(len(points))
    return len(points)


def to_points(cube):
    points = set()
    for x in range(cube[0], cube[1] + 1):
        for y in range(cube[2], cube[3] + 1):
            for z in range(cube[4], cube[5] + 1):
                points.add(Point3(x, y, z))
    return points


def part_2(on_off, cubes):
    points_debug_1 = set()
    points_debug_2 = set()
    cube_archive = set()
    n_turned = 0
    for turn_on, cube in zip(on_off, cubes):
        vol = calc_volume(cube)
        overlapped = []
        to_add = set()
        to_remove = set()
        new_on = []
        for other in cube_archive:
            overlap = get_overlap(cube, other)
            if overlap is not None:
                new_cubes = split_cubes(other, overlap)
                for c in new_cubes:
                    to_add.add(tuple(c))
                overlapped.append(overlap)
                to_remove.add(tuple(other))

        if turn_on:
           # points_debug_2 = to_points(cube)

            cube_archive.add(tuple(cube))
            if len(overlapped) >0:
                for o in overlapped:
                    # check if any new cubes overlap
                    vol -= calc_volume(o)
                    #points_debug_2 -= to_points(o)
            n_turned += vol
          #  if (to_points(cube) - points_debug_1) != (points_debug_2):
          #      print("debug")
          #  assert (to_points(cube) - points_debug_1) == (points_debug_2)

            points_debug_1 |= to_points(cube)
        else:
           # points_debug_1 = set()
          #  points_debug_2 = set()
            if len(overlapped) > 0:
                for o in overlapped:
                  #  print(to_points(o))
                    n_turned -= calc_volume(o)
                  #  points_debug_2 += to_points(o)
           # print(to_points(cube) & points_debug_1)
          #  print((points_debug_1 - to_points(cube)).intersection(points_debug_1))
         #   assert ( (points_debug_1 - to_points(cube)).intersection(points_debug_1)   ) == points_debug_2
          #  points_debug_1 -= to_points(cube)
        cube_archive |= to_add
        cube_archive -= to_remove
        print(n_turned)
    return n_turned


def split_cubes(cube, sub_cube):
    if sub_cube == cube:
        return cube
    assert cube[X_MIN] <= sub_cube[X_MIN] <= cube[X_MAX]
    assert cube[X_MIN] <= sub_cube[X_MAX] <= cube[X_MAX]
    x_section = [cube[X_MIN], sub_cube[X_MIN] - 1, sub_cube[X_MIN], sub_cube[X_MAX], sub_cube[X_MAX] + 1, cube[X_MAX]]
    if x_section[1] < x_section[0]:
        x_section = x_section[2:]
    if x_section[-2] > x_section[-1]:
        x_section = x_section[:-2]
    y_section = [cube[Y_MIN], sub_cube[Y_MIN] - 1, sub_cube[Y_MIN], sub_cube[Y_MAX], sub_cube[Y_MAX] + 1, cube[Y_MAX]]
    if y_section[1] < y_section[0]:
        y_section = y_section[2:]
    if y_section[-2] > y_section[-1]:
        y_section = y_section[:-2]
    z_section = [cube[Z_MIN], sub_cube[Z_MIN] - 1, sub_cube[Z_MIN], sub_cube[Z_MAX], sub_cube[Z_MAX] + 1, cube[Z_MAX]]
    if z_section[1] < z_section[0]:
        z_section = z_section[2:]
    if z_section[-2] > z_section[-1]:
        z_section = z_section[:-2]
    cubes = []
    for x1, x2 in zip(x_section[::2], x_section[1::2]):
        for y1, y2 in zip(y_section[::2], y_section[1::2]):
            for z1, z2 in zip(z_section[::2], z_section[1::2]):
                # don't add sub_subcube
                if not (x1 == sub_cube[X_MIN] and x2 == sub_cube[X_MAX] and
                        y1 == sub_cube[Y_MIN] and y2 == sub_cube[Y_MAX] and
                        z1 == sub_cube[Z_MIN] and z2 == sub_cube[Z_MAX]):
                    cubes.append([x1, x2, y1, y2, z1, z2])
    return cubes


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
    assert len(split_cubes([10, 12, 10, 12, 10, 12], sub_cube=[10, 11, 10, 11, 10, 11])) == 7
    assert len(split_cubes([10, 13, 10, 13, 10, 13], sub_cube=[11, 11, 11, 11, 11, 11])) == 26


def main():
    tests()
    lines = get_lines("input_22_test1.txt")
    on_off, cubes = parse_input(lines)
    print("Part 1:", part_1(on_off, cubes))
    print("Part 2:", part_2(on_off, cubes))


if __name__ == '__main__':
    main()
