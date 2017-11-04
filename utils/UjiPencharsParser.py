from model.PenChar import PenChar
from utils.penchars_mapping import mapping


class UjiPencharsParser:
    def __init__(self, debug=False):
        self.shortest_normalized_path = (16, "")
        self.longest_normalized_path = (16, "")
        self.debug = debug
        self.x_range = [-1, -1]
        self.y_range = [-1, -1]
        self.x_range_names = ["sample_id", "sample_id"]
        self.y_range_names = ["sample_id", "sample_id"]
        self.train_count = 0
        self.test_count = 0

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
                    sample_id = parts[2].rstrip()
                    unique_identifier = character_id + "_" + sample_id

                    if character_id not in mapping:
                        continue
                    if sample_id.startswith("trn"):
                        self.train_count += 1
                    if sample_id.startswith("tst"):
                        self.test_count += 1

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
                            self.update_range(point, unique_identifier)
                            stroke_points[stroke_id].append(point)

                    penchar = PenChar(character_id, strokes_number, stroke_points, unique_identifier, self.debug)
                    if penchar.status != "OK":
                        problems += 1
                        if self.shortest_normalized_path[0] > penchar.normalized_path_size:
                            self.shortest_normalized_path = (penchar.normalized_path_size, penchar.unique_identifier)
                        if self.longest_normalized_path[0] < penchar.normalized_path_size:
                            self.longest_normalized_path = (penchar.normalized_path_size, penchar.unique_identifier)
                    penchars.append(penchar)
        print("Total samples: ", len(penchars))
        print("Problems: ", problems)
        print("Shortest path: {} {}".format(self.shortest_normalized_path[0], self.shortest_normalized_path[1]))
        print("Longest path: {}, {}".format(self.longest_normalized_path[0], self.longest_normalized_path[1]))
        print("x range: {} {}".format(self.x_range, self.x_range_names))
        print("y range: {} {}".format(self.y_range, self.y_range_names))
        print("test samples count: ", self.test_count)
        print("train samples count: ", self.train_count)
        return penchars

    def update_range(self, xy, sample_id):
        if self.x_range[0] == -1 or self.x_range[0] > xy[0]:
            self.x_range[0] = xy[0]
            self.x_range_names[0] = sample_id
        if self.x_range[1] == -1 or self.x_range[1] < xy[0]:
            self.x_range[1] = xy[1]
            self.x_range_names[1] = sample_id
        if self.y_range[0] == -1 or self.y_range[0] > xy[1]:
            self.y_range[0] = xy[0]
            self.y_range_names[0] = sample_id
        if self.y_range[1] == -1 or self.y_range[1] < xy[1]:
            self.y_range[1] = xy[1]
            self.y_range_names[1] = sample_id

parser = UjiPencharsParser(debug=False)
penchars = parser.parse("../data/ujipenchars2.txt")

# print(len(penchars))
x_min_entity = [penchar for penchar in penchars if penchar.unique_identifier == parser.x_range_names[0]][0]
x_min_entity.draw_normalized_path()
x_min_entity.draw_path("x_min")

x_max_entity = [penchar for penchar in penchars if penchar.unique_identifier == parser.x_range_names[1]][0]
x_max_entity.draw_normalized_path()
x_max_entity.draw_path("x_max")

y_min_entity = [penchar for penchar in penchars if penchar.unique_identifier == parser.y_range_names[0]][0]
y_min_entity.draw_normalized_path()
y_min_entity.draw_path("y_min")

y_max_entity = [penchar for penchar in penchars if penchar.unique_identifier == parser.y_range_names[1]][0]
y_max_entity.draw_normalized_path()
y_max_entity.draw_path("y_max")

# z_entity = [penchar for penchar in penchars if penchar.character_id == ';'][0]
# o_entity.print_penchar()
# z_entity.print_penchar()
#
# z_entity.print_stroke_info()
# x, y = z_entity.to_vector()
# print(x)
# print(y)
