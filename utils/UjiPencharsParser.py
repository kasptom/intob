from model.PenChar import PenChar
from utils.penchars_mapping import mapping


class UjiPencharsParser:
    def __init__(self, debug=False):
        self.shortest_normalized_path = (16, "")
        self.longest_normalized_path = (16, "")
        self.debug = debug

    def parse(self, file_name):
        penchars = []
        problems = 0

        with open(file_name, mode="r") as file:
            iter_file = iter(file)
            for line in iter_file:
                if line.lstrip().startswith("//"):
                    continue
                elif line.startswith("WORD"):
                    parts = line.split(sep=" ", maxsplit=3)
                    character_id = parts[1]
                    unique_identifier = character_id + "_" + parts[2].rstrip()

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

                    penchar = PenChar(character_id, strokes_number, stroke_points, unique_identifier, self.debug)
                    if penchar.status != "OK":
                        problems += 1
                        if self.shortest_normalized_path[0] > penchar.normalized_path_size:
                            self.shortest_normalized_path = (penchar.normalized_path_size, penchar.unique_identifier)
                        if self.longest_normalized_path[0] < penchar.normalized_path_size:
                            self.longest_normalized_path = (penchar.normalized_path_size, penchar.unique_identifier)
                    penchars.append(penchar)
        print("TOTAL SAMPLES: ", len(penchars))
        print("PROBLEMS: ", problems)
        print("SHORTEST PATH: {} {}".format(self.shortest_normalized_path[0], self.shortest_normalized_path[1]))
        print("LONGEST PATH: {}, {}".format(self.longest_normalized_path[0], self.longest_normalized_path[1]))
        return penchars


parser = UjiPencharsParser(debug=False)
penchars = parser.parse("../data/ujipenchars2.txt")

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
