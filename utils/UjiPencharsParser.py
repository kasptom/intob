import numpy as np

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
                    parts = line.split(sep=" ", maxsplit=3)
                    character_id = parts[1]

                    if character_id not in mapping:
                        continue

                    line = next(iter_file)
                    parts = line.lstrip().split(sep=" ", maxsplit=2)

                    strokes_number = int(parts[1])
                    stroke_points = [[] for _ in range(strokes_number)]

                    for stroke_id in range(strokes_number):
                        line = next(iter_file)
                        parts = line.lstrip().split(sep=" ")
                        points_number = int(parts[1])
                        # every point consists of two coordinates
                        # points start from the 4th element of the line (3rd index)
                        for j in range(4, points_number * 2 + 3, 2):
                            point = (int(parts[j - 1]), int(parts[j]))
                            stroke_points[stroke_id].append(point)

                    penchar = PenChar(character_id, strokes_number, stroke_points)
                    penchars.append(penchar)
        print("TOTAL SAMPLES: ", len(penchars))
        return penchars

penchars = UjiPencharsParser.parse("../data/ujipenchars2.txt")

# print(len(penchars))
o_entity = [penchar for penchar in penchars if penchar.character_id == 'o'][0]
# z_entity = [penchar for penchar in penchars if penchar.character_id == ';'][0]
o_entity.print_penchar()
# z_entity.print_penchar()
#
# z_entity.print_stroke_info()
# x, y = z_entity.to_vector()
# print(x)
# print(y)
