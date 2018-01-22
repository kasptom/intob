import random
from unittest import TestCase

import matplotlib.pyplot as plt

from data import raw_chars
from utils.mappings.penchars_mapping_2 import mapping
from utils.penchar_preprocessor import preprocessed_chars
from utils.plotting import draw_chars


class TestSamplePreprocessor(TestCase):
    stroke_points = [
        [(0, 1), (1, 2), (-10, 3)],
        [(100, 0), (4, 6), (5, 9)],
        [(-5, 0), (-10, 200), (5, 4)],
    ]

    def test_compute_range(self):
        pass

    def test_compute_centre_of_mass(self):
        pass

    def test_calculate_glyph_slant(self):
        pass

    def test_rotate_sample(self):
        pass

    def test_preprocess_sample(self):
        penchars = raw_chars(mapping)
        sample = random.sample(penchars, 50)

        preprocessed = preprocessed_chars(sample)

        plt.figure(figsize=(14, 10))

        zipped = []
        for i in range(len(sample)):
            zipped.append(sample[i])
            zipped.append(preprocessed[i])

        draw_chars(zipped)
