import cv2 as cv
import numpy as np


class ImageProcessor():
    def draw_lines(self, lines, img, line_counter, data):
        if lines is not None:
                for r_theta in lines:
                    arr = np.array(r_theta[0], dtype=np.float64)
                    r, theta = arr

                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a*r
                    y0 = b*r
                    x1 = int(x0 + 1000*(-b))
                    y1 = int(y0 + 1000*(a))
                    x2 = int(x0 - 1000*(-b))
                    y2 = int(y0 - 1000*(a))
                    
                    data["line " + str(line_counter)] = [x1, x2, y1, y2]
                    line_counter += 1
                    cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
