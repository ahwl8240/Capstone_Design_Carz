import cv2
from cv2 import dnn_superres
import matplotlib.pyplot as plt
import os
import numpy as np


def sr_operate(img_path):
    
    # Create an SR object
    sr = dnn_superres.DnnSuperResImpl_create()

    # Read image
    img_array = np.fromfile(img_path,np.uint8)

    #image = cv2.imread(img_path)
    image = cv2.imdecode(img_array,cv2.IMREAD_COLOR)

    # Read the desired model
    path = "FSRCNN_x4.pb"
    sr.readModel(path)

    # Set CUDA backend and target to enable GPU inference
    #sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    #sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    # Set the desired model and scale to get correct pre- and post-processing
    sr.setModel("fsrcnn", 4)

    # Upscale the image
    result = sr.upsample(image)

    # Save the image
    save_path="d:\\carz_operated\\sr_img"
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    cv2.imwrite(save_path+"\\upscaled.png", result)
    return save_path+"\\upscaled.png"


