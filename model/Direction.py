from math import pi


class Direction:
    ang = [-180.0] + [-157.5 + k * 45.0 for k in range(8)] + [180]
    # indexes in directions array
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7

    @staticmethod
    def get_direction(angle):
        direction = 0
        angle_deg = angle / pi * 180

        if Direction.ang[0] <= angle_deg < Direction.ang[1] or Direction.ang[8] <= angle_deg <= Direction.ang[9]:
            direction = Direction.S
        if Direction.ang[1] <= angle_deg < Direction.ang[2]:
            direction = Direction.SW
        if Direction.ang[2] <= angle_deg < Direction.ang[3]:
            direction = Direction.W
        if Direction.ang[3] <= angle_deg < Direction.ang[4]:
            direction = Direction.NW
        if Direction.ang[4] <= angle_deg < Direction.ang[5]:
            direction = Direction.N
        if Direction.ang[5] <= angle_deg < Direction.ang[6]:
            direction = Direction.NE
        if Direction.ang[6] <= angle_deg < Direction.ang[7]:
            direction = Direction.E
        if Direction.ang[7] <= angle_deg < Direction.ang[8]:
            direction = Direction.SE
        print(angle_deg, " ", direction)
        return direction

