from typing import List

from keras import callbacks
from keras.layers import np

from data import raw_glyphs, Glyph, preprocessed_glyphs
from model.raw_chars_to_vector import W, H
from utils.get_file import create_file_and_folders_if_not_exist
from utils.mappings.penchars_mapping import SAMPLES_PER_WRITER, mapping
from utils.penchar_preprocessor import get_sections_number_distribution

X_SIZE = W * H * 8
EPOCH_PATIENCE = 3
EPOCHS_LIMIT = 100

class Solver:
    def __init__(self, glyphs_data: List[Glyph]):
        self.char_vectors, self.char_labels = self.generate_vectors(glyphs_data)
        self.model = self.create_model()
        self.batch_size = self.set_batch_size()

    def generate_vectors(self, glyphs_data: List[Glyph]):
        raise NotImplementedError()

    def create_model(self):
        raise NotImplementedError()

    def get_csv_log_file_name(self):
        raise NotImplementedError()

    def save_model(self):
        raise NotImplementedError()

    def set_batch_size(self):
        raise NotImplementedError()

    def train(self):
        create_file_and_folders_if_not_exist(self.get_csv_log_file_name())
        _callbacks = [callbacks.EarlyStopping(monitor='val_loss', patience=EPOCH_PATIENCE),
                      callbacks.CSVLogger(self.get_csv_log_file_name())]

        train_x = np.array(self.char_vectors[0 * SAMPLES_PER_WRITER:50 * SAMPLES_PER_WRITER])
        test_x = np.array(self.char_vectors[50 * SAMPLES_PER_WRITER:60 * SAMPLES_PER_WRITER])

        train_y = np.array(self.char_labels[0 * SAMPLES_PER_WRITER:50 * SAMPLES_PER_WRITER])
        test_y = np.array(self.char_labels[50 * SAMPLES_PER_WRITER:60 * SAMPLES_PER_WRITER])

        self.model.fit(train_x, train_y, batch_size=self.batch_size, epochs=EPOCHS_LIMIT, callbacks=_callbacks)

        self.model.evaluate(test_x, test_y, batch_size=self.batch_size)

        self.save_model()

        score, acc = self.model.evaluate(test_x, test_y)

        print('Score: %f' % score)
        print('Test accuracy: %f%%' % (acc * 100))
        print('Score', score)


if __name__ == '__main__':
    raw_chars = raw_glyphs(mapping)

    glyphs = preprocessed_glyphs(mapping)

    solver = Solver(glyphs)
    print(get_sections_number_distribution())
    solver.train()
