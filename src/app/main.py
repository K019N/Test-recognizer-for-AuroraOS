import cv2 as cv
import numpy as np

from .camera_reciver import *

#TODO: buttons not working now
#def back_button(*args):
#    pass

camera = cv.VideoCapture(0) 
app = CameraReciver()
if (app.exists_device(camera)): app.runCamera(camera)
#cv.createButton("Back", back_button, None, cv.QT_PUSH_BUTTON,1)
