import unittest
from text_recogniser import *


class RocogniserTesting(unittest.TestCase):
    def test(self):
        recog = TextRecogniser()
        img = cv2.imread("1.png")
        recog.data_to_table(recog.recognise(img))
        print(recog.get_data())
        self.assertIsNotNone(recog.get_data())
'''
        self.recog.data_to_table("")
        img = cv2.imread("2.png")
        self.recog.data_to_table(self.recog.recognise(img))
        print(self.recog.get_data())
        self.assertIsNotNone(self.recog.get_data())
'''

if __name__ == "__main__":
    unittest.main()