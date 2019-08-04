from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import os
import imageToMNIST as itm

print('Tensorflow version: ' + str(tf.__version__))
np.set_printoptions(linewidth=300)

# train_images array of 60000 28x28 images
# train_labels array of 60000 labels for each image
mnist = tf.keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

def show_image(image):
    plt.imshow(image, cmap=plt.cm.binary)
    plt.colorbar()
    plt.grid(False)
    plt.show()

def train_model(checkpoint_path):
    checkpoint_dir = os.path.dirname(checkpoint_path)
    cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, save_weights_only=True, verbose=1)
    model.fit(train_images, train_labels, epochs=5, validation_data=(test_images, test_labels), callbacks=[cp_callback])


train_images = train_images.reshape((60000, 28, 28, 1))
test_images = test_images.reshape((10000, 28, 28, 1))

# Normalize rgb values between 0 and 1
train_images = train_images/255.0
test_images = test_images/255.0

"""# one-hot encoding: reshape labels into array with correct number stored as index
with tf.compat.v1.Session() as sess:
    train_labels = sess.run(tf.one_hot(train_labels, depth=10))
    test_labels = sess.run(tf.one_hot(test_labels, depth=10))
"""

# placeholder: variable used to feed data into (must match data shape and type exactly)
x_train = tf.compat.v1.placeholder(dtype=tf.float32, shape=[None, 784])
y_train = tf.compat.v1.placeholder(dtype=tf.float32, shape=[None, 10])
image = tf.reshape(x_train, shape=[28,28,1])

model = keras.Sequential()
model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(10, activation='softmax'))
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

checkpoint_path = 'training_1/cp.ckpt'
#train_model(checkpoint_path)
model.load_weights(checkpoint_path)

testImage = np.expand_dims(test_images[0], axis=0)
print(itm.mnistImage)
#print(np.argmax(model.predict(itm.mnistImage)))

#loss, acc = model.evaluate(test_images, test_labels)
#print("Restored model, accuracy: {:5.2f}%".format(100*acc))
