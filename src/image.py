from src import bug
import os
import numpy as np

os.path.dirname(os.path.abspath(__file__))


class Object(object):
    size = None
    matrix = None
    character_to_id = None
    np_matrix = None

    def __init__(self, path, character_to_id, padding_char=' '):
        """

        :param path:
        :param character_to_id:
        :param padding_char:
        """
        self.path = path
        self.character_to_id = character_to_id
        self.padding_char = padding_char
        self.get_matrix()

    def read_txt(self):
        with open(self.path) as f:
            return [a for a in f.readlines()]

    def get_matrix(self):
        padding_char = self.padding_char
        lines = self.read_txt()
        width = len(lines)
        matrix = []
        height = max(map(lambda x: len(list(x)), lines))
        self.size = (width, height)
        for line in lines:
            elements = list(line)
            charater_to_id_vector = map(lambda x: self.character_to_id.get(x, 0), elements)

            if len(elements) < height:
                matrix.append(
                    charater_to_id_vector + [self.character_to_id.get(padding_char, 0)] * (height - len(elements)))
            else:
                matrix.append(charater_to_id_vector)
        self.matrix = matrix
        self.np_matrix = np.asarray(matrix)

    def search_object(self, object_definition):

        count_object = 0
        coords = []
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                A = self.np_matrix[j:j + object_definition.size[0], i:i + object_definition.size[1]]
                if object_definition == A:
                    coords.append((i, i + object_definition.size[0], j, j + object_definition.size[1]))
                    count_object += 1

        return count_object, coords

    def object_detection_big_box(self, character_to_id, object_definition):
        sub_row_number = -1
        count_object = 0

        previous_ = None
        x1, y1 = None, None
        x2, y2 = -1, None
        coords = []
        coord_dectects = []
        for item in self.np_matrix:
            sub_row_number += 1
            index = [list(item).index(i) for i in character_to_id if i in item]
            reversed_item = list(item)
            reversed_item.reverse()
            reversed_index = [len(item) - 1 - reversed_item.index(i) for i in character_to_id if i in reversed_item]
            if not previous_ and index != []:
                previous_ = True
                y1 = sub_row_number
                y2 = sub_row_number
                x1 = min(index)
                x2 = max(max(reversed_index), x2)
            elif index != []:
                x2 = max(max(reversed_index), x2)
                y2 = sub_row_number
            else:
                cord = (x1, y1, x2, y2)
                if cord not in coords:
                    coords.append(cord)
                previous_ = None
        if previous_:
            cord = (x1, y1, x2, y2)
            if cord not in coords:
                coords.append(cord)
        for coord in coords:

            (x1, y1, x2, y2) = coord

            A = self.np_matrix[y1:y2 + 1, x1: x2 + 1]
            for y in range(A.shape[0] - object_definition.size[0] + 1):
                for x in range(A.shape[1] - object_definition.size[1] + 1):
                    A_tmp = A[y:y + object_definition.size[0],
                            x:x + object_definition.size[1]]

                    if object_definition == A_tmp:
                        count_object += 1
                        coord_dectect = (
                            x1 + x, y1 + y, x1 + x + object_definition.size[1], y1 + y + object_definition.size[0])
                        coord_dectects.append(coord_dectect)

        return (count_object, coord_dectects)
