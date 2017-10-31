import tensorflow as tf

from model.PenChar import PenChar
from utils.UjiPencharsParser import UjiPencharsParser


class Solver:
    def __init__(self, penchars):
        self.penchars = penchars
        self.x = tf.placeholder(tf.float32, shape=[None, 55])
        self.y_ = tf.placeholder(tf.float32, shape=[None, 64])
        self.W = tf.Variable(tf.zeros([55, 64]))
        self.b = tf.Variable(tf.zeros([64]))
        self.y = tf.matmul(self.x, self.W) + self.b

        self.cross_entropy = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits(labels=self.y_, logits=self.y))
        self.train_step = tf.train.GradientDescentOptimizer(0.5).minimize(self.cross_entropy)

    def train(self):
        sess = tf.InteractiveSession()
        tf.global_variables_initializer().run()

        penchar_vectors = PenChar.to_vectors(self.penchars)

        for i in range(50):  # 50 out of 60 writers
            # 194 - samples per writer
            train_vecs = penchar_vectors[i * 194:(i + 1) * 194]
            batch_xs = [penchar_data[0] for penchar_data in train_vecs]
            batch_ys = [penchar_data[1] for penchar_data in train_vecs]
            sess.run(self.train_step, feed_dict={self.x: batch_xs, self.y_: batch_ys})

        test_vecs = penchar_vectors[11640-1164:11640]
        # cs_vecs = penchar_vectors[1000:1164]
        # test trained model
        test_x = [penchar_data[0] for penchar_data in test_vecs]
        test_y = [penchar_data[1] for penchar_data in test_vecs]
        correct_prediction = tf.equal(tf.argmax(self.y, 1), tf.argmax(self.y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        print(sess.run(accuracy, feed_dict={self.x: test_x,
                                            self.y_: test_y}))


penchars = UjiPencharsParser.parse("../data/ujipenchars2.txt")
solver = Solver(penchars)
solver.train()
