from PIL import Image
import numpy as np
import os

def get_dataset():
    res = []
    for file in os.listdir("./dataset1/"):
        image = Image.open("./dataset1/{}".format(file))
        temp = np.array(image).reshape((12288,))
        temp = temp / 255
        res.append(temp)
    return res
