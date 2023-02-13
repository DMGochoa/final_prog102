import logging


class LoggerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            logging.basicConfig(filename='uiapp.log',
                                level=logging.WARNING,
                                format='%(asctime)s %(levelname)s: %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')
            cls._instance.logger = logging.getLogger()
        return cls._instance


logger = LoggerSingleton().logger
