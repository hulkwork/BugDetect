import unittest
from src import bug as module
import os
import numpy as np

dir_name = os.path.dirname(os.path.abspath(__file__))


class Testobject(unittest.TestCase):
    def setUp(self):
        self.bug_definition = module.Object(path=os.path.join(dir_name, "../data/bug.txt"))

    def test_get_object(self):
        self.assertEqual((3, 5), self.bug_definition.size)
        expected = [[1, 0, 1, 2, 0], [3, 3, 3, 4, 2], [1, 0, 1, 0, 0]]
        self.assertEqual(expected, self.bug_definition.matrix)
        expected = {' ': 0, '#': 3, '\n': 2, '|': 1, 'O': 4}
        self.assertEqual(expected, self.bug_definition.character_to_id)

    def test_equal(self):
        self.assertEqual(True, self.bug_definition == self.bug_definition.np_matrix)


