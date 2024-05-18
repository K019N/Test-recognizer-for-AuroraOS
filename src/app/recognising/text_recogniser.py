import cv2
import pytesseract
from table_data import *


class IRecogniser():
    def __init__(self):
        self.data = Table("")
    
    def recognise(self, img):
        pass
    
    def data_to_table(self, some_data: str):
        self.data = Table(some_data)

    def get_data(self):
        return self.data.data
    

class TextRecogniser(IRecogniser):
    def __init__(self):
        self.data = {}
    
    def recognise(self, img):
        pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\\tesseract.exe"

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        invert = 255 - opening

        data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
        return data
    
    def recognise_table(self, img):
        pass
