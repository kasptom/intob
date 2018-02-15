from typing import List

from keras import Sequential
from keras.layers import LSTM, Dense

from data import Glyph
from model.raw_chars_to_vector import M, to_vectors_and_labels
from solver.base_solver import Solver
from utils.mappings.penchars_mapping_2 import SAMPLES_PER_WRITER, CLASSES_NUMBER

TIME_STEPS = M
SECTION_DIM = 4
DROPOUT = 0.2
RECURRENT_DROPOUT = 0.2


class LstmSolver(Solver):
    def set_batch_size(self):
        self.batch_size = int(SAMPLES_PER_WRITER / 4)

    def generate_vectors(self, glyphs_data: List[Glyph]):
        return to_vectors_and_labels(glyphs_data)

    def create_model(self):
        print('Build model...')
        model = Sequential()
        model.add(
            LSTM(200, input_shape=(TIME_STEPS, SECTION_DIM), dropout=DROPOUT, recurrent_dropout=RECURRENT_DROPOUT))
        model.add(Dense(CLASSES_NUMBER, activation='softmax'))

        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])
        print(model.summary())
        return model

    def save_model(self):
        self.model.save("lstm_glyphs.h5")
