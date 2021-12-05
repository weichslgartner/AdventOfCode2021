#!/usr/bin/env python3
from pathlib import Path
from requests import get
from enum import Enum
from datetime import date


class Language(str, Enum):
    Python = "Python"
    Haskell = "Haskell"


extension = {Language.Python: "py", Language.Haskell: "hs"}

cookie = open(".cookie", 'r').readline().strip()
cookies = {'session': cookie}
year = 2021


def python_stub(day):
    return f"""from pathlib import Path


def parse_input(lines):
    return lines


def part_1(lines):
    pass


def part_2(lines):
    pass


def main():
    file = Path(__file__).parents[2] / "inputs" / "input_{day:02d}.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    lines = parse_input(lines)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
"""


def haskell_stub(day):
    return f"""
main = do  
    contents <- readFile "../../inputs/input_{day:02d}.txt"
    print . map readInt . words $ contents
readInt :: String -> Int
readInt = read
    """


def get_input(day: int):
    input_file = Path("inputs") / f"input_{day:02d}.txt"
    input_file.parent.mkdir(parents=True, exist_ok=True)
    if input_file.exists():
        return
    print(f"Fetching day {day}")
    raw_input = get(f"https://adventofcode.com/{year}/day/{day}/input", cookies=cookies)
    with input_file.open('w') as f:
        f.writelines(raw_input.content.decode('utf-8'))


def generate_stub(day: int, lang: Language):
    input_file = Path("src") / lang.name / f"day_{day:02d}.{extension[lang]}"
    input_file.parent.mkdir(parents=True, exist_ok=True)
    if input_file.exists():
        return
    print(f"Creating stub day {day} for {lang.name}")
    with input_file.open('w') as f:
        if lang == Language.Python:
            stub = python_stub(day)
        else:
            stub = haskell_stub(day)
        f.write(stub)


def main():
    today = date.today()
    print("Today is:", today)
    for day in range(1, 26):
        if today.year == year and (today.day < day or today.month != 12):
            break
        get_input(day)
        generate_stub(day, lang=Language.Python)
        generate_stub(day, lang=Language.Haskell)
    print("Done")


if __name__ == '__main__':
    main()
