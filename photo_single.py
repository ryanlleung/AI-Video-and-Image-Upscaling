# -*- coding: utf-8 -*-

import numpy as np
import time

from img_ops import *


path = "tom"
model = "lapsrn"
scale = 0.7

image = cv2.imread("image_src/"+path+".png")
t0 = time.time()
upscaled = upscale_img(image,model,scale)
t1 = time.time()
print("\nElasped time:",np.round(t1-t0,4),"s")
cv2.imwrite("image_dst/"+path+"_up.png",upscaled)

print(image.shape)
print(upscaled.shape)
print(upscaled.shape[0]/image.shape[0])

plt.figure(figsize=(5,3))
plt.subplot(1,2,1)
plt.imshow(image[:,:,::-1])
plt.subplot(1,2,2)
plt.imshow(upscaled[:,:,::-1])
plt.show()
