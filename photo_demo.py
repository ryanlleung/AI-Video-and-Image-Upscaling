# -*- coding: utf-8 -*-

import cv2
from cv2 import dnn_superres
import matplotlib.pyplot as plt
import numpy as np
import time

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


path = "xxx"
image = cv2.imread("cmp_imgs/"+path+".png")
t0 = time.time()
upscaled = upscale_img(image,"lapsrn",2)
t1 = time.time()
print("\nElasped time:",np.round(t1-t0,4),"s")
cv2.imwrite("cmp_imgs/"+path+"_up.png",upscaled)


plt.figure(figsize=(12,8))
plt.subplot(1,2,1)
plt.imshow(image[:,:,::-1])
plt.subplot(1,2,2)
plt.imshow(upscaled[:,:,::-1])
plt.show()
