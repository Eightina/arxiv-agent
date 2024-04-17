import warnings
import logging
from datetime import datetime
from abc import ABC, abstractmethod


class Logger(ABC):
    """
    Abstract base class for logger.
    """
    
    def __init__(self, logFile:str):
        """
        Initialize the logger.

        Parameters:
        logFile (str): Path to the log file.

        Raises:
        ValueError: If the file path is empty.
        """
        
        if not logFile:
            raise ValueError("empty file path")
        logging.basicConfig(filename=logFile, level=logging.INFO)


    @staticmethod
    def newLogFile() -> str:
        """
        Create a new log file.

        Returns:
        str: Path of the newly created log file.
        """
        
        currentDate = datetime.now().strftime("%Y-%m-%d")
        logFile = f"./log/crawler_{currentDate}.log"
        # set log file
        with open(logFile, "w") as temp:
            pass
        return logFile


    @abstractmethod
    def log(self, content:str):
        """
        Log the content.

        Parameters:
        content (str): The content to be logged.
        """
        pass



class WarnLogger(Logger):
    """
    Logger class for warning messages, inherits from Logger abstract base class.
    """

    def __init__(self, logFile:str):
        """
        Initialize the warning logger.

        Parameters:
        logFile (str): Path to the log file.
        """
        
        super().__init__(logFile)
    
    
    def log(self, content:str):
        """
        Log warning messages.

        Parameters:
        content (str): The content of the warning message.
        """
        
        warnings.warn(content)
        logging.warning(content)
        
        
        
class InfoLogger(Logger):
    """
    Logger class for information messages, inherits from Logger abstract base class.
    """
    
    def __init__(self, logFile:str):
        """
        Initialize the information logger.

        Parameters:
        logFile (str): Path to the log file.
        """
        
        super().__init__(logFile)
    
    
    def log(self, content:str):
        """
        Log information messages.

        Parameters:
        content (str): The content of the information message.
        """
        
        logging.info(content)
