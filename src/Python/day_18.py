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
            self.left.depth = self.depth + 1
            self.left.parent = self
            self.left.traverse(tree_list)
        if self.right is not None:
            self.right.parent = self
            self.right.depth = self.depth + 1
            self.right.traverse(tree_list)

    def copy(self):
        if self.left is None and self.right is None:
            return Node(value=self.value, left=None, right=None, depth=self.depth)
        elif self.left is None:
            return Node(value=self.value, left=None, right=self.right.copy(), depth=self.depth)
        elif self.right is None:
            return Node(value=self.value, left=self.left.copy(), right=None, depth=self.depth)
        return Node(value=self.value, left=self.left.copy(), right=self.right.copy(), depth=self.depth)

    def get_magnitude(self):
        if self.value is not None:
            return self.value
        else:
            return 3 * self.left.get_magnitude() + 2 * self.right.get_magnitude()


def part_1(trees):
    cur_tree = None
    for tree in trees:
        to_add = tree
        if cur_tree is None:
            cur_tree = to_add.copy()
        else:
            cur_tree = add_trees(cur_tree, to_add.copy())
            reduce(cur_tree)
    return cur_tree.get_magnitude()


def part_2(trees):
    max_mag = 0
    i = 0
    for tree in list(permutations(trees, 2)):
        cur_tree = add_trees(tree[0].copy(), tree[1].copy())
        reduce(cur_tree)
        max_mag = max(cur_tree.get_magnitude(), max_mag)
        i += 1
    return max_mag


def split(cur_node: Node) -> None:
    cur_node.left = Node(value=(cur_node.value // 2), depth=cur_node.depth + 1)
    cur_node.right = Node(value=(math.ceil(cur_node.value / 2)), depth=cur_node.depth + 1)
    cur_node.value = None


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
        return Node(left=Node(value=int(left), depth=depth + 1), right=Node(value=int(right), depth=depth + 1),
                    depth=depth)
    if left.isdecimal():
        return Node(left=Node(value=int(left), depth=depth + 1), right=parse_tree(right, depth + 1), depth=depth)
    if right.isdecimal():
        return Node(left=parse_tree(left, depth + 1), right=Node(value=int(right), depth=depth), depth=depth)
    return Node(left=parse_tree(left, depth + 1), right=parse_tree(right, depth + 1), depth=depth)


def add_trees(tree: Node, new_tree: Node):
    return Node(left=tree, right=new_tree)


def reduce(tree):
    found = True
    while found:
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


def parse_lines(lines):
    return [parse_tree(line) for line in lines]


def main():
    lines = get_lines("input_18.txt")
    trees = parse_lines(lines)
    print("Part 1:", part_1(trees))
    print("Part 2:", part_2(trees))


if __name__ == '__main__':
    main()
