import tensorflow as tf


class Solver:
    def __init__(self, entities):
        self.entities = entities
        self.x = tf.placeholder(tf.float32, shape=[None, 55])
        self.y_ = tf.placeholder(tf.float32, shape=[None, 64])
        self.W = tf.Variable(tf.zeros([55, 64]))
        self.b = tf.Variable(tf.zeros([64]))
        self.y = tf.matmul(self.x, self.W) + self.b

        cross_entropy = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits(labels=self.y_, logits=self.y))
        train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

        for _ in range(100):
            pass




    def train(self):
        sess = tf.InteractiveSession()
        tf.global_variables_initializer().run()

