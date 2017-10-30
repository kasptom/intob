from model.Entity import Entity


class UjiPencharsParser:
    @staticmethod
    def parse(file_name):
        entities = []

        with open(file_name, mode="r") as file:
            iter_file = iter(file)
            for line in iter_file:
                if line.lstrip().startswith("//"):
                    continue
                elif line.startswith("WORD"):
                    entity = Entity()

                    parts = line.split(sep=" ", maxsplit=3)
                    entity.character_id = parts[1]
                    line = next(iter_file)
                    parts = line.lstrip().split(sep=" ", maxsplit=2)
                    entity.strokes_number = int(parts[1])
                    for stroke_id in range(entity.strokes_number):
                        line = next(iter_file)
                        parts = line.lstrip().split(sep=" ")
                        points_number = int(parts[1])
                        # print(points_number)
                        # every point consists of two coordinates
                        # points start from the 4th element of the line (3rd index)
                        for j in range(6, points_number * 2 + 3, 2):
                            point_a = (int(parts[j - 3]), int(parts[j - 2]))
                            point_b = (int(parts[j - 1]), int(parts[j]))
                            entity.increase_vectors_number(stroke_id=stroke_id, point_a=point_a, point_b=point_b)
                    entities.append(entities)
        return entities


penchars = UjiPencharsParser.parse("../data/ujipenchars2.txt")
print(len(penchars))
