from unittest import TestCase

import numpy as np

from data import RawChar
from model.tests.data_test_glyphs import test_glyphs
from utils.penchar_preprocessor import xy_from_points, _calculate_glyph_slant, _rotate_strokes, _centre_of_mass
from utils.plotting import draw_chars


class TestPreprocessing(TestCase):
    def test_xy_from_points(self):
        self.point_a = (0, 10)
        self.point_b = (0, 0)
        # when
        x, y = xy_from_points(self.point_a, self.point_b)
        self.assertEqual((x, y), (0, -10))
