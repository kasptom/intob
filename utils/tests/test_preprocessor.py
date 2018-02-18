import os
import random
import unittest
from math import pi
from unittest import TestCase

import matplotlib.pyplot as plt
import numpy as np

from data import Glyph, raw_glyphs_dict, preprocessed_glyphs_dict
from model.Direction import Direction
from utils.mappings.penchars_mapping_2 import mapping
from utils.penchar_preprocessor import _centre_of_mass, xy_from_points, _rotate_strokes, _calculate_glyph_slant
from utils.plotting import draw_chars
from utils.tests.data_test_glyphs import test_glyphs


class TestPreprocessor(TestCase):
    def test_center_of_mass(self):
        strokes = [np.array([[-1, 1], [0, 1], [1, 1]])]
        expected = np.array([0, 1])

        result = _centre_of_mass(strokes)

        np.testing.assert_array_equal(expected, result)

    def test_xy_from_points(self):
        self.point_a = (0, 10)
        self.point_b = (0, 0)
        # when
        x, y = xy_from_points(self.point_a, self.point_b)
        self.assertEqual((x, y), (0, -10))

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
        character_id = 'a'
        character_id = 'h'

        glyph = test_glyphs[character_id]
        raw_char = Glyph(character_id, "test_sample_123", [np.array(stroke) for stroke in glyph['strokes']])
        rotation_sequence = [raw_char]

        for i in range(9):
            centre_of_mass = _centre_of_mass(raw_char.strokes)
            slant = _calculate_glyph_slant(raw_char.strokes)
            rotated_strokes = _rotate_strokes(raw_char.strokes, centre_of_mass, slant)
            rotated_char = Glyph(character_id, "rotated_sample_123", [np.array(stroke) for stroke in rotated_strokes])
            rotation_sequence.append(rotated_char)

        # draw_chars(rotation_sequence, 10)
        np.testing.assert_array_equal(rotation_sequence[1].strokes[0], rotation_sequence[-1].strokes[0])
        np.testing.assert_array_equal(rotation_sequence[1].strokes[1], rotation_sequence[-1].strokes[1])

    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "skipping glyphs' plotting")
    def test_compare_rotation(self):
        character_ids = ['I', 'H', 'c']
        rotation_sequence = []
        raw_sequence = []

        for character_id in character_ids:
            glyph = test_glyphs[character_id]
            raw_char = Glyph(character_id, "test_sample_123" + character_id, [np.array(stroke) for stroke in glyph['strokes']])

            centre_of_mass = _centre_of_mass(raw_char.strokes)
            slant = _calculate_glyph_slant(raw_char.strokes)
            rotated_strokes = _rotate_strokes(raw_char.strokes, centre_of_mass, slant)
            glyph = Glyph(character_id, "rotated_sample_123" + character_id, [np.array(stroke) for stroke in rotated_strokes])

            raw_sequence.append(raw_char)
            rotation_sequence.append(glyph)

        draw_chars(raw_sequence + rotation_sequence, 3)

    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "skipping glyphs' plotting")
    def test_preprocess_sample(self):
        raw_dict, prep_dict = np.array(list(raw_glyphs_dict(mapping))), preprocessed_glyphs_dict(mapping)

        zipped_dicts = list(zip(raw_dict, prep_dict))
        zipped_dicts = random.sample(list(zipped_dicts), 50)

        raw_sample = [Glyph(**pair[0]) for pair in zipped_dicts]
        prep_sample = [Glyph(**pair[1]) for pair in zipped_dicts]

        plt.figure(figsize=(14, 10))

        zipped = []
        for i in range(len(raw_sample)):
            zipped.append(raw_sample[i])
            zipped.append(prep_sample[i])
        draw_chars(zipped)

    def test_get_direction(self):
        # given
        angle_rads_n = 0
        angle_rads_ne = 0.25 * pi
        angle_rads_e = 0.5 * pi
        angle_rads_se = 0.75 * pi
        angle_rads_s = pi
        angle_rads_sw = -0.75 * pi
        angle_rads_w = -0.5 * pi
        angle_rads_nw = -0.25 * pi

        # when
        direction_n = Direction.get_direction(angle_rads_n)
        direction_ne = Direction.get_direction(angle_rads_ne)
        direction_e = Direction.get_direction(angle_rads_e)
        direction_se = Direction.get_direction(angle_rads_se)
        direction_s = Direction.get_direction(angle_rads_s)
        direction_sw = Direction.get_direction(angle_rads_sw)
        direction_w = Direction.get_direction(angle_rads_w)
        direction_nw = Direction.get_direction(angle_rads_nw)

        # then
        self.assertEqual(direction_n, Direction.N)
        self.assertEqual(direction_ne, Direction.NE)
        self.assertEqual(direction_e, Direction.E)
        self.assertEqual(direction_se, Direction.SE)
        self.assertEqual(direction_s, Direction.S)
        self.assertEqual(direction_sw, Direction.SW)
        self.assertEqual(direction_w, Direction.W)
        self.assertEqual(direction_nw, Direction.NW)
