from typing import List

import tensorflow as tf

from data import raw_glyphs, Glyph, preprocessed_glyphs
from model.raw_chars_to_vector import W, H, to_vectors_72
from utils.mappings.penchars_mapping import CLASSES_NUMBER, SAMPLES_PER_WRITER, mapping
from utils.penchar_preprocessor import get_sections_number_distribution

X_SIZE = W * H * 8


class Solver:
    def __init__(self, raw_chars_data: List[Glyph]):
        self.char_vectors = to_vectors_72(raw_chars_data)
        self.x = tf.placeholder(tf.float32, shape=[None, X_SIZE])
        self.y_ = tf.placeholder(tf.float32, shape=[None, CLASSES_NUMBER])
        self.W = tf.Variable(tf.zeros([X_SIZE, CLASSES_NUMBER]))
        self.b = tf.Variable(tf.zeros([CLASSES_NUMBER]))
        self.y = tf.matmul(self.x, self.W) + self.b

        self.cross_entropy = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits(labels=self.y_, logits=self.y))
        self.train_step = tf.train.GradientDescentOptimizer(0.5).minimize(self.cross_entropy)

    def train(self):
        sess = tf.InteractiveSession()
        tf.global_variables_initializer().run()

        for i in range(50):  # 50 out of 60 writers
            train_vecs = self.char_vectors[i * SAMPLES_PER_WRITER:(i + 1) * SAMPLES_PER_WRITER]
            batch_xs = [penchar_data[0] for penchar_data in train_vecs]
            batch_ys = [penchar_data[1] for penchar_data in train_vecs]
            sess.run(self.train_step, feed_dict={self.x: batch_xs, self.y_: batch_ys})

        test_vecs = self.char_vectors[50 * SAMPLES_PER_WRITER:60 * SAMPLES_PER_WRITER]
        # cs_vecs = penchar_vectors[1000:1164]
        # test trained model
        test_x = [penchar_data[0] for penchar_data in test_vecs]
        test_y = [penchar_data[1] for penchar_data in test_vecs]
        correct_prediction = tf.equal(tf.argmax(self.y, 1), tf.argmax(self.y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        print(sess.run(accuracy, feed_dict={self.x: test_x,
                                            self.y_: test_y}))


if __name__ == '__main__':
    raw_chars = raw_glyphs(mapping)

    glyphs = preprocessed_glyphs(mapping)

    solver = Solver(glyphs)
    print(get_sections_number_distribution())
    solver.train()
