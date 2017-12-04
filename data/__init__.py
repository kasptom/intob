import os
from collections import namedtuple

import numpy as np

from model import PenChar
from utils.penchar_preprocessor import preprocess

_DIR = os.path.dirname(__file__)
_UJI_NPY = os.path.join(_DIR, "ujipenchars2.npy")
_UJI_PREP_NPY = os.path.join(_DIR, "ujipenchars_prep.npy")
_UJI_VEC_NPY = os.path.join(_DIR, "ujipenchars_vec.npy")
_UJI_TXT = os.path.join(_DIR, "ujipenchars2.txt")


def char_dicts(mapping=None):
    try:
        dictchars = np.load(_UJI_NPY)
    except FileNotFoundError:
        print("Loading from text file...")
        from utils.penchars_reader import read_file
        dictchars = read_file(_UJI_TXT)
        np.save(_UJI_NPY, dictchars)
    return filter(lambda c: c['character_id'] in mapping, dictchars)


def raw_chars(mapping=None):
    return [RawChar(**d) for d in char_dicts(mapping)]


def preprocessed_chars(mapping=None):
    try:
        preprocessed_dictchars = np.load(_UJI_PREP_NPY)
    except FileNotFoundError:
        print("Preprocessing raw characters...")
        preprocessed_dictchars = [preprocess(raw_sample) for raw_sample in raw_chars(mapping)]
    return preprocessed_dictchars


def vectorized_chars(mapping=None):
    return [PenChar.to_vector(penchar) for penchar in preprocessed_chars(mapping)]


def _stroke_length(stroke):
    diff = stroke[1:] - stroke[:-1]
    return np.linalg.norm(diff, axis=1).sum()


class RawChar(namedtuple('RawChar', 'character_id sample_id strokes')):
    @property
    def stroke_lengths(self):
        return np.array([_stroke_length(s) for s in self.strokes])
