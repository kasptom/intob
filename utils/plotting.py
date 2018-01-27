from typing import List
from data import RawChar

import matplotlib.pyplot as plt


def draw_chars(chars: List[RawChar], cols=10):
    rows = -(-len(chars)//cols)  # rounding up
    r = range(cols * rows)
    for i, s in zip(r, chars):
        plt.subplot(rows, cols, i + 1)
        plt.axis('off')
        plt.title(s.character_id)
        for stroke in s.strokes:
            x, y = stroke.T
            plt.plot(x, -y)
    plt.show()
