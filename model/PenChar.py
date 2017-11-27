import math

import numpy as np
from utils.sample_preprocessor import SamplePreprocessor
from PIL import Image, ImageDraw
from pip._vendor.distlib.compat import raw_input
from utils.sample_preprocessor import SQUARE_PICTURE_SIDE

from model.Direction import Direction
from utils.penchars_mapping import CLASSES_NUMBER
from utils.penchars_mapping import mapping

PI = math.pi
M = 20  # number of points in the path
W, H = 4, 4  # resolution of the rectangle with a character
MAX_STROKES = 6
DISPLAY_IF_WARN = False


class PenChar:
    def __init__(self, character_id, strokes_number, stroke_points, unique_identifier=None, debug=False, preprocess=True):
        """
        :param character_id: e.g. "a"
        :param strokes_number: number of lines used to draw a character
        :param stroke_points: list of lists of points for each of the stroke
        :param unique_identifier: id of the sample (should be unique)
        """
        self.character_id = character_id  # character UTF-8 id
        self.unique_identifier = unique_identifier
        self.strokes_number = strokes_number  # number of strokes - max 6
        self.strokes_points = SamplePreprocessor.preprocess_sample(stroke_points) if preprocess else stroke_points
        self.section_length = self.compute_section_length()
        self.debug = debug

        self.normalized_path = None
        self.normalized_path_size = 0
        self.status = "OK"
        self.create_normalized_path()

        self.segments_directions = None
        if preprocess:
            self.compute_directions()

    def compute_section_length(self):
        path_length = 0

        for stroke_id in range(self.strokes_number):
            for idx in range(1, len(self.strokes_points[stroke_id])):
                path_length += PenChar.distance(self.strokes_points[stroke_id][idx - 1],
                                                self.strokes_points[stroke_id][idx])
        return path_length / (M - 1)

    @staticmethod
    def distance(point_a, point_b):
        return math.sqrt(math.pow(point_a[0] - point_b[0], 2) + math.pow(point_a[1] - point_b[1], 2))

    def increase_vectors_number(self, segment_id, point_a, point_b):
        x, y = PenChar.xy_from_points(point_a, point_b)
        rads = math.atan2(x, y)
        direction_to_increase = Direction.get_direction(rads)
        self.segments_directions[segment_id[0]][segment_id[1]][direction_to_increase] += 1

    def print_penchar(self):
        print('---')
        print(self.character_id, "strokes: ", self.strokes_number)
        np.set_printoptions(precision=1)
        points_in_path = 0
        for i in range(self.strokes_number):
            points_in_path += len(self.normalized_path[i])
            print("original stroke {}: {}".format(i, self.strokes_points[i]))
            print("normalized stroke {}: {}".format(i, self.normalized_path[i]))
            # print("stroke: {0} {1}".format(i, 100 * self.num_directions[i] / self.points_per_stroke[i]))
        print("number of points", points_in_path)
        print("M=", M)
        print('---')

    def draw_normalized_path(self, title=None):
        im = Image.new('RGB', (420, 620), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        for i in range(self.strokes_number):
            for j in range(len(self.normalized_path[i]) - 1):
                a = self.normalized_path[i][j]
                a = (a[0] / 5, a[1] / 5)
                b = self.normalized_path[i][j + 1]
                b = (b[0] / 5, b[1] / 5)
                draw.line(a + b, fill=255, width=1)
                PenChar.draw_dot(draw, a)
                PenChar.draw_dot(draw, b)
        im.show(title)
        return im

    def draw_path(self, title=None):
        im = Image.new('RGB', (420, 620), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        for i in range(self.strokes_number):
            for j in range(len(self.strokes_points[i]) - 1):
                a = self.strokes_points[i][j]
                a = (a[0] / 5, a[1] / 5)
                b = self.strokes_points[i][j + 1]
                b = (b[0] / 5, b[1] / 5)
                draw.line(a + b, fill=255, width=1)
                PenChar.draw_dot(draw, a)
                PenChar.draw_dot(draw, b)
        im.show(title)
        return im

    @staticmethod
    def draw_dot(draw, xy):
        draw.ellipse((xy[0] - 2, xy[1] - 2, xy[0] + 2, xy[1] + 2), fill='blue', outline='blue')

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
            if DISPLAY_IF_WARN:
                path_image = self.draw_path()
                npath_image = self.draw_normalized_path()
                raw_input('Press enter to continue: ')
                path_image.close()
                npath_image.close()
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
        w = int((W-1) * (point[0] / SQUARE_PICTURE_SIDE))
        h = int((H-1) * (point[1] / SQUARE_PICTURE_SIDE))
        return w, h
