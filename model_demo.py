# -*- coding: utf-8 -*-

import cv2
from cv2 import dnn_superres
import matplotlib.pyplot as plt

def display_img(img,cmap=None):
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111)
    ax.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB),cmap)
    plt.show()
    return

# Create an SR object
sr = dnn_superres.DnnSuperResImpl_create()

# Read image
image = cv2.imread("xxx.png")
display_img(image)


# Read the desired model
path = "models/edsr_x4.pb"
sr.readModel(path)

# Set the desired model and scale to get correct pre- and post-processing
sr.setModel("edsr", 4)


# Upscale the image
result = sr.upsample(image)
display_img(result)

# Save the image
cv2.imwrite("upscaled.png", result)
