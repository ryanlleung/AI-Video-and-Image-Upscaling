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


## VIDEO ##
path = "xxx"
scale = 2
fps = 25 #### CHECK THIS ####

cap = cv2.VideoCapture('video_in/'+path+'.mp4')
if cap.isOpened() == False:
    print('ERROR: FILE NOT FOUND OR WRONG CODEC USED!')

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

writer = cv2.VideoWriter('video_out/'+path+'_up.mp4',cv2.VideoWriter_fourcc(*'XVID'),fps,(width*scale,height*scale))

t0 = time.time()
while cap.isOpened():
    ret,frame = cap.read()
    if ret == True:
        ## OPERATIONS ##
        frame = upscale_img(frame,"lapsrn",scale)
        writer.write(frame)
        cv2.imshow('frame',frame)
        ## OUT ##
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()
t1 = time.time()
print("\nElasped time:",np.round(t1-t0,4),"s  | ",np.round((t1-t0)/fps,4),"seconds per frame")
