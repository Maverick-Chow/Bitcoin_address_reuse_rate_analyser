#!/bin/python
import csv

class Node:
    def __init__(self, val):
        self.left = None
        self.right = None
        self.value = val
        self.occurence = 1


class Tree:
    def __init__(self):
        self.root = None
        self.size = 0

    def get_root(self):
        return self.root

    def add(self, val):
        if not self.root:
            self.root = Node(val)
            self.size += 1
            return True
        else:
            return self._add(val, self.root)

    def _add(self, val, node):
        if val < node.value:
            if node.left:
                return self._add(val, node.left)
            else:
                node.left = Node(val)
                self.size += 1
                return True
        elif val > node.value:
            if node.right:
                return self._add(val, node.right)
            else:
                node.right = Node(val)
                self.size += 1
                return True
        else:
            node.occurence += 1
            return False

    def list_tree(self):
        return self._show_tree(self.root)

    def _show_tree(self, node):
        if not node:
            return []
        else:
            return self._show_tree(node.left) + [(node.value, node.occurence)] + self._show_tree(node.right)

    def analyse(self):
        return f"""
 ==========================================
 || Total address count: {self.size}
 || Reused address count: {self._count_reused(self.root)}
 || Reuse percentage: {self._count_reused(self.root)*100/self.size}%
 ==========================================
        """

    def _count_reused(self, node):
        if not node:
            return 0
        else:
            r = 0
            if node.occurence > 1:
                r = 1
            return self._count_reused(node.left) + self._count_reused(node.right) + r

    def store_tree(self, path):
        with open(path, 'w', newline='') as csvfile:
            fieldnames = ['Address_string', 'Occurences']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            self._write_row(self.root, writer)

    def _write_row(self, node, writer):
        if node:
            writer.writerow({'Address_string': node.value, 'Occurences': node.occurence})
            self._write_row(node.left, writer)
            self._write_row(node.right, writer)
