import os
import random
import unittest
from unittest import TestCase

import matplotlib.pyplot as plt
import numpy as np

from data import Glyph, preprocessed_glyphs_dict
from model.raw_chars_to_vector import to_vector_m, to_vector_72
from utils.mappings.penchars_mapping_2 import mapping
from utils.plotting import draw_chars


@unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "skipping NNs evaluation")
class TestSolvers(TestCase):

    @classmethod
    def setUpClass(cls):
        prep_dict = np.array(preprocessed_glyphs_dict(mapping))
        prep_sample = [Glyph(**g) for g in prep_dict]
        cls.prep_sample = random.sample(prep_sample, 50)

    def test_lstm_solver(self):
        import keras
        lstm_model = keras.models.load_model("../lstm_glyphs.h5")
        inv_map = {v: k for k, v in mapping.items()}
        answers = []
        for glyph in self.prep_sample:
            answers.append(inv_map[np.argmax(lstm_model.predict(np.array([to_vector_m(glyph)]))[0])])
        print(answers)

        plt.figure(figsize=(14, 10))

        zipped = []
        for i in range(len(self.prep_sample)):
            zipped.append(self.prep_sample[i])
        draw_chars(zipped)

    def test_softmax_solver(self):
        import keras
        softmax_model = keras.models.load_model("../softmax_glyphs.h5")
        inv_map = {v: k for k, v in mapping.items()}
        answers = []
        for glyph in self.prep_sample:
            result = softmax_model.predict(np.array([to_vector_72(glyph)[0]]))
            answers.append(inv_map[np.argmax(result)])
        print(answers)

        plt.figure(figsize=(14, 10))

        zipped = []
        for i in range(len(self.prep_sample)):
            zipped.append(self.prep_sample[i])
        draw_chars(zipped)
