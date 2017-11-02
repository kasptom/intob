from unittest import TestCase

import numpy as np
import numpy.testing as np_test

from model.PenChar import PenChar


class TestPenchar(TestCase):
    def test_increase_vectors_number(self):
        pass
        # self.entity = PenChar()
        # self.stroke_id = 0
        # self.expected_directions_vector = np.array([1, 1, 1, 1, 1, 1, 1, 1])
        # # when
        # self.entity.increase_vectors_number(self.stroke_id, (0, 0), (0, 10))
        # self.entity.increase_vectors_number(self.stroke_id, (0, 0), (10, 10))
        # self.entity.increase_vectors_number(self.stroke_id, (0, 0), (10, 0))
        # self.entity.increase_vectors_number(self.stroke_id, (0, 0), (10, -10))
        # self.entity.increase_vectors_number(self.stroke_id, (0, 0), (0, -10))
        # self.entity.increase_vectors_number(self.stroke_id, (0, 0), (-10, -10))
        # self.entity.increase_vectors_number(self.stroke_id, (0, 0), (-10, 0))
        # self.entity.increase_vectors_number(self.stroke_id, (0, 0), (-10, 10))
        # # then
        # np_test.assert_array_equal(self.entity.num_directions[self.stroke_id], self.expected_directions_vector)

    def test_xy_from_points(self):
        self.point_a = (0, 10)
        self.point_b = (0, 0)
        # when
        x, y = PenChar.xy_from_points(self.point_a, self.point_b)
        self.assertEqual((x, y), (0, -10))

    def test_create_normalized_path(self):
        character_id = 'a'
        strokes_number = 1
        stroke_points = [
            [(557, 844), (550, 803), (550, 803), (550, 803), (505, 803), (505, 803), (450, 833), (450, 833), (377, 903),
             (336, 957), (298, 1014), (268, 1086), (242, 1144), (230, 1214), (235, 1272), (254, 1317), (254, 1317),
             (337, 1347), (392, 1334), (452, 1298), (518, 1247), (577, 1178), (632, 1105), (676, 1026), (707, 951),
             (728, 888), (739, 835), (739, 835), (727, 785), (727, 785), (684, 824), (661, 875), (643, 935),
             (628, 1000), (621, 1066), (622, 1126), (635, 1177), (635, 1177), (689, 1239), (689, 1239), (759, 1269),
             (759, 1269), (841, 1285), (888, 1291)]]
        print("stroke points length: ", len(stroke_points[0]))
        penchar = PenChar(character_id, strokes_number, stroke_points)
        penchar.print_penchar()
