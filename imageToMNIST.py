from PIL import Image, ImageFilter
from matplotlib import pyplot as plt
import numpy as np

np.set_printoptions(linewidth=500)

def convertImage(png):
    pic = Image.open(png).convert('L')
    width = float(pic.size[0])
    height = float(pic.size[1])
    newImage = Image.new('L', (28, 28), (255))

    nwidth = int(round((20.0 / height * width), 0))
    img = pic.resize((nwidth, 20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
    wleft = int(round(((28 - nwidth) / 2), 0))
    newImage.paste(img, (wleft, 4))

    pixels = list(newImage.getdata())
    normPixels = [(255 - x) * 1.0 / 255.0 for x in pixels]

    return normPixels

def displayMNIST(mnist):
    newArr=[[0 for d in range(28)] for y in range(28)]
    k = 0
    for i in range(28):
        for j in range(28):
            newArr[i][j]=x[0][k]
            k += 1
"""
    plt.imshow(newArr, interpolation='nearest')
    plt.savefig('MNIST_IMAGE.png')
    plt.show()
    return newArr
"""
x = [convertImage('./image.png')]

mnistImage = np.array(displayMNIST(x))
mnistImage = np.expand_dims(mnistImage, axis=0)
mnistImage = np.expand_dims(mnistImage, axis=-1)
#print(mnistImage.shape)
