import math

import numpy as np

from model.Direction import Direction
from utils.mappings.penchars_mapping import CLASSES_NUMBER
from utils.mappings.penchars_mapping import mapping
from utils.penchar_preprocessor import preprocess, SQUARE_PICTURE_SIDE

PI = math.pi
M = 20  # number of points in the path
W, H = 4, 4  # resolution of the rectangle with a character
MAX_STROKES = 6
DISPLAY_IF_WARN = False


class PenChar:
    def __init__(self, raw_char, unique_identifier=None, debug=False):
        """
        :param character_id: e.g. "a"
        :param strokes_number: number of lines used to draw a character
        :param stroke_points: list of lists of points for each of the stroke
        :param unique_identifier: id of the sample (should be unique)
        """
        self.character_id = raw_char.character_id  # character UTF-8 id
        self.unique_identifier = unique_identifier
        self.strokes_number = len(raw_char.strokes)  # number of strokes - max 6
        self.strokes_points = preprocess(raw_char)
        self.section_length = self.compute_section_length(self.strokes_number, self.strokes_points)
        self.debug = debug

        self.normalized_path = None
        self.normalized_path_size = 0
        self.status = "OK"
        self.create_normalized_path()

        self.segments_directions = None
        self.compute_directions()

    @staticmethod
    def compute_section_length(strokes_number, strokes):
        path_length = 0

        for stroke_id in range(strokes_number):
            for idx in range(1, len(strokes[stroke_id])):
                path_length += PenChar.distance(strokes[stroke_id][idx - 1],
                                                strokes[stroke_id][idx])
        return path_length / (M - 1)

    @staticmethod
    def distance(point_a, point_b):
        return math.sqrt(math.pow(point_a[0] - point_b[0], 2) + math.pow(point_a[1] - point_b[1], 2))

    def increase_vectors_number(self, segment_id, point_a, point_b):
        x, y = PenChar.xy_from_points(point_a, point_b)
        rads = math.atan2(x, y)
        direction_to_increase = Direction.get_direction(rads)
        self.segments_directions[segment_id[0]][segment_id[1]][direction_to_increase] += 1

    def to_vector(self):
        x_vector = np.array(self.segments_directions)
        # 9 segments 8 directions => 72 values
        x_vector = x_vector.flatten()
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
        :return: x (n x 72), y - (n x CLASSES_NUMBER) - where n is the length of the entities list
        """
        return [penchar.to_vector() for penchar in penchars]

    def create_normalized_path(self):
        normalized_path = [[] for _ in range(self.strokes_number)]

        for i in range(self.strokes_number):
            stroke = self.strokes_points[i]
            prev_point = stroke[0]
            normalized_path[i].append(prev_point)
            j = 1
            while j < len(stroke):
                prev_point = normalized_path[i][-1]
                point = stroke[j]
                prev_distance = 0
                distance = PenChar.distance(prev_point, point)

                k = j
                while distance < self.section_length and k + 1 < len(stroke):
                    prev_point = stroke[k]
                    point = stroke[k + 1]
                    prev_distance = distance
                    distance += PenChar.distance(prev_point, point)
                    k += 1

                utvec = [point[0] - prev_point[0], point[1] - prev_point[1]]
                norm = PenChar.distance(point, prev_point)

                j = k if k != j else j + 1

                if norm == 0 or j == len(stroke):
                    continue
                utvec = [utvec[0] / norm, utvec[1] / norm]
                path_point = (
                    round(prev_point[0] + utvec[0] * (self.section_length - prev_distance)),
                    round(prev_point[1] + utvec[1] * (self.section_length - prev_distance))
                )
                normalized_path[i].append(path_point)

        length = 0
        for i in range(self.strokes_number):
            length += len(normalized_path[i])

        self.normalized_path_size = length

        if length != M:
            overall_points = 0
            for stroke in self.strokes_points:
                overall_points += len(stroke)

            if self.debug:
                print("WARN for: {}: normalized path length: {}, M={}, all points count: {}, strokes: {}"
                      .format(self.unique_identifier, length, M, overall_points, self.strokes_number))
            self.status = "WARN"
            # if DISPLAY_IF_WARN:
            # TODO
        self.normalized_path = normalized_path

    def compute_directions(self):
        self.segments_directions = [[[0 for _ in range(8)] for _ in range(W)] for _ in range(H)]
        for i in range(self.strokes_number):
            stroke = self.normalized_path[i]
            for j in range(2, len(stroke)):
                point_a = stroke[j - 1]
                point_b = stroke[j]
                segment_id = PenChar.get_segment_of_point(point_a)
                self.increase_vectors_number(segment_id, point_a, point_b)

    @staticmethod
    def get_segment_of_point(point):
        w = int((W - 1) * (point[0] / SQUARE_PICTURE_SIDE))
        h = int((H - 1) * (point[1] / SQUARE_PICTURE_SIDE))
        return w, h
