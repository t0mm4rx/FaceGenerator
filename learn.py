import numpy as np
import tensorflow as tf
import dataset
from PIL import Image

if __name__ != "__main__":
    exit(0)

dataset = dataset.get_dataset()

train_set = np.array(dataset[:697])
test_set = np.array(dataset[697:])

print("Train set : {}".format(len(train_set)))
print("Test set : {}".format(len(test_set)))

# We define out model
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(512, input_shape=(12288,), activation='sigmoid'))
model.add(tf.keras.layers.Dense(32, activation='relu'))
model.add(tf.keras.layers.Dense(512, activation='relu'))
model.add(tf.keras.layers.Dense(12288, activation='sigmoid'))

# We train it
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(train_set, train_set, epochs=50, batch_size=32, validation_data=(test_set, test_set))
#loss, acc = model.evaluate(test_set, test_set)
#print('Test Accuracy: {}'.format(acc))

# We visualize one example
predictions = model.predict(np.array(test_set[0:10]))
for i in range(10):
    img = predictions[i]
    img = img * 255
    img = img.reshape((64, 64, 3))
    img = img.astype(np.uint8)

    pil_img = Image.fromarray(img)
    pil_img.save("./results/test{}.png".format(i))
