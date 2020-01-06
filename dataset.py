from PIL import Image
import numpy as np
import os

def get_dataset():
    res = []
    for file in os.listdir("./images/"):
        image = Image.open("./images/{}".format(file))
        print(image.size)
        image.show()
        exit(0)
