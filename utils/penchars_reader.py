import numpy as np

from utils.penchars_mapping import mapping


def read_file(file_name: str):
    penchars = []
    with open(file_name, mode="r") as file:
        iter_file = iter(file)
        for line in iter_file:
            if line.lstrip().startswith("//"):
                continue
            elif line.startswith("WORD"):
                parts = line.split(" ", 3)
                character_id = parts[1]
                sample_id = parts[2].rstrip()

                if character_id not in mapping:
                    continue

                line = next(iter_file)
                parts = line.lstrip().split(" ", 2)

                strokes_number = int(parts[1])
                strokes = []

                for stroke_id in range(strokes_number):
                    parts = next(iter_file).split()
                    points_number = int(parts[1])
                    points = [int(p) for p in parts[3:]]
                    points = np.array(points, dtype=np.float32).reshape((-1, 2))
                    assert points.shape[0] == points_number
                    strokes.append(points)

                assert len(strokes) == strokes_number

                penchars.append({
                    'character_id': character_id,
                    'sample_id': sample_id,
                    'strokes': strokes
                })
    return penchars


def main():
    penchars = read_file("../data/ujipenchars2.txt")
    print(penchars[0])


if __name__ == '__main__':
    main()