# -*- coding: utf-8 -*-

import os
import numpy as np
import time

from img_ops import *


scale = 4
show = True
names = []
direc = os.fsencode("photo_src")
for file in os.listdir(direc):
    names.append(os.fsdecode(file))

t0 = time.time()

errlist = []
for i in range(0,len(names)):
    path = names[i]
    image = cv2.imread("photo_src/"+path)
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
