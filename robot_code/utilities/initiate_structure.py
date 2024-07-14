from robot_code.utilities.base import Base
import logging
import inspect
from robot_code.utilities.custom_exception import FailedCustomException
logger = logging.getLogger()


class Initiate_Structure(Base):
    """
    To initiate the necesary folder structure for the robot
    """

    def __init__(self):
        self.file_name = inspect.currentframe().f_code.co_filename

    def setup_folders(self):
        logger.info("Set up folder started")
        try:
            # fs = FileSystem()
            # create
            self.file_system_actions.create_directory(
                path=self.my_constanst.LOGGING_PATH,
                exist_ok=True
            )
            # fs.create_directory(path=LOGGING_PATH, exist_ok=True)
            self.file_system_actions.create_directory(
                path=self.my_constanst.PICTURES_PATH,
                exist_ok=True
            )

            # Create folder for excel report
            self.file_system_actions.create_directory(
                path=self.my_constanst.FINAL_REPORT_PATH,
                exist_ok=True
            )

        except Exception as e:
            source = inspect.currentframe().f_code.co_name
            self.work_items.fail(exception_type="APPLICATION",
                                 code="FOLDER_SETUP_FAILED", message=e)
            raise FailedCustomException(
                message=e, source=source, file_name=self.file_name)
