from __future__ import annotations

import heapq
from dataclasses import dataclass
from functools import total_ordering
from queue import PriorityQueue
from heapq import heappush, heappop

from bitstring import Bits


class HuffmanCodec:
    # """Codec (encoder/decoder) for a specific Huffman code.
    #
    # Examples
    # --------
    # ASCII requires 424 bits to encode this test string.
    # >>> test_string = "David Huffman invented Huffman coding at MIT in 1952."
    # >>> ascii_encoding = test_string.encode(encoding="ascii")
    # >>> len(Bits(ascii_encoding))
    # 424
    #
    # Our HuffmanCodec should produce a more efficient encoding than ASCII.
    # We should be able to encode, decode, and get the same string back.
    # >>> from collections import Counter
    # >>> frequency_map = Counter(test_string)
    # >>> codec = HuffmanCodec(frequency_map)
    # >>> huffman_encoding = codec.encode(test_string)
    # >>> len(huffman_encoding)
    # 226
    # >>> codec.decode(huffman_encoding)
    # 'David Huffman invented Huffman coding at MIT in 1952.'
    #
    # The HuffmanCodec should throw an error if we ask it to encode unfamiliar symbols:
    # >>> codec.encode("y = 19x + 52 + c")
    # Traceback (most recent call last):
    #   ...
    # ValueError: Unsupported symbol: 'y'
    #
    # It should also throw an error if we ask it to decode some data which it did not encode:
    # >>> garbage_bits = Bits(bin="0b1")
    # >>> codec.decode(huffman_encoding + garbage_bits)
    # Traceback (most recent call last):
    #   ...
    # ValueError: Could not decode.
    # """

    def __init__(self, frequency_map: dict[str, float]):
        """Constructs a HuffmanCodec for the given distribution of source symbols.

        Parameters
        ----------
        frequency_map : dict[str, float]
            Distribution of source symbols
        """
        self.root = HuffmanCodec._build_tree(frequency_map=frequency_map)
        self.code = self._get_code()

    def encode(self, source_data: str) -> Bits:
        """Encodes the given source data.

        Parameters
        ----------
        source_data : str
            String over source alphabet.

        Returns
        -------
        encoded_bits : Bits
            Encoded source data.

        Raises
        ------
        ValueError
            If source_data contains symbols which are unsupported by the codec.
        """
        try:
            return Bits().join(self.code[symbol] for symbol in source_data)
        except KeyError as err:
            raise ValueError(f"Unsupported symbol: {err.args[0]!r}")

    def decode(self, encoded_data: Bits) -> str:
        """Decodes the given string.

        Parameters
        ----------
        encoded_data : Bits
            Bitstring containing some encoded data.

        Returns
        -------
        source_data : str
            Original source data.

        Raises
        ______
        ValueError
            If encoded_data contains bits which could not be decoded.
        """
        # TODO
        # reference from: https://www.geeksforgeeks.org/huffman-decoding/
        decoded_array = []
        curr_node = self.root

        for data in encoded_data:
            if data == 0:
                curr_node = curr_node.left
            else:
                curr_node = curr_node.right

            if curr_node.is_leaf:
                decoded_array.append(curr_node.symbol)
                curr_node = self.root

        if curr_node != self.root:
            raise ValueError("Could not decode.")
        return ''.join(decoded_array)

    @staticmethod
    def _build_tree(frequency_map: dict[str, float]) -> TreeNode:
        """Builds the Huffman tree and returns the root TreeNode.

        Parameters
        ----------
        frequency_map : dict[str, float]
            Distribution of source symbols.

        Returns
        -------
        TreeNode
            Root node of resulting tree.
        """
        # TODO

        huffman_tree = [TreeNode(symbol=s, weight=w) for s, w in frequency_map.items()]

        # nodes.sort(reverse=True)
        heapq.heapify(huffman_tree)  # construct a heap structure
        while len(huffman_tree) > 1:
            leftChild = heappop(huffman_tree)  # first min value symbol - left child
            # according to the heap structure, children place from left to right
            rightChild = heappop(huffman_tree)  # second min value symbol - right child
            new_node = TreeNode(symbol="",
                                weight=leftChild.weight + rightChild.weight,
                                left=leftChild,
                                right=rightChild)
            heappush(huffman_tree, new_node)
            # nodes.sort(reverse=True)
        return huffman_tree[0]  # Root node of resulting tree.

    def _get_code(self) -> dict[str, Bits]:
        """Returns the Huffman code represented by this tree.

        Returns
        -------
        code : dict[str, Bits]
            Dictionary mapping source symbols to code words.
        """

        # TODO
        def traceback(node, path):
            if node.is_leaf:
                return {node.symbol: Bits(bin="0b" + path)}  # create a Bits object from a binary string representation
            huffman_code = dict()  # required to return a dictionary mapping
            # use the update method to update the code of the huffman code
            # reference from: https://www.programiz.com/dsa/huffman-coding
            # go left is 0, go right is 1 based on the concept of huffman code
            if node.left:
                huffman_code.update(traceback(node.left, path + '0'))
            if node.right:
                huffman_code.update(traceback(node.right, path + '1'))
            return huffman_code

        return traceback(self.root, "")


@total_ordering
@dataclass(eq=False)
class TreeNode:
    symbol: str
    weight: float
    left: TreeNode | None = None
    right: TreeNode | None = None

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    def __lt__(self, other: TreeNode) -> bool:
        return (self.weight, self.symbol) < (other.weight, other.symbol)

    def __eq__(self, other: TreeNode) -> bool:
        return (self.weight, self.symbol) == (other.weight, other.symbol)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
