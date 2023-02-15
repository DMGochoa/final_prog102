class Data_carrier(object):
    __user_data = dict()
    __accounts = dict()
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Data_carrier, cls).__new__(cls)
        return cls.instance

    def get_general(self):
        return self.__user_data
    
    def set_general(self, new_data):
        self.__user_data = new_data
    
    def get_specific(self):
        return self.__accounts
    
    def set_specific(self, new_data):
        self.__accounts = new_data
        