from model.PenChar import PenChar
from utils.penchars_mapping import mapping


class UjiPencharsParser:
    @staticmethod
    def parse(file_name):
        penchars = []

        with open(file_name, mode="r") as file:
            iter_file = iter(file)
            for line in iter_file:
                if line.lstrip().startswith("//"):
                    continue
                elif line.startswith("WORD"):
                    penchar = PenChar()
                    parts = line.split(sep=" ", maxsplit=3)
                    penchar.character_id = parts[1]

                    if penchar.character_id not in mapping:
                        # print("character: " + penchar.character_id + "not in a mapping")
                        continue

                    line = next(iter_file)
                    parts = line.lstrip().split(sep=" ", maxsplit=2)
                    penchar.strokes_number = int(parts[1])
                    for stroke_id in range(penchar.strokes_number):
                        line = next(iter_file)
                        parts = line.lstrip().split(sep=" ")
                        points_number = int(parts[1])
                        penchar.points_per_stroke[stroke_id] = points_number
                        # print(points_number)
                        # every point consists of two coordinates
                        # points start from the 4th element of the line (3rd index)
                        point_b = None
                        for j in range(6, points_number * 2 + 3, 2):
                            point_a = (int(parts[j - 3]), int(parts[j - 2]))
                            penchar.stroke_points.append(point_a)
                            point_b = (int(parts[j - 1]), int(parts[j]))
                            penchar.increase_vectors_number(stroke_id=stroke_id, point_a=point_a, point_b=point_b)
                        if point_b is not None:
                            penchar.stroke_points.append(point_b)
                    penchars.append(penchar)
        print("TOTAL SAMPLES: ", len(penchars))
        return penchars


# penchars = UjiPencharsParser.parse("../data/ujipenchars2.txt")
# print(len(penchars))
# o_entity = [penchar for penchar in penchars if penchar.character_id == 'o'][0]
# z_entity = [penchar for penchar in penchars if penchar.character_id == ';'][0]
# o_entity.print_penchar()
# z_entity.print_penchar()
#
# z_entity.print_stroke_info()
# x, y = z_entity.to_vector()
# print(x)
# print(y)
