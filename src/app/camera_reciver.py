import cv2 as cv
import numpy as np
import requests
import json

from image_processor import *
from recognising.table_recog import *
from table_to_results import *


class CameraReciver():
    def __init__(self, id: str):
        self.data_to_recive = {"number": ["x1", "x2", "y1", "y2"]}
        self.server_url = "http://192.168.1.1:8080/"
        self.id = id
    
    #TODO: img counter, now not working anytime zero number ;(
    def take_picture(self, frame, img_counter):
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
        return img_name

    def exists_device(self, cap):
        if cap is None or not cap.isOpened():
            print('Warning: unable to open video source')
            return False
        return True

    def runCamera(self, vid):
        line_counter = 0
        img_counter = 0
        #TODO: connection to real server? 
        while(True): 
            ret, frame = vid.read() 
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            edges = cv.Canny(gray, 50, 150, apertureSize=3)
            lines = cv.HoughLines(edges, 1, np.pi/180, 200)
            ImageProcessor().draw_lines(lines, frame, line_counter, self.data_to_recive)
            cv.imshow('frame', frame)

            #TODO: create buttons in application window
            key = cv.waitKey(1)
            if key % 256 == 27:   #esc 
                break
            
            elif key % 256 == 32:   #space
                pic = self.take_picture(frame, img_counter)
                data = TableRecogniser().recognise(pic)
                exit = Resulter().make_results(data)
                exit = Resulter().compare(exit, requests.get(self.server_url + self.id))
                response = requests.post(self.server_url + self.id, json=exit)
                if response.status_code == 200:
                    result = response.json()
                    print("Результат:", result)
                else:
                    print("Ошибка:", response.status_code)
            
            elif key % 256 == 0:
                self.text_recog.recognise(frame)

        #self.client.send_data(self.data_to_recive)
        vid.release() 
        cv.destroyAllWindows() 