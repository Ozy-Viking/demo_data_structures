"""
__main__.py



Author: Zack Hankin
Started: 17/02/2023
"""
from __future__ import annotations

from icecream import ic
from .heap import Heap, Node


def main() -> int:
    t = range(5)
    tree = Heap.generate(Node(4), Node(2))
    tree.max_heap()
    ic(tree)  # .check_heap())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
