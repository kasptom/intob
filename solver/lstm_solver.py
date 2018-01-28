from keras import Sequential
from keras.layers import LSTM, Dense, np

from data import preprocessed_glyphs
from model.raw_chars_to_vector import M, to_vectors_and_labels
from utils.mappings.penchars_mapping_2 import SAMPLES_PER_WRITER, CLASSES_NUMBER, mapping

batch_size = int(SAMPLES_PER_WRITER / 4)

TIME_STEPS = M
SECTION_DIM = 4
DROPOUT = 0.2
RECURRENT_DROPOUT = 0.2

print('Loading data...')

glyphs = preprocessed_glyphs(mapping)
vectors, glyph_labels = to_vectors_and_labels(glyphs)

train_vecs = vectors[0:42 * SAMPLES_PER_WRITER]
valid_vecs = vectors[42 * SAMPLES_PER_WRITER:54 * SAMPLES_PER_WRITER]
test_vecs = vectors[54 * SAMPLES_PER_WRITER:60 * SAMPLES_PER_WRITER]

x_train = np.array(train_vecs)
x_valid = np.array(valid_vecs)
x_test = np.array(test_vecs)

y_train = np.array(glyph_labels[0:42 * SAMPLES_PER_WRITER])
y_valid = np.array(glyph_labels[42 * SAMPLES_PER_WRITER:54 * SAMPLES_PER_WRITER])
y_test = np.array(glyph_labels[54 * SAMPLES_PER_WRITER:60 * SAMPLES_PER_WRITER])

print(len(x_train), 'train sequences')
print(len(x_test), 'test sequences')

print('Build model...')
model = Sequential()
model.add(LSTM(200, input_shape=(TIME_STEPS, SECTION_DIM), dropout=DROPOUT, recurrent_dropout=RECURRENT_DROPOUT))
model.add(Dense(CLASSES_NUMBER, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
print(model.summary())

print('Train...')
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=15,
          validation_data=(x_valid, y_valid))
score, acc = model.evaluate(x_test, y_test,
                            batch_size=batch_size)
print('Test score:', score)
print('Test accuracy:', acc)

model.save("lstm_glyphs.h5")
