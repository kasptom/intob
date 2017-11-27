from unittest import TestCase

from model.PenChar import PenChar
from model.tests.test_glyphs import test_glyphs


class TestPenChar(TestCase):
    def test_xy_from_points(self):
        self.point_a = (0, 10)
        self.point_b = (0, 0)
        # when
        x, y = PenChar.xy_from_points(self.point_a, self.point_b)
        self.assertEqual((x, y), (0, -10))

    def test_create_normalized_path(self):
        # character_id = 'a'
        character_id = 'c'
        glyph = test_glyphs[character_id]
        pen_char = PenChar(character_id, glyph['strokes_number'], glyph['strokes'])
        pen_char.print_penchar()
        pen_char.draw_normalized_path()
        pen_char.draw_path()
