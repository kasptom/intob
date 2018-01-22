import math
from typing import List

import numpy as np

from data import RawChar
from model.Direction import Direction
from utils.mappings.penchars_mapping import CLASSES_NUMBER
from utils.mappings.penchars_mapping import mapping
from utils.penchar_preprocessor import SQUARE_PICTURE_SIDE, preprocess

PI = math.pi
M = 20  # number of points in the path
W, H = 4, 4  # resolution of the rectangle with a character
MAX_STROKES = 6
DISPLAY_IF_WARN = False


def to_vectors(raw_chars: List[RawChar]):
    """
    Converts each entity from entities to the list of x and y vectors
    :param raw_chars:
    :return: x (n x 72), y - (n x CLASSES_NUMBER) - where n is the length of the entities list
    """
    return [to_vector(raw_char) for raw_char in raw_chars]


def to_vector(raw_char: RawChar):
    raw_char = preprocess(raw_char)
    directions = compute_directions(raw_char)
    x_vector = np.array(directions)
    # 9 segments 8 directions => 72 values
    x_vector = x_vector.flatten()
    y_vector = [0] * CLASSES_NUMBER
    y_vector[mapping.get(raw_char.character_id)] = 1
    return x_vector, y_vector


def _compute_section_length(strokes_number, strokes):
    path_length = 0

    for stroke_id in range(strokes_number):
        for idx in range(1, len(strokes[stroke_id])):
            path_length += _distance(strokes[stroke_id][idx - 1], strokes[stroke_id][idx])
    return path_length / (M - 1)


def _distance(point_a, point_b):
    return math.sqrt(math.pow(point_a[0] - point_b[0], 2) + math.pow(point_a[1] - point_b[1], 2))


def compute_directions(raw_char: RawChar):
    segments_directions = [[[0 for _ in range(8)] for _ in range(W)] for _ in range(H)]
    strokes_number = len(raw_char.strokes)
    for i in range(strokes_number):
        stroke = raw_char.strokes[i]
        for j in range(2, len(stroke)):
            point_a = stroke[j - 1]
            point_b = stroke[j]
            segment_id = get_segment_of_point(point_a)
            increase_vectors_number(segment_id, point_a, point_b, segments_directions)
    return segments_directions


def increase_vectors_number(segment_id, point_a, point_b, segments_directions):
    x, y = _xy_from_points(point_a, point_b)
    rads = math.atan2(x, y)
    direction_to_increase = Direction.get_direction(rads)
    segments_directions[segment_id[0]][segment_id[1]][direction_to_increase] += 1


def _xy_from_points(a, b):
    xs = b[0] - a[0]
    ys = b[1] - a[1]
    return xs, ys


def create_normalized_path(raw_char: RawChar):
    strokes_number = len(raw_char.strokes)
    normalized_path = [[] for _ in range(strokes_number)]
    section_length = _compute_section_length(strokes_number, raw_char.strokes)

    for i in range(strokes_number):
        stroke = raw_char.strokes[i]
        prev_point = stroke[0]
        normalized_path[i].append(prev_point)
        j = 1
        while j < len(stroke):
            prev_point = normalized_path[i][-1]
            point = stroke[j]
            prev_distance = 0
            points_distance = _distance(prev_point, point)

            k = j
            while points_distance < section_length and k + 1 < len(stroke):
                prev_point = stroke[k]
                point = stroke[k + 1]
                prev_distance = points_distance
                points_distance += points_distance(prev_point, point)
                k += 1

            utvec = [point[0] - prev_point[0], point[1] - prev_point[1]]
            norm = points_distance(point, prev_point)

            j = k if k != j else j + 1

            if norm == 0 or j == len(stroke):
                continue
            utvec = [utvec[0] / norm, utvec[1] / norm]
            path_point = (
                round(prev_point[0] + utvec[0] * (section_length - prev_distance)),
                round(prev_point[1] + utvec[1] * (section_length - prev_distance))
            )
            normalized_path[i].append(path_point)

    length = 0
    for i in range(strokes_number):
        length += len(normalized_path[i])
    raw_char.strokes = normalized_path


def get_segment_of_point(point):
    w = int((W - 1) * (point[0] / SQUARE_PICTURE_SIDE))
    h = int((H - 1) * (point[1] / SQUARE_PICTURE_SIDE))
    return w, h
