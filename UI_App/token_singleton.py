class TokenManager:
    __instance = None
    __token = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__token = None
        return cls.__instance

    def get_token(self):
        return self.__token

    def set_token(self, token):
        self.__token = token


token = TokenManager()
