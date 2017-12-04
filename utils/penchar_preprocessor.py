from typing import List

import numpy as np

SQUARE_PICTURE_SIDE = 600


def preprocess(raw_char):
    centre_of_mass = _centre_of_mass(raw_char.strokes)
    slant = calculate_glyph_slant(raw_char.strokes)
    rotated_strokes = rotate_strokes(raw_char.strokes, centre_of_mass, -slant)
    x_range = compute_x_range(rotated_strokes)
    y_range = compute_y_range(rotated_strokes)

    cropped_sample = crop_sample(x_range, y_range, rotated_strokes)

    side_size = max(x_range[1] - x_range[0], y_range[1] - y_range[0])
    scale = SQUARE_PICTURE_SIDE / side_size

    scaled_sample = scale_sample(scale, cropped_sample)
    return scaled_sample


def _centre_of_mass(strokes):
    merged_strokes = np.concatenate(tuple(strokes))
    x_values = [point[0] for point in merged_strokes]
    y_values = [point[1] for point in merged_strokes]
    points_number = float(len(x_values))
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    return sum_x / points_number, sum_y / points_number


def flatten_sample(sample):
    return [point for stroke in sample for point in stroke]


def compute_x_range(strokes):
    return compute_coordinate_range(strokes=strokes, coordinate_index=0)


def compute_y_range(sample):
    return compute_coordinate_range(strokes=sample, coordinate_index=1)


def compute_coordinate_range(strokes, coordinate_index):
    merged_strokes = np.concatenate(tuple(strokes))
    coord_min = np.amin(merged_strokes, axis=coordinate_index)
    coord_max = np.amax(merged_strokes, axis=coordinate_index)
    return coord_min, coord_max


def calculate_glyph_slant(sample):
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
            if abs(rads) <= 50.0:
                slant += rads
                vectors_count += 1
    slant = slant / vectors_count
    return slant


def xy_from_points(a, b):
    xs = b[0] - a[0]
    ys = b[1] - a[1]
    return xs, ys


def _rotate(point, origin, angle):
    """
    Rotate the point around origin by the angle (counter-clockwise)
    :param origin: point around which we perform the rotation
    :param point: point which position we want to change
    :param angle: angle given in radians
    :return: coordinates of the rotated point
    """
    ox, oy = origin
    px, py = point

    qx = ox + np.math.cos(angle) * (px - ox) - np.math.sin(angle) * (py - oy)
    qy = oy + np.math.sin(angle) * (px - ox) + np.math.cos(angle) * (py - oy)
    return qx, qy


def rotate_strokes(strokes: List[np.ndarray], centre_of_mass, angle_rads):
    rotated_strokes = []
    for stroke in strokes:
        rotated_strokes.append(np.apply_along_axis(_rotate, 1, stroke, centre_of_mass, angle_rads))
    return rotated_strokes


def scale_sample(scale, sample):
    scaled_sample = []
    for i in range(len(sample)):
        stroke = sample[i]
        stroke = [(point[0] * scale, point[1] * scale) for point in stroke]
        scaled_sample.append(stroke)
    return scaled_sample


def crop_sample(x_range, y_range, sample):
    cropped_sample = []
    x_side = x_range[1] - x_range[0]
    y_side = y_range[1] - y_range[0]

    tvec = [0, 0]
    if x_side < y_side:
        tvec[0] = x_range[0] - (y_side - x_side) / 2
        tvec[1] = y_range[0]
    else:
        tvec[0] = x_range[0]
        tvec[1] = y_range[0] - (x_side - y_side) / 2

    for i in range(len(sample)):
        stroke = sample[i]
        stroke = [(point[0] - tvec[0], point[1] - tvec[1]) for point in stroke]
        cropped_sample.append(stroke)
    return cropped_sample
