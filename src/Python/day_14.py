from collections import Counter, defaultdict
from copy import copy, deepcopy
from pathlib import Path


def parse_input(lines):
    input = lines[0]
    insertion_dict = {}
    for line in lines[2:]:
        t = line.split('->')
        insertion_dict[t[0].strip()] = t[1].strip()

    return input,insertion_dict


def part_1(input,insertion_dict,rounds=10):
    for r in range(rounds):
        new_string = input[0]
        for i in range(0,len(input)-1,1):
            token = input[i:i+2]
            new_string += insertion_dict[token] + token[1]
        input = new_string
        counter = Counter(input)
    counter = counter.most_common(len(counter))
    return counter[0][1]-counter[-1][1]


def part_2(input,insertion_dict,rounds=40):
    result_dict = {}
    for k in insertion_dict.keys():
        result_dict[k] = 0
    for i in range(0, len(input) - 1, 1):
        result_dict[input[i:i + 2]]+=1
    for r in range(rounds):
        for k,v in list(result_dict.items()):
            if v > 0:
                result_dict[k] -=v
                result_dict[k[0]+insertion_dict[k]] += v
                result_dict[insertion_dict[k] + k[1]] += v

    counter = get_letter_count(input, result_dict)
    counter = counter.most_common(len(counter))
    return counter[0][1] - counter[-1][1]


def get_letter_count(input, result_dict):
    letter_count = defaultdict(int)
    for k, v in result_dict.items():
        letter_count[k[0]] += v
        letter_count[k[1]] += v
    letter_count[input[0]] += 1
    letter_count[input[-1]] += 1
    for k,v, in letter_count.items():
        letter_count[k] = v //2
    counter = Counter(letter_count)
    return counter


def main():
    file = Path(__file__).parents[2] / "inputs" / "input_14.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    input,insertion_dict = parse_input(lines)
    print("Part 1:", part_1(input,insertion_dict))
    print("Part 2:", part_2(input,insertion_dict))

#2304722022017 too low

if __name__ == '__main__':
    main()
