import re

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
    return cur_point.y < target[0].y or cur_point.x > target[1].x


def undershot(cur_point, velocity, target):
    return velocity.x == 0 and cur_point.x < target[0].x


def part_1(target):
    maxy = 0
    perfrom_shot(target,Point(6,9))
    x_values = []
    for x in range(6, 200):
        ret = perfrom_shot((Point(target[0].x, 0), Point(target[1].x, 0)), Point(x, 0), True)
        if ret is not None:
            x_values.append(x)
    print(x_values)
    cnt = 0
    for x in x_values:
        for y in range(-500, 1000):
            velocity = Point(x, y)
            cmax = perfrom_shot(target, velocity)
            if cmax is not None:
                cnt += 1
                maxy = max(cmax,maxy)
    return maxy, cnt


def perfrom_shot(target, velocity, disabley=False):
    cur_point = Point(0, 0)
    points = [cur_point]
    for _ in range(5000):
        cur_point = add_points(cur_point, velocity)
        points.append(cur_point)
        if hit_target(cur_point, target):
            break
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
    return max(points, key=lambda p: p.y).y


def part_2(lines):
    pass


def main():
    lines = get_lines("input_17.txt")
    points = parse_input(lines)
    print(points)
    maxy, cnt = part_1(points)
    print("Part 1:", maxy)
    print("Part 2:", cnt)


if __name__ == '__main__':
    main()
