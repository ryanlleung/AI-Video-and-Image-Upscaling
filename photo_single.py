# -*- coding: utf-8 -*-

import numpy as np
import time

from img_ops import *


path = "tom"
model = "edsr"
scale = 1

img = cv2.imread("image_src/"+path+".png")
t0 = time.time()
upscaled = upscale_img(img,model,scale)
t1 = time.time()
print("\nElasped time:",np.round(t1-t0,4),"s")
cv2.imwrite("image_dst/"+path+"_up.png",upscaled)

print(img.shape)
print(upscaled.shape)
print(upscaled.shape[0]/img.shape[0])

plt.figure(figsize=(5,3))
plt.subplot(1,2,1)
plt.imshow(img[:,:,::-1])
plt.subplot(1,2,2)
plt.imshow(upscaled[:,:,::-1])
plt.show()
