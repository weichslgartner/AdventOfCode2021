from collections import Counter, namedtuple, defaultdict
from operator import mul

from aoc import get_lines
from pathlib import Path


def parse_input(lines):
    return [int(line.split(' ')[-1]) for line in lines if len(line) > 0]


def part_1(pos):
    scores = [0, 0]
    dice = 1
    dice_total = 0
    while True:
        for i in range(len(pos)):
            s = 0
            rolls = []
            for _ in range(3):
                if dice > 100:
                    dice = 1
                s += dice
                rolls.append(dice)
                dice += 1
            dice_total += 3
            pos[i] = wrap(pos[i] + s, 10)
            scores[i] += pos[i]
            # print(f"player {i} rolls {rolls} {s} moves to {pos[i]} scores {scores[i]}")
            if scores[i] >= 1000:
                return mul(dice_total, scores[0 if i == 1 else 1])


def wrap(val, base):
    quotient, remainder = divmod(val, base)
    if remainder > 0:
        return remainder
    return 10


class PScores(namedtuple('PScores', 'pos, score, times, rounds')):
    def __repr__(self):
        return f"{self.pos} {self.score} {self.times} {self.rounds}"


def part_2(pos):
    outcomes = []
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                outcomes.append([a, b, c])
    possible_sums = Counter(map(sum, outcomes))
    pos_scores = [PScores(pos[0], 0, 1, 0)]
    finished_rounds = defaultdict(int)
    while len(pos_scores) > 0:
        new_pos_scores = []
        for ps in pos_scores:
            for k, v in possible_sums.items():
                new_pos = wrap(ps.pos + k, 10)
                new_score = ps.score + new_pos
                if new_score >= 21:
                    finished_rounds[ps.rounds + 1] += ps.times * v
                else:
                    new_pos_scores.append(PScores(new_pos, new_score, ps.times * v, ps.rounds + 1))
        pos_scores = new_pos_scores
    print(finished_rounds)


def main():
    lines = get_lines("input_21_test.txt")
    lines = parse_input(lines)
 #   print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
