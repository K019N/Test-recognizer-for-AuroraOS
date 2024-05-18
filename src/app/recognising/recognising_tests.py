import unittest
from text_recogniser import *
from table_recog import *


class RocogniserTesting(unittest.TestCase):
    def test(self):
        recog = TableRecogniser()
        counter = ["122.png"]
        
        for i in counter:
            #recog.data_to_table("")
            #img = cv2.imread(i)
            recog.table_recog(i)

if __name__ == "__main__":
    unittest.main()
