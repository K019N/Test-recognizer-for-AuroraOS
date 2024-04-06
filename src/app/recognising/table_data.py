class Table():
    def __init__(self, some_data: str):
        self.data = self.str_to_table(some_data)
    
    def str_to_table(self, some_data: str):
        data = {}
        key = ''
        value = ''
        was_dash = False
        for i in range(len(some_data)):
            print(was_dash, some_data[i])
            if some_data[i] == '-':
                was_dash = True
            elif some_data[i] == '\n':
                data[int(key.replace(" ", ""))] = value.replace(" ", "")
                key = ''
                value = ''
                was_dash = False
            elif was_dash: value += some_data[i] 
            else: key += some_data[i]
        data[int(key.replace(" ", ""))] = value.replace(" ", "")
        return data
    
    def get_value(self, key: int):
        return self.data[key]
    
    def get_length(self):
        return len(self.data)
    
    def data_to_null(self):
        self.data = {}
