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
def upscale_img(img, model='lapsrn', scale=None, height=None, width=None):

    if scale is None:
        if height is None and width is None:
            raise Exception("Error: Either scale or height or width has to be specified.")
        elif height is not None and width is not None:
            raise Exception("Error: Only height or width can be specified.")
        elif height is not None:
            new_height = height # ensure output height is correct
            scale = float(height) / img.shape[0]
        elif width is not None:
            new_width = width # ensure output width is correct
            scale = float(width) / img.shape[1]

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
        raise Exception("Error: Model not available... Check spelling.")

    # Discrete upscaling
    upscaled = upscale_dscrt(img, path, model, sc)
    
    # Resize to continuous scale by downscaling
    swidth = int(upscaled.shape[1] * scale / sc)
    sheight = int(upscaled.shape[0] * scale / sc)
    print('Upscaled by ', str(scale), ' using ', model, 'x', str(sc))
    resized = cv2.resize(upscaled, (swidth, sheight))

    print(f'Resized image shape: {resized.shape}')

    # Check if output height or width is correct
    if height is not None:
        if resized.shape[0] != new_height:
            width = int(resized.shape[1] * (float(new_height) / resized.shape[0]))
            resized = cv2.resize(resized, (width, new_height))
    elif width is not None:
        if resized.shape[1] != new_width:
            height = int(resized.shape[0] * (float(new_width) / resized.shape[1]))
            resized = cv2.resize(resized, (new_width, height))

    return resized

# Takes input and output path as input, returns upscaled numpy array
def upscale_ff(input_path ,output_path, model='lapsrn', scale=None, height=None, width=None):
    
    if not os.path.exists(input_path):
        raise Exception("Error: Input file not found.")

    if height is not None and width is not None:
        raise Exception("Error: Only height or width can be specified.")

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

    if height is None and width is None:
        upscaled = upscale_img(img, model, scale=scale)
    elif height is not None:
        upscaled = upscale_img(img, model, height=height)
    elif width is not None:
        upscaled = upscale_img(img, model, width=width)

    print(f'Input image shape: {img.shape}')
    print(f'Output image shape: {upscaled.shape}')
    print(f'Scale: {upscaled.shape[1] / img.shape[1]}x')

    try: cv2.imwrite(output_path, upscaled)
    except: raise Exception("Error: Output file could not be written.")
    else: print("Upscaled image saved to", output_path)

    return upscaled

if __name__ == '__main__':
    upscale_ff("image_src/Stage.png", "image_dst/Stage_r.png", "lapsrn", height=2000)
