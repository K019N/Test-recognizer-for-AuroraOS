import unittest
from .text_recogniser import *


class RocogniserTesting(unittest.TestCase):
    def test(self):
        recog = TextRecogniser()
        counter = ["1.png", "2.png", "3.png", "4.jpg"]
        
        for i in counter:
            recog.data_to_table("")
            img = cv2.imread(i)
            recog.data_to_table(recog.recognise(img))
            print(recog.get_data())
            self.assertIsNotNone(recog.data)

if __name__ == "__main__":
    unittest.main()
