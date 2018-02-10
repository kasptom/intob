import os
from collections import namedtuple

import numpy as np

from utils.penchar_preprocessor import create_preprocessed_glyphs_dict

_DIR = os.path.dirname(__file__)
_UJI_NPY = os.path.join(_DIR, "ujipenchars2.npy")
_UJI_PREP_NPY = os.path.join(_DIR, "ujipenchars2_prep.npy")
_UJI_VEC_NPY = os.path.join(_DIR, "ujipenchars_vec.npy")
_UJI_TXT = os.path.join(_DIR, "ujipenchars2.txt")


def raw_glyphs_dict(mapping=None):
    try:
        dictchars = np.load(_UJI_NPY)
    except FileNotFoundError:
        print("Loading from text file...")
        from utils.penchars_reader import read_file
        dictchars = read_file(_UJI_TXT)
        np.save(_UJI_NPY, dictchars)
    return filter(lambda c: c['character_id'] in mapping, dictchars)


def raw_glyphs(mapping=None):
    return [Glyph(**d) for d in raw_glyphs_dict(mapping)]


def preprocessed_glyphs(mapping=None):
    return [Glyph(**d) for d in preprocessed_glyphs_dict(mapping)]


def preprocessed_glyphs_dict(mapping=None):
    try:
        prep_glyphs_dict = np.load(_UJI_PREP_NPY)
    except FileNotFoundError:
        print("Preprocessing glyphs...")
        prep_glyphs_dict = create_preprocessed_glyphs_dict(mapping)
        np.save(_UJI_PREP_NPY, prep_glyphs_dict)
    return prep_glyphs_dict


def _stroke_length(stroke):
    diff = stroke[1:] - stroke[:-1]
    return np.linalg.norm(diff, axis=1).sum()


class Glyph(namedtuple('RawChar', 'character_id sample_id strokes')):
    @property
    def stroke_lengths(self):
        return np.array([_stroke_length(s) for s in self.strokes])
