from RPA.FileSystem import FileSystem
from constants import (
    LOGGING_PATH,
    PICTURES_PATH,
    OUTPUT_BASE_PATH)
from Utilities import FailedCustomException
import logging
from datetime import datetime
import inspect

logger = logging.getLogger()


class Initiate_Structure:
    """
    To initiate the necesary folder structure for the robot
    """

    def __init__(self):
        self.file_name = inspect.currentframe().f_code.co_filename

    def setup_folders(self):
        logger.info("Set up folder started")
        try:
            fs = FileSystem()
            # create
            fs.create_directory(path=LOGGING_PATH, exist_ok=True)
            fs.create_directory(path=PICTURES_PATH, exist_ok=True)

        except Exception as e:
            source = inspect.currentframe().f_code.co_name
            raise FailedCustomException(
                message=e, source=source, file_name=self.file_name)
