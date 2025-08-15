import logging
import os
from datetime import datetime


class CustomLogger:
    def __init__(self):
        # create logs directory if it doesn't exist
        self.logs_dir = os.path.join(os.getcwd(),'logs')
        os.makedirs(self.logs_dir, exist_ok=True)

        # create log file with timestamp
        log_file = f"{datetime.now().strftime('%m-%m-%Y_%H-%M-%S')}.log"
        log_file_path = os.path.join(self.logs_dir, log_file)

        # configure logging
        logging.basicConfig(
            filename=log_file_path,
            level=logging.INFO,
            format="[ %(asctime)s ] %(levelname)s %(name)s (line:%(lineno)d) - %(message)s"
        )
        
    def get_logger(self, name=__file__):
        return logging.getLogger(os.path.basename(name))
    
    
if __name__ == "__main__":
    logger = CustomLogger().get_logger()
    logger.info("Malli's Custom Logger Initialized")
        