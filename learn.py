import numpy as np
import tensorflow as tf
import dataset
from PIL import Image
import os

if __name__ != "__main__":
    exit(0)

dataset = dataset.get_dataset()

train_set = np.array(dataset[:697])
test_set = np.array(dataset[697:])

print("Train set : {}".format(len(train_set)))
print("Test set : {}".format(len(test_set)))

# We define out model
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(4048, input_shape=(12288,), activation='sigmoid'))
model.add(tf.keras.layers.Dense(1024, activation='relu'))
model.add(tf.keras.layers.Dense(512, activation='relu'))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(512, activation='relu'))
model.add(tf.keras.layers.Dense(1024, activation='relu'))
model.add(tf.keras.layers.Dense(4048, activation='relu'))
model.add(tf.keras.layers.Dense(12288, activation='sigmoid'))

# We train it
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(train_set, train_set, epochs=25, batch_size=32, validation_data=(test_set, test_set))
#loss, acc = model.evaluate(test_set, test_set)
#print('Test Accuracy: {}'.format(acc))

# We visualize examples

def encode_decode(folder, file):
    os.system("mkdir -p ./results/{}".format(folder))
    image = Image.open("./dataset1/{}".format(file))
    image = np.array(image).reshape((12288,))
    image = image / 255
    prediction = model.predict(np.array([image]))[0]
    prediction = prediction * 255
    prediction = prediction.reshape((64, 64, 3))
    prediction = prediction.astype(np.uint8)

    pil_img = Image.fromarray(prediction)
    pil_img.save("./results/{}/test_{}.png".format(folder, file))

logins = ["vgoldman", "tmarx", "dyoann", "dzementz", "anloubie", "vparekh", "mashar"]
for login in logins:
    encode_decode("model3", "{}.jpg".format(login))
