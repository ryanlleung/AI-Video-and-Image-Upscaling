# -*- coding: utf-8 -*-

import os
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


scale = 4
show = True
names = []
direc = os.fsencode("photo_in")
for file in os.listdir(direc):
    names.append(os.fsdecode(file))
t0 = time.time()
errlist = []
for i in range(0,len(names)):
    path = names[i]
    image = cv2.imread("photo_in/"+path)
    x,y,c = image.shape
    if x*scale > 6000 or y*scale > 6000:
        errlist.append((i,names[i]))
        continue
    upscaled = upscale_img(image,"edsr",scale)
    cv2.imwrite("photo_out/"+path[:-4]+"_up.png",upscaled)
    if show == True:
        plt.figure(figsize=(12,8))
        plt.subplot(1,2,1)
        plt.imshow(image[:,:,::-1])
        plt.subplot(1,2,2)
        plt.imshow(upscaled[:,:,::-1])
        plt.show()
    t1 = time.time()
    print("\nElasped time:",np.round(t1-t0,4),"s  | ",i+1-len(errlist),"out of",len(names)-len(errlist))
if len(errlist) != 0:
    print("\nThe photos below are too large:")
    for i in errlist:
        print(i)
