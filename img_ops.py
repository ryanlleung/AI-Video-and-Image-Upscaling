import cv2
from cv2 import dnn_superres
import matplotlib.pyplot as plt

def display_img(img,cmap=None):
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111)
    ax.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB),cmap)
    plt.show()
    return

def upscale_img(img,model,x=2):
    if model == "edsr":
        path = "models/EDSR_x"+str(x)+".pb"
    elif model == "espcn":
        path = "models/ESPCN_x"+str(x)+".pb"
    elif model == "fsrcnn":
        path = "models/FSRCNN_x"+str(x)+".pb"
    elif model == "lapsrn":
        path = "models/LapSRN_x"+str(x)+".pb"
    sr = dnn_superres.DnnSuperResImpl_create()
    sr.readModel(path)
    sr.setModel(model,x)
    return sr.upsample(img)