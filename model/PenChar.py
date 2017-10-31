import math

import numpy as np

from model.Direction import Direction
from utils.penchars_mapping import mapping
from utils.penchars_mapping import CLASSES_NUMBER

PI = math.pi


class PenChar:
    def __init__(self):
        self.character_id = ''  # character UTF-8 id
        self.strokes_number = 0  # number of strokes - max 6
        self.points_per_stroke = np.array([0] * 6)  # overall points number per stroke
        self.num_points = np.array([0] * 6)  # number of points for each stroke (max 6 strokes)
        self.stroke_points = []
        self.num_directions = np.array([[0] * 8] * 6)  # number of vectors of each type (direction) for each stroke

    def increase_vectors_number(self, stroke_id, point_a, point_b):
        x, y = PenChar.xy_from_points(point_a, point_b)
        rads = math.atan2(x, y)
        direction_to_increase = Direction.get_direction(rads)
        self.num_directions[stroke_id, direction_to_increase] += 1

    def print_penchar(self):
        print('---')
        print(self.character_id, "strokes: ", self.strokes_number)
        np.set_printoptions(precision=1)
        for i in range(self.strokes_number):
            print("stroke: {0} {1}".format(i, 100 * self.num_directions[i] / self.points_per_stroke[i]))
        print('---')

    def print_stroke_info(self):
        points_all = 0
        for count in self.points_per_stroke:
            points_all += count
        print("length: {0}, list length: {1}, points: {2}".format(points_all, len(self.stroke_points),
                                                                  self.stroke_points))

    def to_vector(self):
        x_vector = np.array([0] * 55)
        # 8 directions 6 strokes => 48 values
        x_vector[:48] = self.num_directions.flatten()
        for i in range(self.strokes_number):
            start = i * 8
            end = (i + 1) * 8
            v_func = np.vectorize(lambda p: round(100 * p / self.points_per_stroke[i]))
            # e.g x_vector[9] is the percentage of vectors in NE direction of the 2nd stroke
            x_vector[start:end] = v_func(x_vector[start:end])

        x_vector[48:54] = self.points_per_stroke.flatten()
        x_vector[54] = self.strokes_number
        y_vector = [0] * CLASSES_NUMBER
        y_vector[mapping.get(self.character_id)] = 1

        return x_vector, y_vector

    @staticmethod
    def xy_from_points(a, b):
        xs = b[0] - a[0]
        ys = b[1] - a[1]
        return xs, ys

    @staticmethod
    def to_vectors(penchars):
        """
        Converts each entity from entities to the list of x and y vectors
        :param penchars:
        :return: x (n x 55), y - (n x CLASSES_NUMBER) - where n is the length of the entities list
        """
        return [penchar.to_vector() for penchar in penchars]
