from unittest import TestCase
from model.Direction import Direction
from math import pi


class TestDirection(TestCase):
    def test_get_direction(self):
        # given
        angle_rads_n = 0
        angle_rads_ne = 0.25 * pi
        angle_rads_e = 0.5 * pi
        angle_rads_se = 0.75 * pi
        angle_rads_s = pi
        angle_rads_sw = -0.75 * pi
        angle_rads_w = -0.5 * pi
        angle_rads_nw = -0.25 * pi

        # when
        direction_n = Direction.get_direction(angle_rads_n)
        direction_ne = Direction.get_direction(angle_rads_ne)
        direction_e = Direction.get_direction(angle_rads_e)
        direction_se = Direction.get_direction(angle_rads_se)
        direction_s = Direction.get_direction(angle_rads_s)
        direction_sw = Direction.get_direction(angle_rads_sw)
        direction_w = Direction.get_direction(angle_rads_w)
        direction_nw = Direction.get_direction(angle_rads_nw)

        # then
        self.assertEqual(direction_n, Direction.N)
        self.assertEqual(direction_ne, Direction.NE)
        self.assertEqual(direction_e, Direction.E)
        self.assertEqual(direction_se, Direction.SE)
        self.assertEqual(direction_s, Direction.S)
        self.assertEqual(direction_sw, Direction.SW)
        self.assertEqual(direction_w, Direction.W)
        self.assertEqual(direction_nw, Direction.NW)
