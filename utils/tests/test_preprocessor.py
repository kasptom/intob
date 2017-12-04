from unittest import TestCase

import numpy as np

from utils.penchar_preprocessor import rotate_strokes, _centre_of_mass


class TestPreprocessor(TestCase):
    def test_center_of_mass(self):
        strokes = [np.array([[-1, 1], [0, 1], [1, 1]])]
        expected = np.array([0, 1])

        result = _centre_of_mass(strokes)

        np.testing.assert_array_equal(expected, result)

    def test_rotate_strokes(self):
        strokes = [np.array([[-1, 1], [0, 1], [1, 1]])]
        center_of_mass = np.array([0, 0])
        angle = np.math.pi / 2

        expected = [np.array([[-1, -1], [-1, 0], [-1, 1]])]

        result = rotate_strokes(strokes, center_of_mass, angle)

        np.testing.assert_allclose(expected, result, atol=1e-16)
