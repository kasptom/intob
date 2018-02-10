from typing import List

from keras import Sequential, optimizers
from keras.layers import Dense, Activation, np

from data import raw_glyphs, Glyph, preprocessed_glyphs
from model.raw_chars_to_vector import W, H, to_vectors_72
from utils.mappings.penchars_mapping import CLASSES_NUMBER, SAMPLES_PER_WRITER, mapping
from utils.penchar_preprocessor import get_sections_number_distribution

X_SIZE = W * H * 8


class Solver:
    def __init__(self, glyphs_data: List[Glyph]):
        self.char_vectors = to_vectors_72(glyphs_data)

        self.model = Sequential()
        self.model.add(Dense(CLASSES_NUMBER, kernel_initializer='uniform', input_shape=(X_SIZE,)))
        self.model.add(Activation('tanh'))
        self.model.add(Activation('softmax'))

        sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        self.model.compile(loss='mean_squared_error', optimizer=sgd, metrics=['accuracy'])

    def train(self):
        train_vecs = self.char_vectors[0 * SAMPLES_PER_WRITER:50 * SAMPLES_PER_WRITER]
        test_vecs = self.char_vectors[50 * SAMPLES_PER_WRITER:60 * SAMPLES_PER_WRITER]

        train_x = np.array([penchar_data[0] for penchar_data in train_vecs])
        train_y = np.array([penchar_data[1] for penchar_data in train_vecs])

        test_x = np.array([penchar_data[0] for penchar_data in test_vecs])
        test_y = np.array([penchar_data[1] for penchar_data in test_vecs])

        self.model.fit(train_x, train_y, batch_size=1, epochs=15)

        self.model.evaluate(test_x, test_y, 1)

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
