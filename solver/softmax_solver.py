from typing import List

from keras import Sequential, optimizers
from keras.layers import Dense, Activation

from data import raw_glyphs, Glyph, preprocessed_glyphs
from model.raw_chars_to_vector import W, H, to_vectors_whd
from solver.base_solver import Solver
from utils.mappings.penchars_mapping import CLASSES_NUMBER, mapping
from utils.penchar_preprocessor import get_sections_number_distribution

X_SIZE = W * H * 8


class SoftmaxSolver(Solver):
    def __init__(self, glyphs_data: List[Glyph]):
        super().__init__(glyphs_data)

    def generate_vectors(self, glyphs_data: List[Glyph]):
        return to_vectors_whd(glyphs_data)

    def create_model(self):
        model = Sequential()
        model.add(Dense(CLASSES_NUMBER, kernel_initializer='uniform', input_shape=(X_SIZE,)))
        model.add(Activation('tanh'))
        model.add(Activation('softmax'))
        sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='mean_squared_error', optimizer=sgd, metrics=['accuracy'])
        return model

    def get_csv_log_file_name(self):
        return "data/log_softmax.csv"

    def save_model(self):
        self.model.save("softmax_glyphs.h5")

    def set_batch_size(self):
        return 1


if __name__ == '__main__':
    raw_chars = raw_glyphs(mapping)

    glyphs = preprocessed_glyphs(mapping)

    solver = Solver(glyphs)
    print(get_sections_number_distribution())
    solver.train()
