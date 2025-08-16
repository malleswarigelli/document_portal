import sys
import traceback
from logger.custom_logger import CustomLogger
logger=CustomLogger().get_logger(__file__)

class DocumentPortalException(Exception):
    """Base class for Document Portal exceptions."""
    def __init__(self, error_messagge:str, error_details:sys):
        _,_,exc_tb=error_details.exc_info()
        self.file_name=exc_tb.tb_frame.f_code.co_filename  
        self.lineno=exc_tb.tb_lineno # Get the line number where the exception occurred
        self.error_message=str(error_messagge)
        self.traceback_str = ''.join(traceback.format_exception(*error_details.exc_info()))  

    def __str__(self):
        return f"""
        Error occurred in [{self.file_name}] at line [{self.lineno}]
        Message: {self.error_message}
        Traceback: {self.traceback_str}
        """

if __name__ == "__main__":
    try:
        # Simulating an error for demonstration purposes
        a=1/0  # This will raise a ZeroDivisionError
        print(a)
    except Exception as e:
        app_exc= DocumentPortalException(e, sys)        
        logger.error(app_exc)
        raise app_exc
        