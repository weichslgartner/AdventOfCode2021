from collections import Counter, namedtuple, defaultdict
from itertools import product
from operator import mul

from aoc import get_lines


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
            if scores[i] >= 1000:
                return mul(dice_total, scores[0 if i == 1 else 1])


def wrap(val, base):
    quotient, remainder = divmod(val, base)
    if remainder > 0:
        return remainder
    return base


class PScores(namedtuple('PScores', 'pos, score')):
    def __repr__(self):
        return f"{self.pos} {self.score} {self.times}"


def part_2(pos):
    outcomes = []
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                outcomes.append([a, b, c])
    possible_sums = Counter(map(sum, outcomes))
    possible_sums_two = {}
    pos_scores = defaultdict(int)
    pos_scores[(PScores(pos[0], 0), PScores(pos[1], 0))] = 1
    for p in product(possible_sums.keys(), possible_sums.keys()):
        #print((p[0],p[1]),possible_sums[p[0]]*possible_sums[p[1]])
        possible_sums_two[(p[0],p[1])] = possible_sums[p[0]]*possible_sums[p[1]]
    #print(sum(possible_sums_two.values()))
    player_1_wins = 0
    player_2_wins = 0
    for round in range(12):
        print(round)
        new_pos_scores = defaultdict(int)
        for ps, n_times in pos_scores.items():
            for k, v in possible_sums_two.items():
                player1, player2 = ps
                new_pos_1 = wrap(player1.pos + k[0], 10)
                new_score_1 = player1.score + new_pos_1
                new_pos_2 = wrap(player2.pos + k[1], 10)
                new_score_2 = player2.score + new_pos_2
                n_universes = n_times * v
                if new_score_1 >= 21:
                    player_1_wins += n_universes
                elif new_score_2 >= 21:
                    player_2_wins += n_universes
                else:
                    new_pos_scores[(PScores(new_pos_1, new_score_1) , PScores(new_pos_2, new_score_2))] += n_universes
        pos_scores = new_pos_scores
    return (player_1_wins,player_2_wins)



def main():
    lines = get_lines("input_21_test.txt")
    pos = parse_input(lines)
    print("Part 1:", part_1(pos.copy()))
    print("Part 2:", part_2(pos))


if __name__ == '__main__':
    main()
