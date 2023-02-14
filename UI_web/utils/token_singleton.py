import json

# This singleton is to save the information of the token
class Token(object):
    __token = ''
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Token, cls).__new__(cls)
        return cls.instance

    def get_token(self):
        return self.__token
    
    def set_token(self, new_token):
        self.__token = json.loads(new_token)['access_token']
    
    def del_token(self):
        self.__token = ''
