import math

SQUARE_PICTURE_SIDE = 600


class SamplePreprocessor:
    def __init__(self):
        pass

    @staticmethod
    def preprocess_sample(sample):
        flatten_sample = SamplePreprocessor.flatten_sample(sample)

        centre_of_mass = SamplePreprocessor.center_of_mass(flatten_sample)
        slant = SamplePreprocessor.calculate_glyph_slant(sample)

        rotated_sample = SamplePreprocessor.rotate_sample(sample, centre_of_mass, slant)

        rotated_flatten_sample = SamplePreprocessor.flatten_sample(rotated_sample)
        x_range = SamplePreprocessor.compute_x_range(rotated_flatten_sample)
        y_range = SamplePreprocessor.compute_y_range(rotated_flatten_sample)

        cropped_sample = SamplePreprocessor.crop_sample(x_range, y_range, rotated_sample)

        side_size = max(x_range[1] - x_range[0], y_range[1] - y_range[0])
        scale = SQUARE_PICTURE_SIDE / side_size

        scaled_sample = SamplePreprocessor.scale_sample(scale, cropped_sample)

        return scaled_sample

    @staticmethod
    def flatten_sample(sample):
        return [point for stroke in sample for point in stroke]

    @staticmethod
    def compute_x_range(flatten_sample):
        return SamplePreprocessor.compute_coordinate_range(flatten_sample=flatten_sample, coordinate_index=0)

    @staticmethod
    def compute_y_range(sample):
        return SamplePreprocessor.compute_coordinate_range(flatten_sample=sample, coordinate_index=1)

    @staticmethod
    def compute_coordinate_range(flatten_sample, coordinate_index):
        coordinate_values = [point[coordinate_index] for point in flatten_sample]
        coord_min = min(coordinate_values)
        coord_max = max(coordinate_values)
        return coord_min, coord_max

    @staticmethod
    def center_of_mass(flatten_sample):
        x_values = [point[0] for point in flatten_sample]
        y_values = [point[1] for point in flatten_sample]
        points_number = float(len(x_values))
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        return sum_x / points_number, sum_y / points_number

    @staticmethod
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
                x, y = SamplePreprocessor.xy_from_points(point_a, point_b)
                y = abs(y)
                rads = math.atan2(x, y)
                if abs(rads) <= 50.0:
                    slant += rads
                    vectors_count += 1
        slant = slant / vectors_count
        return slant

    @staticmethod
    def xy_from_points(a, b):
        xs = b[0] - a[0]
        ys = b[1] - a[1]
        return xs, ys

    @staticmethod
    def rotate(origin, point, angle):
        """
        Rotate the point around origin by the angle (counter-clockwise)
        :param origin: point around which we perform the rotation
        :param point: point which position we want to change
        :param angle: angle given in radians
        :return: coordinates of the rotated point
        """
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy

    @staticmethod
    def rotate_sample(sample, centre_of_mass, angle_rads):
        rotated_sample = []
        for i in range(len(sample)):
            stroke = sample[i]
            stroke = [SamplePreprocessor.rotate(centre_of_mass, point, angle_rads) for point in stroke]
            rotated_sample.append(stroke)
        return rotated_sample

    @staticmethod
    def scale_sample(scale, sample):
        scaled_sample = []
        for i in range(len(sample)):
            stroke = sample[i]
            stroke = [(point[0] * scale, point[1] * scale) for point in stroke]
            scaled_sample.append(stroke)
        return scaled_sample

    @staticmethod
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
