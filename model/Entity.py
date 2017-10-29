import math
import numpy as np

from model.Direction import Direction

PI = math.pi


class Entity:
    def __init__(self):
        self.character_id = ''  # character UTF-8 id
        self.strokes_number = 0  # number of strokes - max 6
        self.all_points_number = 0  # overall points number
        self.num_points = np.array([0] * 6)  # number of points for each stroke (max 6 strokes)
        self.num_vectors = np.array([[0] * 8] * 6)  # number of vectors of each type (direction) for each stroke

    def increase_vectors_number(self, stroke_id, point_a, point_b):
        x, y = Entity.xy_from_points(point_a, point_b)
        rads = math.atan2(x, y)
        direction_to_increase = Direction.get_direction(rads)
        self.num_vectors[stroke_id, direction_to_increase] += 1

    @staticmethod
    def xy_from_points(a, b):
        xs = b[0] - a[0]
        ys = b[1] - a[1]
        return xs, ys


ent = Entity()
# ent.increase_vectors_number(0, (10.0, 10), (20.0, 20.0))
# ent.increase_vectors_number(0, (10.0, 0), (0.0, 10.0))

# print(ent.num_vectors)
# x, y = Entity.xy_from_points((0, 0), (0, 10))
# print(x, y, math.atan2(x, y) / PI * 180)
# x, y = Entity.xy_from_points((0, 0), (10, 10))
# print(x, y, math.atan2(x, y) / PI * 180)
# x, y = Entity.xy_from_points((0, 0), (10, 0))
# print(x, y, math.atan2(x, y) / PI * 180)
# x, y = Entity.xy_from_points((0, 0), (10, -10))
# print(x, y, math.atan2(x, y) / PI * 180)
# x, y = Entity.xy_from_points((0, 0), (0, -10))
# print(x, y, math.atan2(x, y) / PI * 180)
# x, y = Entity.xy_from_points((0, 0), (-10, -10))
# print(x, y, math.atan2(x, y) / PI * 180)
# x, y = Entity.xy_from_points((0, 0), (-10, 0))
# print(x, y, math.atan2(x, y) / PI * 180)
# x, y = Entity.xy_from_points((0, 0), (-10, 10))
# print(x, y, math.atan2(x, y) / PI * 180)

ent.increase_vectors_number(0, (0, 0), (0, 10))
print(ent.num_vectors[0])
ent.increase_vectors_number(0, (0, 0), (10, 10))
print(ent.num_vectors[0])
ent.increase_vectors_number(0, (0, 0), (10, 0))
print(ent.num_vectors[0])
ent.increase_vectors_number(0, (0, 0), (10, -10))
print(ent.num_vectors[0])
ent.increase_vectors_number(0, (0, 0), (0, -10))
print(ent.num_vectors[0])
ent.increase_vectors_number(0, (0, 0), (-10, -10))
print(ent.num_vectors[0])
ent.increase_vectors_number(0, (0, 0), (-10, 0))
print(ent.num_vectors[0])
ent.increase_vectors_number(0, (0, 0), (-10, 10))
print(ent.num_vectors[0])
