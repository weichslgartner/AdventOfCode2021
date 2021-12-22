from collections import Counter, namedtuple, defaultdict
from itertools import product, cycle
from typing import List

from aoc import get_lines, take


def parse_input(lines: List[str]) -> List[int]:
    return [int(line.split(' ')[-1]) for line in lines if len(line) > 0]


def part_1(pos: List[int], score_to_win: int = 1000) -> int:
    scores = [0, 0]
    dice_total = 0
    dice_cycle = cycle(range(1, 101))
    while True:
        for i in range(len(pos)):
            s = sum(take(3, dice_cycle))
            dice_total += 3
            pos[i] = wrap(pos[i] + s, 10)
            scores[i] += pos[i]
            if scores[i] >= score_to_win:
                return dice_total * scores[0 if i == 1 else 1]


def part_2(pos: List[int], score_to_win: int = 21) -> int:
    outcomes = [sum([a, b, c]) for c in range(1, 4) for b in range(1, 4) for a in range(1, 4)]
    possible_sums = Counter(outcomes)
    pos_scores = defaultdict(int)
    pos_scores[(PScores(pos[0], 0), PScores(pos[1], 0))] = 1
    possible_sums_two = {(p[0], p[1]): possible_sums[p[0]] * possible_sums[p[1]]
                         for p in product(possible_sums.keys(), possible_sums.keys())}
    player_1_wins = 0
    player_2_wins = 0
    while len(pos_scores) > 0:
        new_pos_scores = defaultdict(int)
        for ps, n_times in pos_scores.items():
            already_won = set()
            for k, v in possible_sums_two.items():
                if k[0] in already_won:
                    continue
                player1, player2 = ps
                new_pos_1 = wrap(player1.pos + k[0], 10)
                new_score_1 = player1.score + new_pos_1
                new_pos_2 = wrap(player2.pos + k[1], 10)
                new_score_2 = player2.score + new_pos_2
                n_universes = n_times * v
                if new_score_1 >= score_to_win:
                    player_1_wins += n_times * possible_sums[k[0]]
                    already_won.add(k[0])
                elif new_score_2 >= score_to_win:
                    player_2_wins += n_universes
                else:
                    new_pos_scores[(PScores(new_pos_1, new_score_1), PScores(new_pos_2, new_score_2))] += n_universes
        pos_scores = new_pos_scores
    return max(player_1_wins, player_2_wins)


def wrap(val: int, base: int) -> int:
    quotient, remainder = divmod(val, base)
    if remainder > 0:
        return remainder
    return base


class PScores(namedtuple('PScores', 'pos, score')):
    def __repr__(self):
        return f"{self.pos} {self.score}"


def main():
    lines = get_lines("input_21.txt")
    pos = parse_input(lines)
    print("Part 1:", part_1(pos.copy()))
    print("Part 2:", part_2(pos))


if __name__ == '__main__':
    main()
