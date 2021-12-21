from enum import Enum
from functools import reduce
from operator import mul
from typing import List

from aoc import get_lines


class Field(Enum):
    Version = 1
    Id = 2
    Lateral = 3
    Length_Type_ID = 4
    N_Sub_Packets = 5
    Total_Length_Sub_Packet = 6
    Sub_Packet = 7


class Operations(Enum):
    Sum = 0
    Product = 1
    Minimum = 2
    Maximum = 3
    Value = 4
    GT = 5
    LT = 6
    EQ = 7


bit_lengths = {
    Field.Version: 3,
    Field.Id: 3,
    Field.Lateral: 5,
    Field.Length_Type_ID: 1,
    Field.N_Sub_Packets: 11,
    Field.Total_Length_Sub_Packet: 15,
    Field.Sub_Packet: 11

}


def parse_input(lines: List[str]) -> str:
    return ''.join([f"{int(h, 16):04b}" for h in lines[0]])


def parse_packet(pos: int, version_sum: int, bitstring: str) -> (int, int, int):
    values = []
    cur_pos = pos
    version_sum += int(bitstring[cur_pos:pos + bit_lengths[Field.Version]], 2)
    cur_pos += bit_lengths[Field.Version]
    operation = Operations(int(bitstring[cur_pos:cur_pos + bit_lengths[Field.Id]], 2))
    cur_pos += bit_lengths[Field.Id]
    if operation == Operations.Value:
        not_last = '1'
        lateral = ""
        while not_last == "1":
            not_last = bitstring[cur_pos]
            cur_pos += 1
            lateral += bitstring[cur_pos:cur_pos + bit_lengths[Field.Lateral] - 1]
            cur_pos += bit_lengths[Field.Lateral] - 1
        return cur_pos, int(lateral, 2), version_sum
    else:
        length_type_id = bitstring[cur_pos]
        cur_pos += bit_lengths[Field.Length_Type_ID]
        if length_type_id == '1':
            n_sub_packets = int(bitstring[cur_pos:cur_pos + bit_lengths[Field.N_Sub_Packets]], 2)
            cur_pos += bit_lengths[Field.N_Sub_Packets]
            for _ in range(n_sub_packets):
                cur_pos, val, version_sum = parse_packet(pos=cur_pos, version_sum=version_sum, bitstring=bitstring)
                values.append(val)
        else:
            len_packets = int(bitstring[cur_pos:cur_pos + bit_lengths[Field.Total_Length_Sub_Packet]], 2)
            cur_pos += bit_lengths[Field.Total_Length_Sub_Packet]
            received = 0
            while received < len_packets:
                n_pos, val, version_sum = parse_packet(pos=cur_pos, version_sum=version_sum, bitstring=bitstring)
                received += n_pos - cur_pos
                cur_pos = n_pos
                values.append(val)
    return cur_pos, calculate_expression(operation, values=values), version_sum


def calculate_expression(operator: Operations, values: List[int]) -> int:
    if operator == Operations.Sum:
        return sum(values)
    elif operator == Operations.Product:
        return reduce(mul, values)
    elif operator == Operations.Maximum:
        return max(values)
    elif operator == Operations.Minimum:
        return min(values)
    elif operator == Operations.GT:
        assert len(values) == 2
        return int(values[0] > values[1])
    elif operator == Operations.LT:
        assert len(values) == 2
        return int(values[0] < values[1])
    elif operator == Operations.EQ:
        assert len(values) == 2
        return int(values[0] == values[1])


def part_1(bitstring: str) -> int:
    return parse_packet(pos=0, version_sum=0, bitstring=bitstring)[2]


def part_2(bitstring: str) -> int:
    return parse_packet(pos=0, version_sum=0, bitstring=bitstring)[1]


def main():
    lines = get_lines("input_16.txt")
    bitstring = parse_input(lines)
    _, result, version_sum = parse_packet(pos=0, version_sum=0, bitstring=bitstring)
    print("Part 1:", version_sum)
    print("Part 1:", result)


if __name__ == '__main__':
    main()
