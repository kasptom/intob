from unittest import TestCase

from model.PenChar import PenChar
from model.tests.test_glyphs import test_glyphs
from utils.sample_preprocessor import SamplePreprocessor


class TestSamplePreprocessor(TestCase):
    stroke_points = [
        [(0, 1), (1, 2), (-10, 3)],
        [(100, 0), (4, 6), (5, 9)],
        [(-5, 0), (-10, 200), (5, 4)],
    ]

    def test_compute_range(self):
        stroke_points = TestSamplePreprocessor.stroke_points
        flatten_strokes = SamplePreprocessor.flatten_sample(stroke_points)
        expected_x_min = -10
        expected_x_max = 100
        expected_y_min = 0
        expected_y_max = 200

        x_min, x_max = SamplePreprocessor.compute_x_range(flatten_sample=flatten_strokes)
        y_min, y_max = SamplePreprocessor.compute_y_range(sample=flatten_strokes)
        self.assertEqual(expected_x_min, x_min)
        self.assertEqual(expected_x_max, x_max)
        self.assertEqual(expected_y_min, y_min)
        self.assertEqual(expected_y_max, y_max)

    def test_compute_centre_of_mass(self):
        stroke_points = TestSamplePreprocessor.stroke_points
        flatten_strokes = SamplePreprocessor.flatten_sample(stroke_points)
        expected_center_of_mass = (10.0, 25.0)
        centre_of_mass = SamplePreprocessor.center_of_mass(flatten_sample=flatten_strokes)
        self.assertEqual(expected_center_of_mass, centre_of_mass)

    def test_calculate_glyph_slant(self):
        character_id = 'h'
        glyph = test_glyphs[character_id]
        slant = SamplePreprocessor.calculate_glyph_slant(glyph['strokes'])
        print(slant)
        penchar = PenChar(character_id, glyph['strokes_number'], glyph['strokes'], 'tst_a')
        penchar.draw_path()
        penchar.draw_normalized_path()

    def test_rotate_sample(self):
        character_id = 'h'
        glyph = test_glyphs[character_id]
        penchar = PenChar(character_id, glyph['strokes_number'], glyph['strokes'], 'tst_h')
        penchar.draw_path()
        penchar.draw_normalized_path()

        flatten_sample = SamplePreprocessor.flatten_sample(glyph['strokes'])
        center_of_mass = SamplePreprocessor.center_of_mass(flatten_sample)
        slant = SamplePreprocessor.calculate_glyph_slant(glyph['strokes'])
        rotated_stroke_points = SamplePreprocessor.rotate_sample(glyph['strokes'], center_of_mass, slant)

        rotated_penchar = PenChar('h_rotated', 2, rotated_stroke_points, 'tst_h_rtd')
        rotated_penchar.draw_path()

    def test_preprocess_sample(self):
        character_id = 'h'
        # character_id = 'I_slant'
        glyph = test_glyphs[character_id]
        penchar = PenChar(character_id, glyph['strokes_number'], glyph['strokes'], 'tst_h', preprocess=False, debug=True)
        penchar.draw_path()

        # preprocessed_stroke_points = SamplePreprocessor.preprocess_sample(glyph['strokes'])
        preprocessed_penchar = PenChar('h_p', glyph['strokes_number'], glyph['strokes'], 'tst_h_p')
        preprocessed_penchar.draw_path()
        preprocessed_penchar.draw_normalized_path()
