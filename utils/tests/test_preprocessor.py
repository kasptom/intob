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
        center_of_mass_2 = np.array([0, 1])
        angle = np.math.pi / 2

        expected = [np.array([[-1, -1], [-1, 0], [-1, 1]])]
        expected_2 = [np.array([[0, 0], [0, 1], [0, 2]])]

        result = rotate_strokes(strokes, center_of_mass, angle)
        result_2 = rotate_strokes(strokes, center_of_mass_2, angle)

        np.testing.assert_allclose(expected, result, atol=1e-16)
        np.testing.assert_allclose(expected_2, result_2, atol=1e-16)
