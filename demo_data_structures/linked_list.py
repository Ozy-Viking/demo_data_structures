"""
linked_list.py

My first go at linked lists.

Author: Zack Hankin
Started: 17/02/2023
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any, Optional


@dataclass(slots=True)
class Node:
    """
    Node class for Linked List.
    """
    value: Any
    child: Optional[Node] = None

    def __repr__(self) -> str:
        ret_string: str = f"Node({self.value}"
        if not self.is_last:
            ret_string += f", {self.child.value}"
        ret_string += ")"
        return ret_string

    def __str__(self):
        return repr(self)

    def __iter__(self):
        return LinkedList(self)

    @property
    def is_last(self) -> bool:
        """
        Property to check if Node is last in list.

        Returns:
            True if last node.
        """
        return self.child is None

    def copy(self):
        new_node: Node = Node(self.value)
        if not self.is_last:
            new_node.child = self.child.copy()
        return new_node


class LinkedList:
    """
    Linked List class.
    """
    def __init__(self, node: Node, head: Optional[Node] = None) -> None:
        """
        Linked List class.

        Args:
            node (Node): Node in a linked list.
            head (Optional[Node]): if head is different to node.
        """
        if head is None:
            self.head: Node = node
        else:
            self.head: Node = head
        self._current: Node = node

    def __str__(self):
        ret_str: str = "LinkedList("
        for value in self:
            ret_str += f"{value.value}"
            if not value.is_last:
                ret_str += ", "
        ret_str += ")"
        return ret_str

    def __iter__(self):
        self._current = self.head
        return self

    def __next__(self):
        if self._current is None:
            raise StopIteration
        tmp = self._current
        self._current = self._current.child
        return tmp

    def __len__(self):
        count = 0
        for _ in self:
            count += 1
        return count

    def index(self, idx: int) -> Node:
        """
        Node at a given index.

        Args:
            idx (int): index of the node.

        Returns:
            Node at idx.
        """
        if idx < 0:
            idx += len(self)
        for i, node in enumerate(self):
            if idx == i:
                return node
        last_index = len(self) - 1
        raise IndexError(f"Index out of range. Last index: {last_index}. {idx = }")

    def __getitem__(self, key: int | slice) -> Node | LinkedList:
        if isinstance(key, int):
            return self.index(key)
        elif isinstance(key, slice):
            return self.slice(key.start, key.stop, key.step)

    def __delitem__(self, idx: int) -> None:
        if idx > 0:
            tmp_node = self.index(idx - 1)
            tmp_node.child = None
        else:
            self._current = None
            self.head = None

    @classmethod
    def generate(cls, *values) -> LinkedList:
        """
        Generates a linked list.

        Args:
            *values (): An iterable of values.

        Returns:
            Head of the Linked List
        """
        temp_list: list[Node] = []
        for idx, value in enumerate(iter(*values)):
            tmp = Node(value)
            temp_list.append(tmp)
        for idx, link in enumerate(temp_list[:-1]):
            link.child = temp_list[idx + 1]
        return cls(temp_list[0])

    def insert(self, value: Any, index: int = -1) -> LinkedList:
        """
        Insert value into a Linked List.

        Args:
            value (Any): Value of the node.
            index (int): Index of the node.

        Returns:
            The Linked List.
        """
        node = Node(value)
        temp_node = self.index(index)
        temp_node_child = temp_node.child
        temp_node.child = node
        node.child = temp_node_child
        return self

    def slice(self, start: int, end: int, step: int = 1) -> LinkedList:
        """
        Handles the slicing method.

        Args:
            start (int): Start index inclusive.
            end (int): End index exclusive.
            step (int): Step size.

        Returns:
            New linked list.
        """
        if step is None:
            step = 1

        temp_start = min(start, end)
        temp_end = max(start, end)
        tmp_ll = LinkedList(self.head.copy())

        if (step is not None and step < 0) or (start > end):
            reversed(tmp_ll)
            temp_start -= 1
            temp_end -= 1

        if temp_end is not None:
            tmp_ll.index(temp_end - 1).child = None
        if temp_start is not None:
            tmp_ll.head = tmp_ll.index(temp_start)
        if step is not None:
            tmp_ll.step(step)
        return tmp_ll

    def step(self, step: int = 1, linked_list: Optional[LinkedList] = None) -> LinkedList:
        """
        Handles the step method.

        Args:
            step (int): Step size.
            linked_list (Optional[LinkedList]): linked list to step through.

        Returns:
            Modified Linked List.
        """
        if linked_list is None:
            linked_list: LinkedList = self
        if step < 0:
            step = abs(step)
        tmp_node: Optional[Node] = None
        for idx, node in enumerate(linked_list):
            if idx == 0:
                tmp_node = node
            if idx % step == 0:
                tmp_node.child = node
                tmp_node = node
        tmp_node.child = None
        return linked_list

    def __reversed__(self):
        tmp_last: deque[Node | None] = deque([None, None], maxlen=2)
        for node in self:
            tmp_last.append(node)
            if tmp_last[1] is not None:
                tmp_last[1].child = tmp_last[0]
        else:
            self.head = tmp_last[1]
