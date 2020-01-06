import subprocess
import os
from progress.bar import Bar
from PIL import Image

# We get every 175x175 image, we resize it to 64x64 and we store it in dataset1 folder
full_images = []
os.system("mkdir -p dataset1")

bar = Bar("Searching for users...", max=len(os.listdir("./images/")))
for file in os.listdir("./images/"):
    size = subprocess.check_output(["identify", "-format", "%w,%h", "./images/{}".format(file)]).decode("utf-8").split(",")
    if (int(size[0]) == 175 and int(size[1]) == 175):
        full_images.append("./images/{}".format(file))
    bar.next()
bar.finish()
print("Found {} users".format(len(full_images)))

bar = Bar("Cropping and saving those images...", max=len(full_images))
for file in full_images:
    outfile = "./dataset1/{}".format(file.split("/")[-1])
    try:
        im = Image.open(file)
        im.thumbnail((64, 64), Image.ANTIALIAS)
        im.save(outfile, "JPEG")
    except IOError:
        print("Reshaping error for {} !".format(file))
    bar.next()
bar.finish()
