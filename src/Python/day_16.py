from collections import defaultdict
from functools import reduce
from itertools import groupby

from aoc import get_lines
from enum import Enum


class Field(Enum):
    Version = 1
    Id = 2
    Lateral = 3
    Length_Type_ID = 4
    N_Sub_Packets = 5
    Total_Length_Sub_Packet = 6
    Sub_Packet = 7
    Padding = 8


class Operations(Enum):
    Sum = 0
    Product = 1
    Minimum = 2
    Maximum = 3
    Value = 4
    GT = 5
    LT = 6
    EQ = 7
    OPEN = 8
    CLOSE = 9


class Sub_Packet_Type(Enum):
    Total = 1
    Length = 2
    No_Sub_Packet = 3


bit_lengths = {
    Field.Version: 3,
    Field.Id: 3,
    Field.Lateral: 5,
    Field.Length_Type_ID: 1,
    Field.N_Sub_Packets: 11,
    Field.Total_Length_Sub_Packet: 15,
    Field.Sub_Packet: 11

}


class Node:
    glob_id = 0

    def __init__(self, operation: Operations,depth=0, parent=None):
        self.operation = operation
        self.value = None
        self.parent = parent
        self.node_id = Node.glob_id
        self.n_sub_packets = None
        self.len_sub_packets = None
        self.depth = depth
        Node.glob_id += 1

    def __repr__(self):
        if self.parent is not None:
            return f"{self.node_id}({self.parent.node_id}):{self.operation} {self.value}"
        else:
            return f"{self.node_id}:{self.operation} {self.value}"


def parse_input(lines):
    return hex_to_bits(lines[0])


def consume_int(bitstream, n_bits):
    return bitstream[n_bits:], int(bitstream[:n_bits], 2)


def consume_raw(bitstream, n_bits):
    return bitstream[n_bits:], bitstream[:n_bits]


def part_1(bitstring):
    parse = Field.Version
    versions = []
    lateral_raw = ""
    depth = 0
    n_sub_packets = {}
    length_subpackets = []
    expr_dict = defaultdict(list)
    parse_next = None
    sub_packet_dict = {}
    parent_lookup = {}
    while len(bitstring) > 0:
        if bitstring.count('1') == 0:
            break
        consumed_bits = 0
        if parse == Field.Version:
            bitstring, version = consume_int(bitstring, bit_lengths[Field.Version])
            consumed_bits = bit_lengths[Field.Version]
            versions.append(version)
            parse_next = Field.Id
        elif parse == Field.Id:
            bitstring, type = consume_int(bitstring, bit_lengths[Field.Id])
            consumed_bits = bit_lengths[Field.Version]
            if type == 4:
                parse_next = Field.Lateral
            else:
                # operator
                parse_next = Field.Length_Type_ID
            if depth == 0:
                expr_dict[depth].append(Node(Operations(type),depth=0))
            else:
                cur_node = Node(Operations(type), parent=expr_dict[depth - 1][-1],depth = depth)
                parent_lookup[cur_node] = cur_node.parent
                expr_dict[depth].append(cur_node)
                if  expr_dict[depth][-1].node_id == 231:
                    print("debug")

        elif parse == Field.Lateral:
            bitstring, not_last = consume_int(bitstring, 1)
            bitstring, lval = consume_raw(bitstring, 4)
            lateral_raw += lval
            consumed_bits = bit_lengths[Field.Lateral]
            if not_last == 0:
                lateral = int(lateral_raw, 2)
                if lateral == 187:
                    print(lateral)
                expr_dict[depth][-1].value = lateral
                cur_node.value = lateral
                lateral_raw = ""
                parse_next = Field.Version
        elif parse == Field.Padding:
            consumed_bits = len(bitstring)
            bitstring, tmp = consume_raw(bitstring, consumed_bits)
        elif parse == Field.Length_Type_ID:
            consumed_bits = bit_lengths[Field.Length_Type_ID]
            bitstring, next = consume_int(bitstring, consumed_bits)
            if next == 1:
                parse_next = Field.N_Sub_Packets
            else:
                parse_next = Field.Total_Length_Sub_Packet
        elif parse == Field.N_Sub_Packets:
            consumed_bits = bit_lengths[Field.N_Sub_Packets]
            bitstring, val = consume_int(bitstring, consumed_bits)
            sub_packet_dict[expr_dict[depth][-1]] = val
            cur_node.n_sub_packets = val
            print("subpackets", val)
            # if operation_stack[-1] == Operations.GT:
            #     print("asd")
            depth += 1
            n_sub_packets[depth] = val
            parse_next = Field.Version
        elif parse == Field.Total_Length_Sub_Packet:
            consumed_bits = bit_lengths[Field.Total_Length_Sub_Packet]
            bitstring, length_subpacket = consume_int(bitstring, consumed_bits)
            print("length packets", length_subpacket)
            if length_subpacket == 27:
                print("asd")
            cur_node.len_sub_packets =length_subpacket
            length_subpackets.append(length_subpacket)
            parse_next = Field.Version
            depth += 1
        next = cur_node.parent
        while next is not None and next.len_sub_packets > 0:
            next.len_sub_packets -= consumed_bits
            next = next.parent
        # if depth > 0 and len(expr_dict[depth]) > 0:
        #     parent = expr_dict[depth][-1].parent
        # if len(length_subpackets) > 0:
        #     if not parse == Field.Total_Length_Sub_Packet:
        #         length_subpackets[-1] -= consumed_bits
        #     if len(length_subpackets) > 1:
        #         for i in range(len(length_subpackets) - 1):
        #             length_subpackets[i] -= consumed_bits
        #     for i in range(len(length_subpackets) - 1, -1, -1):
        #         if length_subpackets[i] == 0:
        #             length_subpackets.pop()
        #             print("finish",parse,parse_next)
        #             depth -= 1
        #
        # if parse == Field.Lateral and parse_next == Field.Version:
        #
        #     while True:
        #         if parent in sub_packet_dict:
        #             sub_packet_dict[parent] -= 1
        #             if sub_packet_dict[parent] == 0:
        #                 del sub_packet_dict[parent]
        #                 depth -= 1
        #             if parent in parent_lookup:
        #                 parent = parent_lookup[parent]
        #             else: break
        #         else:
        #             break
        #
        #
        #
        #     print("subpackets",sub_packet_dict)
            print(depth)
        parse = parse_next

    # print(versions)
    # print(expressions)
    # print(operation_stack)
    return sum(versions), expr_dict


