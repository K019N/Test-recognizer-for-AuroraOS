from .table_data import *


class IRecogniser():
    def __init__(self):
        self.data = Table("")
    
    def recognise(self, img):
        pass
    
    def data_to_table(self, some_data: str):
        self.data = Table(some_data)

    def get_data(self):
        return self.data.data
    
