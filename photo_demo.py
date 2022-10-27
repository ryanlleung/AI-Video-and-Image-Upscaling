# -*- coding: utf-8 -*-

import cv2
from cv2 import dnn_superres
import matplotlib.pyplot as plt
import numpy as np
import time

from img_ops import *


path = "plane"
image = cv2.imread("cmp_imgs/"+path+".png")
t0 = time.time()
upscaled = upscale_img(image,"edsr",4)
t1 = time.time()
print("\nElasped time:",np.round(t1-t0,4),"s")
cv2.imwrite("cmp_imgs/"+path+"_up.png",upscaled)


plt.figure(figsize=(12,8))
plt.subplot(1,2,1)
plt.imshow(image[:,:,::-1])
plt.subplot(1,2,2)
plt.imshow(upscaled[:,:,::-1])
plt.show()
