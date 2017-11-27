from collections import namedtuple

import os
import numpy as np

_DIR = os.path.dirname(__file__)
_UJI_NPY = os.path.join(_DIR, "ujipenchars2.npy")
_UJI_TXT = os.path.join(_DIR, "ujipenchars2.txt")


def char_dicts():
    try:
        dictchars = np.load(_UJI_NPY)
    except FileNotFoundError:
        print("Loading from text file...")
        from utils.penchars_reader import read_file
        dictchars = read_file(_UJI_TXT)
        np.save(_UJI_NPY, dictchars)
    return dictchars


def raw_chars():
    return [RawChar(**d) for d in char_dicts()]


def _stroke_length(stroke):
    diff = stroke[1:] - stroke[:-1]
    return np.linalg.norm(diff, axis=1).sum()


class RawChar(namedtuple('RawChar', 'character_id sample_id strokes')):
    @property
    def stroke_lengths(self):
        return np.array([_stroke_length(s) for s in self.strokes])

