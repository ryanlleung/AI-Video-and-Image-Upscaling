# -*- coding: utf-8 -*-

import numpy as np
import time

from img_ops import *


## VIDEO ##
path = "stopwatch"
scale = .2
fps = 30 #### CHECK THIS ####

cap = cv2.VideoCapture('video_src/'+path+'.mp4')
if cap.isOpened() == False:
    print('ERROR: FILE NOT FOUND OR WRONG CODEC USED!')

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

writer = cv2.VideoWriter('video_dst/'+path+'_up.mp4',cv2.VideoWriter_fourcc(*'XVID'),fps,(int(width*scale),int(height*scale)))

t0 = time.time()
while cap.isOpened():
    ret,frame = cap.read()
    if ret == True:
        ## OPERATIONS ##
        frame = upscale_img(frame,"fsrcnn",scale)
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
