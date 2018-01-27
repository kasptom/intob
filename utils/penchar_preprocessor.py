from itertools import groupby
from typing import List

import numpy as np
from numpy import linalg as la

import data

SQUARE_PICTURE_SIDE = 600
M = 35


def preprocessed_chars(raw_chars):
    preprocessed_dictchars = [preprocess(raw_sample) for raw_sample in raw_chars]
    return preprocessed_dictchars


# def vectorized_chars(mapping=None):
#     return [PenChar.to_vector(penchar) for penchar in preprocessed_chars(mapping)]
def preprocess(raw_char):
    normalized_strokes = _normalize_path(raw_char, M)

    centre_of_mass = _centre_of_mass(normalized_strokes)
    slant = _calculate_glyph_slant(normalized_strokes)
    rotated_strokes = _rotate_strokes(normalized_strokes, centre_of_mass, slant)
    x_range = _compute_x_range(rotated_strokes)
    y_range = _compute_y_range(rotated_strokes)

    cropped_sample = crop_sample(x_range, y_range, rotated_strokes)

    side_size = max(x_range[1] - x_range[0], y_range[1] - y_range[0])

    if side_size != 0:
        scale = SQUARE_PICTURE_SIDE / side_size
    else:
        scale = 1

    scaled_sample = scale_sample(scale, cropped_sample)
    return data.RawChar(raw_char.character_id, raw_char.sample_id, scaled_sample)


def _normalize_path(raw_char: data.RawChar, path_points_number: int):
    raw_strokes = raw_char.strokes
    normalized_strokes = []
    # remove adjacent duplicates
    strokes = []
    for raw_stroke in raw_strokes:
        stroke = [raw_stroke[0]]

        for raw_point in raw_stroke[1:]:
            if _dist(stroke[-1], raw_point) != 0:
                stroke.append(raw_point)
        strokes.append(np.array(stroke))

    section_len = _compute_strokes_length(strokes) / (path_points_number - 1)

    normalized_stroke = []
    for stroke in strokes:
        prev_point = stroke[0]
        normalized_stroke.append(prev_point)
        curr_dist = 0

        i = 0
        while i < len(stroke):
            point = stroke[i]
            if curr_dist + _dist(prev_point, point) <= section_len:
                curr_dist += _dist(prev_point, point)
                prev_point = point
                i += 1
            else:
                k = 1
                while k * section_len <= curr_dist + _dist(prev_point, point):
                    k += 1
                if k > 1:
                    k -= 1

                new_point = _generate_point(prev_point, point, section_len - curr_dist)
                normalized_stroke.append(new_point)
                prev_point = new_point
                for j in range(k-1):
                    new_point = _generate_point(prev_point, point, section_len)
                    normalized_stroke.append(new_point)
                    prev_point = new_point
                curr_dist = 0

                if i == len(stroke) - 1:
                    i += 1

        normalized_strokes.append(np.array(normalized_stroke))
    points_number = 0
    for stroke in normalized_strokes:
        points_number += len(stroke)
    if points_number != M:
        print(raw_char.character_id)
        print(points_number)
    return normalized_strokes


def _compute_strokes_length(strokes):
    length = 0
    for stroke in strokes:
        for i in range(1, len(stroke)):
            length += _dist(stroke[i - 1], stroke[i])
    return length


def _dist(point_a, point_b):
    return la.norm(point_a - point_b)


def _generate_point(point, next_point, translation):
    if translation < 0:
        raise RuntimeError
    unit_vec = next_point - point
    unit_vec /= la.norm(unit_vec)
    return point + unit_vec * translation


def _centre_of_mass(strokes):
    merged_strokes = np.concatenate(tuple(strokes))
    x_values = [point[0] for point in merged_strokes]
    y_values = [point[1] for point in merged_strokes]
    points_number = float(len(x_values))
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    return sum_x / points_number, sum_y / points_number


def _compute_x_range(strokes):
    return compute_coordinate_range(strokes=strokes, coordinate_index=0)


def _compute_y_range(sample):
    return compute_coordinate_range(strokes=sample, coordinate_index=1)


def compute_coordinate_range(strokes, coordinate_index):
    merged_strokes = np.concatenate(tuple(strokes))
    chosen_coordinate_column = merged_strokes[:, coordinate_index]
    coord_min = np.amin(chosen_coordinate_column)
    coord_max = np.amax(chosen_coordinate_column)
    return coord_min, coord_max


def _calculate_glyph_slant(sample):
    """
    Calculates the slant of a glyph. Only vectors with the absolute value of th angle between them and the vertical
    axis less or equal to 50 degrees are considered. Vectors are created from each consecutive points for each
    stroke.
    If a vector has the negative y-coordinate, the value of the coordinate is changed to -y so that all of
    the vectors point upwards.
    :param sample: list of strokes of the glyph sample
    :return: the estimated slant of the glyph (in radians)
    """
    slant = 0.0
    vectors_count = 0
    for i in range(len(sample)):
        for j in range(2, len(sample[i])):
            stroke = sample[i]
            point_a = stroke[j - 1]
            point_b = stroke[j]
            x, y = xy_from_points(point_a, point_b)
            y = abs(y)
            rads = np.math.atan2(x, y)
            if abs(rads) <= (50.0 * (np.math.pi / 180.0)):
                slant += rads
                vectors_count += 1
    if vectors_count != 0:
        slant = slant / vectors_count
    return slant


def xy_from_points(a, b):
    xs = b[0] - a[0]
    ys = b[1] - a[1]
    return xs, ys


def _rotate_strokes(strokes: List[np.ndarray], centre_of_mass, angle_rads):
    """
    Rotate the points around origin by the angle (counter-clockwise)
    :param strokes:
    :param centre_of_mass:
    :param angle_rads:
    :return:
    """
    rotated_strokes = []
    sin = np.math.sin(-angle_rads)  # counter-clockwise
    cos = np.math.cos(-angle_rads)
    rotation = np.array([[cos, -sin], [sin, cos]])
    for stroke in strokes:
        centered_stroke = stroke - centre_of_mass
        rotated_stroke = np.dot(centered_stroke, rotation)
        rotated_strokes.append(rotated_stroke + centre_of_mass)  # translate it back
    return rotated_strokes


def scale_sample(scale, strokes):
    return [stroke * scale for stroke in strokes]


def crop_sample(x_range, y_range, strokes):
    """
    Crops the sample to the minimal size square.
    Translates the points so that the extreme points touch the edges of the square
    :param x_range:
    :param y_range:
    :param strokes:
    :return: cropped sample
    """
    x_side = x_range[1] - x_range[0]
    y_side = y_range[1] - y_range[0]

    tvec = np.array([0, 0])
    if x_side < y_side:
        tvec[0] = x_range[0] - (y_side - x_side) / 2
        tvec[1] = y_range[0]
    else:
        tvec[0] = x_range[0]
        tvec[1] = y_range[0] - (x_side - y_side) / 2

    return [stroke - tvec for stroke in strokes]
