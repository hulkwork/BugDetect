import os
import numpy as np

os.path.dirname(os.path.abspath(__file__))


class Object(object):
    size = None
    matrix = None
    character_to_id = None
    np_matrix = None

    def __init__(self, path=None):
        """

        :param path:
        """
        if not path:
            raise Exception("Please, define your object you need to detect")
        self.path = path
        self.get_object()

    def read_txt(self):
        with open(self.path) as f:
            return [a.strip() for a in f.readlines()]

    def get_object(self, padding_char=' '):
        id_char_count = 0
        character_to_id = {padding_char: id_char_count}
        lines = self.read_txt()
        width = len(lines)
        matrix = []
        height = max(map(lambda x: len(list(x)), lines))
        self.size = (width, height)
        for line in lines:
            elements = list(line)
            for el in elements:
                if el not in character_to_id:
                    id_char_count += 1
                    character_to_id[el] = id_char_count

            character_to_id_vector = map(lambda x: character_to_id[x], elements)

            if len(elements) < height:
                matrix.append(character_to_id_vector + [character_to_id[padding_char]] * (height - len(elements)))
            else:
                matrix.append(character_to_id_vector)
        self.matrix = matrix
        self.character_to_id = character_to_id
        self.np_matrix = np.asarray(matrix)

    def __eq__(self, other):

        if self.np_matrix.shape != other.shape:
            return False
        res = True
        for i, item in enumerate(self.np_matrix):
            tmp_res = list(set([val == other[i][k] for k, val in enumerate(item) if val != 0 ]))

            r_tmp = True
            for t in tmp_res:
                r_tmp *= t
            if not r_tmp:
                return False

        return res
