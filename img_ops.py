# -*- coding: utf-8 -*-

import os
import sys
import cv2
from cv2 import dnn_superres
from PIL import Image
import matplotlib.pyplot as plt

# Use cv2.imread to read from file to get img as input

# Takes numpy array as input
def display_img(img, cmap=None):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), cmap)
    plt.show()

# Takes numpy array as input, returns discrete upscaled numpy array
def upscale_dscrt(img, path, model, scale):
    sr = dnn_superres.DnnSuperResImpl_create()
    sr.readModel(path)
    sr.setModel(model, scale)
    return sr.upsample(img)

# Takes numpy array as input, returns upscaled numpy array
def upscale_img(img, model='lapsrn', scale=2):

    # Manage invalid parameters
    if scale == 1:
        print('Returned the same image...')
        return img
    if scale > 8 or scale <= 0:
        raise Exception("Error: Scale has to be between 0 and 8.")
    if scale > 4 and model != "lapsrn":
        raise Exception("Error: Only LapSRN can be used for more than 4x.")

    # Downscaling: For scale ]0,1[
    if scale < 1:
        width = int(img.shape[1] * scale)
        height = int(img.shape[0] * scale)
        print('Downscaled by ', str(scale), 'x')
        return cv2.resize(img, (width, height))
    
    # Set discrete upscaling scale
    if model == 'lapsrn':
        if scale > 4: sc = 8
        elif scale > 2: sc = 4
        elif scale > 1: sc = 2
        else: sc = 1
    else:
        if scale > 3: sc = 4
        elif scale > 2: sc = 3
        elif scale > 1: sc = 2
        else: sc = 1

    # Upscaling: For scale ]1,8]
    if model == "lapsrn": # x2, x4, x8:
        path = "models/LapSRN_x" + str(sc) + ".pb"
        print("Using LapSRN...")
    elif model == "edsr": # x2, x3, x4
        path = "models/EDSR_x" + str(sc) + ".pb"
        print("Using EDSR...")
    elif model == "espcn": # x2, x3, x4
        path = "models/ESPCN_x" + str(sc) + ".pb"
        print("Using ESPCN...")
    elif model == "fsrcnn": # x2, x3, x4
        path = "models/FSRCNN_x" + str(sc) + ".pb"
        print("Using FSRCNN...")
    else:
        print("Error: Model not available... Check spelling.")
        raise sys.exit()

    # Discrete upscaling
    upscaled = upscale_dscrt(img, path, model, sc)
    
    # Resize to continuous scale by downscaling
    width = int(upscaled.shape[1] * scale / sc)
    height = int(upscaled.shape[0] * scale / sc)
    print('Upscaled by ', str(scale), ' using ', model, 'x', str(sc))

    return cv2.resize(upscaled, (width, height))

# Takes input and output path as input, returns upscaled numpy array
def upscale_ff(input_path ,output_path, model='lapsrn', scale=2):
    
    # Check if input file is an image
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']
    input_ext = os.path.splitext(input_path)[1].lower()
    output_ext = os.path.splitext(output_path)[1].lower()
    if input_ext not in image_extensions:
        raise Exception("Error: Input file is not an image.")
    if output_ext not in image_extensions:
        raise Exception("Error: Output file is not an image.")
    
    try: img = cv2.imread(input_path)
    except: raise Exception("Error: Input file not found.")

    upscaled = upscale_img(img, model, scale)

    try: cv2.imwrite(output_path, upscaled)
    except: raise Exception("Error: Output file could not be written.")
    else: print("Upscaled image saved to", output_path)

    return upscaled

if __name__ == '__main__':
    upscale_ff("taeni.png", "taeni_s.png", "edsr", 2.32)
