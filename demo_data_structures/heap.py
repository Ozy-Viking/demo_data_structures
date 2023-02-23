"""
heap.py



Author: Zack Hankin
Started: 17/02/2023
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Literal, Optional


@dataclass
class Node:
    """
    Node for a heap.
    """

    value: Optional[Any] = field(default=None)
    left: Optional[Any] = field(default=None)
    right: Optional[Any] = field(default=None)

    def __post_init__(self):
        if isinstance(self.value, Node):
            self.value = self.value.value

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Node):
            return self.value < other.value
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Node):
            return self.value == other.value
        return NotImplemented

    def __repr__(self) -> str:
        ret_str: str = f"Node(value={self.value}"
        if self.left:
            ret_str += f", left={self.left.value}"
        if self.right:
            ret_str += f", right={self.right.value}"
        return ret_str + ")"

    def __str__(self) -> str:
        return repr(self)


class Heap:
    """
    Heap object.
    """
    def __init__(
        self,
        head: Optional[Node] = None,
        heap_type: Literal["Max"] | Literal["Min"] = "Max",
    ):
        self.head = head
        self._current: int = 0
        self.heap_type = heap_type
        self._array: list = list()

    def __repr__(self) -> str:
        array = [str(node) for node in self._array]
        return f"Heap({', '.join(array)})"

    def min_heap(self) -> Heap:
        """
        Reconfigures the heap to be a min heap.

        Returns:
            Heap
        """
        self.heap_type = "Min"
        self.heapify(heap_type="Min")
        self.set_children()
        return self

    def max_heap(self) -> Heap:
        """
        Reconfigures the heap to be a max heap.

        Returns:
            Heap
        """
        self.heap_type = "Max"
        self.heapify(heap_type="Max")
        self.set_children()
        return self

    def __iter__(self) -> Heap:
        self._current = -1
        return self

    def __next__(self) -> Node:
        try:
            self._current += 1
            return self._array[self._current]
        except IndexError:
            raise StopIteration

    def depth_first_iterator(self):
        """
        Returns an iterator that iterates through the heap depth first.

        Returns:

        """
        # todo finish
        while self._current is not None:
            yield self._current
            self._current = self._current
            raise NotImplementedError

    @property
    def heap(self):
        """
        Current heap.
        """
        return self._array

    @classmethod
    def generate(cls, *values: Any, max_heap: bool = True) -> Heap:
        """
        Heapify an array of values.

        Args:
            *values (Any): Values to be heapified.
            max_heap (bool): Max heap to be created.

        Returns:

        """
        try:
            values = list(*values)
        except TypeError:
            ...
        try:
            values = list(values)
        except TypeError:
            raise

        ret_heap: Heap = cls()
        match max_heap:
            case True:
                ret_heap.heap_type = "Max"
            case False:
                ret_heap.heap_type = "Min"
            case _:
                raise TypeError("max_heap must be boolean.")
        ret_heap.heapify([Node(value=value) for value in values]).set_children()
        return ret_heap

    def set_children(self, array: Optional[list[Node]] = None) -> Heap:
        """Set each node's children in the heap."""
        if array is None:
            array = self._array
        max_idx = len(array) - 1
        for idx, node in enumerate(array):
            tmp_left_idx, tmp_right_idx = self.children_idx(idx)
            if tmp_left_idx <= max_idx:
                node.left = array[tmp_left_idx]
            if tmp_right_idx <= max_idx:
                node.right = array[tmp_right_idx]
        return self

    @staticmethod
    def parent_idx(idx: int) -> int:
        """Returns the index of the parent of a given index"""

        return int((idx - 1) // 2)

    @staticmethod
    def children_idx(idx: int) -> tuple[int, int]:
        """
        Returns the index of the children of a given index

        Returns:
            Left, Right
        """
        return 2 * idx + 1, 2 * idx + 2

    @property
    def max(self) -> Any:
        """
        Max element in heap.

        Returns:
            Element
        """
        if self.heap_type == "Max":
            return self._array[0]
        raise NotImplementedError

    @property
    def min(self) -> Any:
        """
        Max element in heap.

        Returns:
            Element
        """
        if self.heap_type == "Min":
            return self._array[0]
        raise NotImplementedError

    def insert(self, value: Any, idx: int) -> Heap:
        """
        Insert a value at a given index.

        Args:
            value (Any): element
            idx (int): Index of the element.

        Returns:
            Heap
        """
        raise NotImplementedError

    def pop(self, idx: int = -1) -> Node:
        """
        Pop a value off from a given index. Default is -1.

        Args:
            value (Any): element
            idx (int): Index of the element.

        Returns:
            Element
        """
        raise NotImplementedError

    def replace(self, idx: int, node: Node) -> Heap:
        """
        Replace a value at a given index.

        Args:
            idx (): index of the Node.
            node (): New Node.

        Returns:
            Heap
        """
        raise NotImplementedError

    def remove(self, node: Node) -> Heap:
        """
        Remove the node from the heap.

        Args:
            node (): Node to remove.

        Returns:
            
        """
        raise NotImplementedError

    def remove_root(self) -> Heap:
        raise NotImplementedError

    def merge(self, heap: Heap) -> Heap:
        raise NotImplementedError

    def __len__(self) -> int:
        return len(self._array)

    def __delitem__(self, key: int):
        raise NotImplementedError

    @property
    def is_empty(self) -> bool:
        return not len(self)

    def key_change(self, current: int, to: int) -> Heap:
        raise NotImplementedError

    def sift_up(self, current: int, to: int) -> Heap:
        raise NotImplementedError

    def sift_down(self, current: int, to: int) -> Heap:
        raise NotImplementedError

    def max_heapify(self, array: list[Node], idx: int) -> bool:
        changed: bool = False
        left, right = self.children_idx(idx)
        largest = idx
        if left <= len(array) - 1 and array[left] > array[largest]:
            largest = left
        if right <= len(array) - 1 and array[right] > array[largest]:
            largest = right

        if largest != idx:
            array[idx], array[largest] = array[largest], array[idx]
            self.max_heapify(array, largest)
            changed = True
        return changed

    def min_heapify(self, array: list[Node], idx: int) -> bool:
        changed: bool = False
        left, right = self.children_idx(idx)
        smallest = idx
        if left <= len(array) - 1 and array[left] < array[smallest]:
            smallest = left
        if right <= len(array) - 1 and array[right] < array[smallest]:
            smallest = right

        if smallest != idx:
            array[idx], array[smallest] = array[smallest], array[idx]
            self.min_heapify(array, smallest)
            changed = True
        return changed

    def heapify(
        self, array: Optional[list[Node]] = None, heap_type: Optional[str] = None
    ) -> Heap:
        if array is None:
            array = self._array
        if heap_type is None:
            heap_type = self.heap_type
        heapify: Callable[[list[Node], int], bool]
        match heap_type:
            case "Max":
                heapify = self.max_heapify
            case "Min":
                heapify = self.min_heapify
            case _:
                raise TypeError(
                    f"Heap type must be 'Min' or 'Max', received: {heap_type} ."
                )
        for idx in range(int(len(array) // 2), -1, -1):
            heapify(array=array, idx=idx)

        self._array = array
        return self

    def check_heap(
        self,
        array: Optional[list[Node]] = None,
        heap_type: Optional[str] = None,
    ) -> bool:
        if array is None:
            array = self._array
        if heap_type is None:
            heap_type = self.heap_type
        array = array[:]
        valid_heap: bool = False
        heapify: Callable[[list[Node], int], bool]
        match heap_type:
            case "Max":
                heapify = self.max_heapify
            case "Min":
                heapify = self.min_heapify
            case _:
                raise TypeError(
                    f"Heap type must be 'Min' or 'Max', received: {heap_type} ."
                )
        for idx in range(int(len(array) // 2), -1, -1):
            valid_heap = not heapify(array=array, idx=idx)

        return valid_heap
