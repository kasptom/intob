from unittest import TestCase

import numpy as np
import numpy.testing as np_test

from model.Entity import Entity


class TestEntity(TestCase):
    def test_increase_vectors_number(self):
        self.entity = Entity()
        self.stroke_id = 0
        self.expected_directions_vector = np.array([1, 1, 1, 1, 1, 1, 1, 1])
        # when
        self.entity.increase_vectors_number(self.stroke_id, (0, 0), (0, 10))
        self.entity.increase_vectors_number(self.stroke_id, (0, 0), (10, 10))
        self.entity.increase_vectors_number(self.stroke_id, (0, 0), (10, 0))
        self.entity.increase_vectors_number(self.stroke_id, (0, 0), (10, -10))
        self.entity.increase_vectors_number(self.stroke_id, (0, 0), (0, -10))
        self.entity.increase_vectors_number(self.stroke_id, (0, 0), (-10, -10))
        self.entity.increase_vectors_number(self.stroke_id, (0, 0), (-10, 0))
        self.entity.increase_vectors_number(self.stroke_id, (0, 0), (-10, 10))
        # then
        np_test.assert_array_equal(self.entity.num_directions[self.stroke_id], self.expected_directions_vector)

    def test_xy_from_points(self):
        self.point_a = (0, 10)
        self.point_b = (0, 0)
        # when
        x, y = Entity.xy_from_points(self.point_a, self.point_b)
        self.assertEqual((x, y), (0, -10))
