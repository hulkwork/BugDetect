import unittest
from src import image as module
import os

dir_name = os.path.dirname(os.path.abspath(__file__))


class Testobject(unittest.TestCase):
    def setUp(self):
        self.character_to_id = {' ': 0, '#': 2, '|': 1, 'O': 3}
        self.image_definition = module.Object(path=os.path.join(dir_name, "../data/landscape"),
                                              character_to_id=self.character_to_id)
        self.object_to_detect = module.bug.Object(path=os.path.join(dir_name, "../data/bug.txt"))

    def test_get_matrix(self):
        self.assertEqual((10, 9), self.image_definition.size)
        expected = [[1, 0, 1, 0, 0, 0, 0, 0, 0], [2, 2, 2, 3, 0, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 1, 0, 0], [0, 0, 0, 0, 2, 2, 2, 3, 0], [0, 0, 0, 0, 1, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 1, 0, 0], [0, 0, 0, 0, 2, 2, 2, 3, 0],
                    [0, 0, 0, 0, 1, 0, 1, 0, 0]]
        self.assertEqual(expected, self.image_definition.matrix)

    def test_search_object(self):
        actual = self.image_definition.search_object(self.object_to_detect)
        self.assertEqual(actual[0], 3)
        actual = self.image_definition.object_detection_big_box(character_to_id=[1, 2, 3],
                                                                object_definition=self.object_to_detect)

        self.assertEqual(actual[0], 3)

    def test_object_detection_box(self):
        image_definition = module.Object(path=os.path.join(dir_name, "../data/landscape2"),
                                         character_to_id=self.character_to_id)

        actual = image_definition.object_detection_big_box(character_to_id=[1, 2, 3], object_definition=self.object_to_detect)
        self.assertEqual(actual[0], 8)
