import re
from math import sqrt
from typing import Tuple

from aoc import get_lines, Point


def parse_input(lines):
    nums = re.findall('[-]*\\d+', lines.pop(0))
    nums = [int(n) for n in nums]
    return Point(nums[0], nums[2]), Point(nums[1], nums[3])


def add_points(a, b):
    return Point(a.x + b.x, a.y + b.y)


def hit_target(cur_point, target):
    return target[0].x <= cur_point.x <= target[1].x and \
           target[0].y <= cur_point.y <= target[1].y


def overshot(cur_point, target):
    return cur_point.x > target[1].x


def undershot(cur_point : Point, velocity : Point, target : Tuple[Point,Point]):
    return (velocity.x == 0 and cur_point.x < target[0].x) or (cur_point.y < target[0].y)


def part_1(target):
    maxy = 0
    x_values = []
    for x_ in range(int(sqrt(target[0].x)) + 1, target[1].x):
        ret = perform_shot((Point(target[0].x, 0), Point(target[1].x, 0)), Point(x=x_, y=0), True)
        if ret is not None:
            x_values.append(x_)
    cnt = 0
    for x in x_values:
        for y in range(-300, 200):
            cmax = perform_shot(target, Point(x, y))
            if cmax is not None:
                cnt += 1
                maxy = max(cmax, maxy)
    return maxy, cnt


def perform_shot(target, velocity, disabley=False):
    cur_point = Point(0, 0)
    maxy = 0
    for _ in range(5000):
        cur_point = add_points(cur_point, velocity)
        maxy = max(cur_point.y, maxy)
        if hit_target(cur_point, target):
            return maxy
        if overshot(cur_point, target):
            return None
        if undershot(cur_point, velocity, target):
            return None
        x, y = velocity
        if x > 0:
            x -= 1
        elif x < 0:
            x += 1
        if not disabley:
            y -= 1
        velocity = Point(x, y)
    return None


def main():
    lines = get_lines("input_17.txt")
    points = parse_input(lines)
    maxy, cnt = part_1(points)
    print("Part 1:", maxy)
    print("Part 2:", cnt)


if __name__ == '__main__':
    main()
