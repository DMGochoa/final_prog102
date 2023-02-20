import logging
import os


class log_web:
    def __init__(self) -> None:
        self.__config()

    def __config(self):
        current_path = os.path.join(os.path.dirname(__file__), '..')
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
            filename=os.path.join(current_path, 'log', 'basic.log')
        )
        
    def debug(self, msg):
        logging.debug(msg)
  
    
if __name__ == "__main__":
    logger = log_web()
    d = 5
    logger.debug(f'Estoy Funcionando {d}')