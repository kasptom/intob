from unittest import TestCase

from model.PenChar import PenChar
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
        stroke_points = [[
            (557, 844), (550, 803), (550, 803), (550, 803), (505, 803), (505, 803), (450, 833), (450, 833),
            (377, 903), (336, 957), (298, 1014), (268, 1086), (242, 1144), (230, 1214), (235, 1272), (254, 1317),
            (254, 1317), (337, 1347), (392, 1334), (452, 1298), (518, 1247), (577, 1178), (632, 1105), (676, 1026),
            (707, 951), (728, 888), (739, 835), (739, 835), (727, 785), (727, 785), (684, 824), (661, 875),
            (643, 935), (628, 1000), (621, 1066), (622, 1126), (635, 1177), (635, 1177), (689, 1239), (689, 1239),
            (759, 1269), (759, 1269), (841, 1285), (888, 1291)
        ]]
        slant = SamplePreprocessor.calculate_glyph_slant(stroke_points)
        print(slant)
        penchar = PenChar('a', 1, stroke_points, 'tst_a')
        penchar.draw_path()
        penchar.draw_normalized_path()

    def test_rotate_sample(self):
        stroke_points = [
            [(319, 354), (313, 345), (313, 345), (313, 345), (313, 345), (313, 345), (313, 363), (313, 385), (316, 414),
             (312, 460), (309, 516), (299, 586), (289, 663), (274, 750), (256, 840), (238, 930), (218, 1011),
             (202, 1081), (187, 1138), (178, 1177), (170, 1201), (170, 1201), (170, 1201), (171, 1173), (172, 1141),
             (177, 1098), (180, 1053), (184, 1003), (184, 957), (184, 915), (181, 881), (177, 852), (173, 833),
             (171, 820), (171, 820), (173, 810), (173, 810), (194, 808), (216, 804), (240, 801), (273, 795), (308, 789),
             (349, 780), (388, 774), (428, 765), (467, 756), (503, 747), (535, 744), (570, 726), (593, 717),
             (619, 699)],
            [(719, 364), (719, 364), (714, 349), (714, 349), (706, 358), (702, 368), (693, 388), (687, 412),
             (674, 448), (663, 486), (644, 539), (627, 593), (602, 659), (580, 728), (553, 803), (531, 874), (507, 945),
             (492, 1010), (478, 1069), (469, 1116), (467, 1152), (468, 1179), (473, 1190), (487, 1188), (500, 1177),
             (520, 1154)]
        ]

        penchar = PenChar('h', 2, stroke_points, 'tst_h')
        penchar.draw_path()
        # penchar.draw_normalized_path()

        flatten_sample = SamplePreprocessor.flatten_sample(stroke_points)
        center_of_mass = SamplePreprocessor.center_of_mass(flatten_sample)
        slant = SamplePreprocessor.calculate_glyph_slant(stroke_points)
        rotated_stroke_points = SamplePreprocessor.rotate_sample(stroke_points, center_of_mass, slant)

        rotated_penchar = PenChar('a_rotated', 2, rotated_stroke_points, 'tst_a_rtd')
        rotated_penchar.draw_path()
