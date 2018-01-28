from keras import Sequential
from keras.layers import LSTM, Dense, np

from data import preprocessed_glyphs
from model.raw_chars_to_vector import M, to_vectors_and_labels
from utils.mappings.penchars_mapping_2 import SAMPLES_PER_WRITER, CLASSES_NUMBER, mapping

batch_size = SAMPLES_PER_WRITER

TIME_STEPS = M
POINT_DIM = 2
DROPOUT = 0.2
RECURRENT_DROPOUT = 0.2

print('Loading data...')

glyphs = preprocessed_glyphs(mapping)
vectors, glyph_labels = to_vectors_and_labels(glyphs)

train_vecs = vectors[0:50 * SAMPLES_PER_WRITER]
test_vecs = vectors[50 * SAMPLES_PER_WRITER:60 * SAMPLES_PER_WRITER]

counter = 0

train_batches = [np.array(train_vecs[x:x + batch_size]) for x in range(0, len(train_vecs), batch_size)]
test_batches = [np.array(test_vecs[x:x + batch_size]) for x in range(0, len(test_vecs), batch_size)]

x_train = np.array(train_batches)
x_test = np.array(test_batches)

y_train = np.array(glyph_labels[0:50 * SAMPLES_PER_WRITER])
y_test = np.array(glyph_labels[50 * SAMPLES_PER_WRITER:60 * SAMPLES_PER_WRITER])

print(len(x_train), 'train sequences')
print(len(x_test), 'test sequences')

print('Build model...')
model = Sequential()
model.add(LSTM(200, input_shape=(TIME_STEPS, POINT_DIM), dropout=DROPOUT, recurrent_dropout=RECURRENT_DROPOUT))
model.add(Dense(CLASSES_NUMBER, activation='softmax'))

# try using different optimizers and different optimizer configs
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
print(model.summary())

print('Train...')
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=15,
          validation_data=(x_test, y_test))
score, acc = model.evaluate(x_test, y_test,
                            batch_size=batch_size)
print('Test score:', score)
print('Test accuracy:', acc)
