from unittest import TestCase

import numpy as np

from data import RawChar
from model.tests.data_test_glyphs import test_glyphs
from utils.penchar_preprocessor import _rotate_strokes, _centre_of_mass, _calculate_glyph_slant
from utils.plotting import draw_chars


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

        result = _rotate_strokes(strokes, center_of_mass, angle)
        result_2 = _rotate_strokes(strokes, center_of_mass_2, angle)

        np.testing.assert_allclose(expected, result, atol=1e-16)
        np.testing.assert_allclose(expected_2, result_2, atol=1e-16)

    def test_slant_correction(self):
        # character_id = 'a'
        character_id = 'h'
        glyph = test_glyphs[character_id]
        raw_char = RawChar(character_id, "test_sample_123", [np.array(stroke) for stroke in glyph['strokes']])

        centre_of_mass = _centre_of_mass(raw_char.strokes)
        slant = _calculate_glyph_slant(raw_char.strokes)
        rotated_strokes = _rotate_strokes(raw_char.strokes, centre_of_mass, slant)

        rotated_char = RawChar(character_id, "rotated_sample_123", [np.array(stroke) for stroke in rotated_strokes])
        draw_chars([raw_char, rotated_char], 2)
