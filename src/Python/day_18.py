import math
from itertools import permutations

from aoc import get_lines


class Node:
    def __init__(self, left=None, right=None, value=None, parent=None, depth=0):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        self.depth = depth

    def print(self):
        print("[", end="")
        if self.left.value is not None:
            print(self.left.value, end="")
        else:
            self.left.print()
        print(",", end="")
        if self.right.value is not None:
            print(self.right.value, end="")
        else:
            self.right.print()
        print("]", end="")
        if self.depth == 0:
            print()

    def traverse(self, tree_list):
        if self.value is not None:
            tree_list.append(self)
        if self.left is not None:
            self.left.traverse(tree_list)
        if self.right is not None:
            self.right.traverse(tree_list)

    def set_parent(self):
        if self.left is not None:
            self.left.depth = self.depth + 1
            self.left.parent = self
            self.left.set_parent()
        if self.right is not None:
            self.right.depth = self.depth + 1
            self.right.parent = self
            self.right.set_parent()

    def get_magnitude(self):
        if self.value is not None:
            return self.value
        else:
            return 3 * self.left.get_magnitude() + 2 * self.right.get_magnitude()


def part_1(lines):
    cur_tree = None
    for line in lines:
        to_add = parse_tree(line)
        if cur_tree is None:
            cur_tree = to_add
        else:
            cur_tree = add_trees(cur_tree, to_add)
            do_actions(cur_tree)
    return cur_tree.get_magnitude()


def part_2(lines):
    max_mag = 0
    for i in permutations(lines, 2):
        cur_tree = add_trees(parse_tree(i[0]), parse_tree(i[1]))
        do_actions(cur_tree)
        max_mag = max(cur_tree.get_magnitude(), max_mag)
    return max_mag


def split(cur_node: Node) -> None:
    cur_node.left = Node(value=(cur_node.value // 2), depth=cur_node.depth + 1)
    cur_node.right = Node(value=(math.ceil(cur_node.value / 2)), depth=cur_node.depth + 1)
    cur_node.value = None
    cur_node.depth = cur_node.depth


def parse_tree(param: str, depth=0) -> Node:
    string_d = 0
    split_point = -1
    for i, c in enumerate(param):
        if c == "[":
            string_d += 1
        elif c == "]":
            string_d -= 1
        elif c == "," and string_d == 1:
            split_point = i
            break
    left = param[1:split_point]
    right = param[split_point + 1:-1]
    if left.isdecimal() and right.isdecimal():
        return Node(left=Node(value=int(left), depth=depth), right=Node(value=int(right), depth=depth), depth=depth)
    if left.isdecimal():
        return Node(left=Node(value=int(left), depth=depth), right=parse_tree(right, depth + 1), depth=depth)
    if right.isdecimal():
        return Node(left=parse_tree(left, depth + 1), right=Node(value=int(right), depth=depth))
    return Node(left=parse_tree(left, depth + 1), right=parse_tree(right, depth + 1), depth=depth)


def add_trees(tree: Node, new_tree: Node):
    return Node(left=tree, right=new_tree)


def do_actions(tree):
    found = True
    while found:
        tree.set_parent()
        found = False
        to_explode = None
        to_split = None
        left_neighbor = None
        right_neighbor = None
        tree_list = []
        tree.traverse(tree_list)
        for i, element in enumerate(tree_list):
            if element.depth > 4:
                found = True
                to_explode = element.parent
                if i > 0:
                    left_neighbor = tree_list[i - 1]
                if i + 2 < len(tree_list):
                    right_neighbor = tree_list[i + 2]
                break
            if element.value >= 10 and to_split is None:
                found = True
                to_split = element
        if to_explode is not None:
            explode(to_explode, left_neighbor, right_neighbor)
        elif to_split is not None:
            split(to_split)


def explode(node: Node, l_neighbor: Node, r_neighbor: Node):
    if l_neighbor is not None:
        l_neighbor.value += node.left.value
    if r_neighbor is not None:
        r_neighbor.value += node.right.value
    node.left = None
    node.right = None
    node.value = 0
    node.depth = node.depth - 1


def main():
    lines = get_lines("input_18.txt")
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
