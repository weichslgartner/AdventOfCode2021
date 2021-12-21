from operator import mul

from aoc import get_lines
from pathlib import Path


def parse_input(lines):
    return [int(line.split(' ')[-1]) for line in lines if len(line)>0]


def part_1(pos):
    scores = [0,0]
    dice = 1
    dice_total = 0
    while True:
        for i in range(len(pos)):
            s = 0
            rolls = []
            for _ in range(3):
                if dice > 100:
                    dice =1
                s+= dice
                rolls.append(dice)
                dice += 1
            dice_total +=3
            pos[i] = wrap(pos[i]+ s,10)
            scores[i] +=pos[i]
           # print(f"player {i} rolls {rolls} {s} moves to {pos[i]} scores {scores[i]}")
            if scores[i] >= 1000:
                return mul(dice_total,scores[0 if i==1 else 1])


def wrap(val, base):
    quotient, remainder = divmod(val, base)
    if quotient >= 1 and remainder > 0:
        val = remainder
    elif remainder == 0:
        val = 10
    return val


def part_2(lines):
    pass


def main():
    lines = get_lines("input_21.txt")
    lines = parse_input(lines)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
