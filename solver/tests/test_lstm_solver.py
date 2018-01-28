import os
import random
import unittest
from unittest import TestCase

import keras
import matplotlib.pyplot as plt
import numpy as np

from data import Glyph, preprocessed_glyphs_dict
from model.raw_chars_to_vector import to_vector_m
from utils.mappings.penchars_mapping_2 import mapping
from utils.plotting import draw_chars


class TestLstmSolver(TestCase):
    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "skipping nn evaluation")
    def test_lstm_solver(self):
        prep_dict = np.array(preprocessed_glyphs_dict(mapping))
        prep_sample = [Glyph(**g) for g in prep_dict]

        prep_sample = random.sample(prep_sample, 50)

        lstm_model = keras.models.load_model("../lstm_glyphs.h5")
        inv_map = {v: k for k, v in mapping.items()}
        answers = []
        for glyph in prep_sample:
            answers.append(inv_map[np.argmax(lstm_model.predict(np.array([to_vector_m(glyph)]))[0])])
        print(answers)

        plt.figure(figsize=(14, 10))

        zipped = []
        for i in range(len(prep_sample)):
            zipped.append(prep_sample[i])
        draw_chars(zipped)
