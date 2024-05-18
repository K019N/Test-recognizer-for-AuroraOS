import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import pandas as pd
from PIL import Image
#jinja2


class TableRecogniser:
    def has_non_white_color(self, image) -> str:
        if image is None:
            print("Ошибка: Изображение не может быть None")
            return ""

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        non_white_mask = np.any(rgb_image != [255, 255, 255], axis=-1)
        if np.any(non_white_mask): return "+"

    def recognise(self, path):
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        _ ,img_bin = cv2.threshold(img,128,255,cv2.THRESH_BINARY)
        img_bin = 255 - img_bin

        img_bin2 = 255 - img.astype("uint8")
        _ ,img_bin_otsu = cv2.threshold(img_bin2,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        #vertical lines
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, np.array(img).shape[1]//100))
        eroded_image = cv2.erode(img_bin_otsu, vertical_kernel, iterations=3)
        vertical_lines = cv2.dilate(eroded_image, vertical_kernel, iterations=3)

        #horizont lines
        hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (np.array(img).shape[1]//100, 1))
        horizontal_lines = cv2.erode(img_bin, hor_kernel, iterations=5)
        horizontal_lines = cv2.dilate(horizontal_lines, hor_kernel, iterations=5)

        #all lines together
        vertical_horizontal_lines = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
        vertical_horizontal_lines = cv2.erode(~vertical_horizontal_lines, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)), iterations=3)
        _, vertical_horizontal_lines = cv2.threshold(vertical_horizontal_lines,128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        bitxor = cv2.bitwise_xor(img,vertical_horizontal_lines)
        bitnot = cv2.bitwise_not(bitxor)

        #pytesseract recog
        contours, _ = cv2.findContours(vertical_horizontal_lines, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        boundingBoxes = [cv2.boundingRect(contour) for contour in contours]
        (contours, boundingBoxes) = zip(*sorted(zip(contours, boundingBoxes),key=lambda x:x[1][1]))

        boxes = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if (w < 1000 and h < 500):
                image = cv2.rectangle(img, (x, y), (x + w,y + h), (0,255,0), 2)
                boxes.append([x,y,w,h])

        #get coords of all cells and height and width
        rows = []
        columns = []
        heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]
        mean = np.mean(heights)
        print(mean)
        columns.append(boxes[0])
        previous = boxes[0]
        for i in range(1,len(boxes)):
            if(boxes[i][1] <= previous[1] + mean / 2):
                columns.append(boxes[i])
                previous = boxes[i]
                if(i == len(boxes)-1):
                    rows.append(columns)
            else:
                rows.append(columns)
                COLUMNS = len(columns)
                columns = []
                previous = boxes[i]
                columns.append(boxes[i])
        ROWS = len(rows)

        def get_cols():
            total_cells = 0
            for row in rows:
                for i in range(len(row)):
                    if len(row[i]) > total_cells:
                        total_cells += len(row[i])
            #print(total_cells)
            return total_cells + 1

        def get_rows():
            #print(len(rows))
            return len(rows)
        get_rows()

        def get_center(rows):
            for row in rows:
                for i in range(0, len(row)):
                    if i < len(rows): center = [int(rows[i][j][0] + rows[i][j][2]/2) for j in range(len(rows[i])) if rows[i]]
            #print("Center -- ", center)
            return center

        boxes_list = []
        center = np.array(get_center(rows))
        for i in range(len(rows)):
            l = []

            for j in range(len(rows[i])):
                diff = abs(center - (rows[i][j][0] + rows[i][j][2] / 4))
                minimum = min(diff)
                indexing = list(diff)
                l.append(rows[i][j])
            boxes_list.append(l)
            for box in boxes_list:
                pass
                #print(box)
        #print("\n\n\n\n", len(boxes_list), len(boxes_list[0]), "\n\n\n\n")
        pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\\tesseract.exe"
        dataframe_final = []
        
        
        for i in range(len(boxes_list)):
            for j in range(get_cols()):
                s = ''
                try:
                    y, x, w, h = boxes_list[i][j][0], boxes_list[i][j][1], boxes_list[i][j][2], boxes_list[i][j][3]
                    roi = bitnot[x-5:x+h-5, y-5:y+w-5]
                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
                    border = cv2.copyMakeBorder(roi, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=[255, 255])
                    cv2.imshow('Border', border)
                    resizing = cv2.resize(border, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                    dilation = cv2.dilate(resizing, kernel,iterations=1)
                    erosion = cv2.erode(dilation, kernel,iterations=2)
                    
                    s = self.has_non_white_color(erosion)
                except: s = ""
                dataframe_final.append(s)
        print(dataframe_final)
        
        arr = np.array(dataframe_final)
        try: 
            dataframe = pd.DataFrame(arr.reshape(get_rows(), get_cols()))
            #data = dataframe.style.set_properties(align="left")
            #print(data)
            #print(dataframe)
            #d = []
            for i in range(0, get_cols()):
                for j in range(0, get_rows()):
                    print(dataframe[i][j], end=" ")
                print()
            print(dataframe)
            return dataframe
        except: return None


#opn file
file2 = "src/app/recognising/123.jpg"
file1 = "src/app/recognising/122.png"
#TableRecogniser().recognise(file2)