def part_2(expr_dict):
    while len(expr_dict.keys()) > 1:
        keys = expr_dict.keys()
        depth = max(keys)
        for k, g in groupby(expr_dict[depth], key=lambda x: x.parent):
            g = list(g)
            if k.operation == Operations.LT:
                print("debug")
            result = calculate_expression(k.operation, [x.value for x in g])
            print(k)
            if depth > 0:
                idx = expr_dict[depth - 1].index(k)
                expr_dict[depth - 1][idx].value = result
                expr_dict[depth - 1][idx].operation = Operations.Value
            else:
                return result
        del expr_dict[depth]
    return expr_dict[0][0].value


def calculate_expression(operator, operands):
    if operator == Operations.Sum:
        return sum(operands)
    elif operator == Operations.Product:
        return reduce(lambda acc, x: acc * x, operands, 1)
    elif operator == Operations.Maximum:
        return max(operands)
    elif operator == Operations.Minimum:
        return min(operands)
    elif operator == Operations.GT:
        assert len(operands) == 2
        return int(operands[0] > operands[1])
    elif operator == Operations.LT:
        if len(operands) > 2:
            print(operands)
        assert len(operands) == 2
        return int(operands[0] < operands[1])
    elif operator == Operations.EQ:
        assert len(operands) == 2
        return int(operands[0] == operands[1])


def hex_to_bits(hex_stream):
    return ''.join([f"{int(h, 16):04b}" for h in hex_stream])


def test():
    _, stack = part_1(hex_to_bits("C200B40A82"))
    assert part_2(stack) == 3
    _, stack = part_1(hex_to_bits("04005AC33890"))
    assert part_2(stack) == 54
    _, stack = part_1(hex_to_bits("880086C3E88112"))
    assert part_2(stack) == 7
    _, stack = part_1(hex_to_bits("CE00C43D881120"))
    assert part_2(stack) == 9
    _, stack = part_1(hex_to_bits("D8005AC2A8F0"))
    assert part_2(stack) == 1
    _, stack = part_1(hex_to_bits("F600BC2D8F"))
    assert part_2(stack) == 0
    _, stack = part_1(hex_to_bits("9C005AC2F8F0"))
    assert part_2(stack) == 0
    _, stack = part_1(hex_to_bits("9C0141080250320F1802104A08"))
    assert part_2(stack) == 1
    result, _ = part_1(hex_to_bits("8A004A801A8002F478"))
    assert result == 16
    result, _ = part_1(hex_to_bits("620080001611562C8802118E34"))
    assert result == 12
    result, _ = part_1(hex_to_bits("C0015000016115A2E0802F182340"))
    assert result == 23
    result, _ = part_1(hex_to_bits("A0016C880162017C3686B18A3D4780"))
    assert result == 31


def main():
    test()
    lines = get_lines("input_16.txt")
    bit_string = parse_input(lines)
    res1, ostack = part_1(bit_string)
    print("Part 1:", res1)

    print("Part 2:", part_2(ostack))


if __name__ == '__main__':
    main()
