import math
import numpy as np

from model.Direction import Direction

PI = math.pi


class Entity:
    def __init__(self):
        self.character_id = ''  # character UTF-8 id
        self.strokes_number = 0  # number of strokes - max 6
        self.points_per_stroke = np.array([0] * 6)  # overall points number per stroke
        self.num_points = np.array([0] * 6)  # number of points for each stroke (max 6 strokes)
        self.num_directions = np.array([[0] * 8] * 6)  # number of vectors of each type (direction) for each stroke

    def increase_vectors_number(self, stroke_id, point_a, point_b):
        x, y = Entity.xy_from_points(point_a, point_b)
        rads = math.atan2(x, y)
        direction_to_increase = Direction.get_direction(rads)
        self.num_directions[stroke_id, direction_to_increase] += 1

    def print_entity(self):
        print('---')
        print(self.character_id, "strokes: ", self.strokes_number)
        np.set_printoptions(precision=1)
        for i in range(self.strokes_number):
            print("stroke: {0} {1}".format(i, 100 * self.num_directions[i] / self.points_per_stroke[i]))
        print('---')

    @ staticmethod
    def xy_from_points(a, b):
        xs = b[0] - a[0]
        ys = b[1] - a[1]
        return xs, ys
