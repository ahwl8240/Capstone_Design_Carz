import cv2
from cv2 import dnn_superres
import matplotlib.pyplot as plt
# Create an SR object
sr = dnn_superres.DnnSuperResImpl_create()

# Read image
image = cv2.imread('testimg/test4.jpg')

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
cv2.imwrite("test_result/upscaled.png", result)


