from robocorp import browser
from robocorp import workitems
from datetime import datetime
from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
from RPA.Tables import Tables
from RPA.Archive import Archive
from robot_code.utilities import constants as CONSTANTS
from RPA.FileSystem import FileSystem
import time
from dateutil.relativedelta import relativedelta
import inspect
import logging
import glob

logger = logging.getLogger()


class Base:
    """
    To provide all the commoun utils for the robot
    """
    page = browser.page()
    work_items = workitems.inputs.current
    run_time_stamp = datetime.now()
    string_timestamp = run_time_stamp.strftime("%Y%m%d_%H%M%S")
    http_actions = HTTP()
    zip_archive_actions = Archive()
    my_constanst = CONSTANTS
    file_system_actions = FileSystem()
    file_name_base_class = inspect.currentframe().f_code.co_filename
    tables_actions = Tables()
    excel_actions = Files()

    @classmethod
    def archive_to_zip(cls):
        """
        To archive all data and clean output folder
        """
        try:
            archive_name = cls.my_constanst.FINAL_ZIP_FILE_TEMPLATE.format(
                time_stamp=cls.string_timestamp)

            cls.zip_archive_actions.archive_folder_with_zip(
                folder=cls.my_constanst.FINAL_REPORT_PATH,
                archive_name=archive_name
            )

            # all more folders
            pictures = glob.glob(pathname=cls.my_constanst.PICTURES_PATH+"*")
            logs = glob.glob(pathname=cls.my_constanst.LOGGING_PATH+"*")

            cls.zip_archive_actions.add_to_archive(
                files=pictures,
                archive_name=archive_name,
                folder="pictures"
            )
            cls.zip_archive_actions.add_to_archive(
                files=logs,
                archive_name=archive_name,
                folder="logs"
            )
            logger.info(f"Final ZIP file created correctly: {archive_name}")

        except Exception as e:
            source = inspect.currentframe().f_code.co_name
            cls.work_items.fail(exception_type="APPLICATION",
                                code="ERROR_IN_ARCHIVE_TO_ZIP_PROCESS", message=e)
            raise FailedCustomException(
                message=e, source=source, file_name=cls.file_name_base_class)

    @classmethod
    def clean_output_folder(cls):
        """
        To clean the output folder
        """
        try:
            for folder in [
                    cls.my_constanst.PICTURES_PATH,
                    cls.my_constanst.LOGGING_PATH,
                    cls.my_constanst.FINAL_REPORT_PATH]:

                cls.file_system_actions.remove_directory(
                    path=folder,
                    recursive=True
                )
        except Exception as e:
            source = inspect.currentframe().f_code.co_name
            cls.work_items.fail(exception_type="APPLICATION",
                                code="ERROR_IN_CLEANING_OUTPUT_FOLDER_PROCESS", message=e)
            raise FailedCustomException(
                message=e, source=source, file_name=cls.file_name_base_class)

    @staticmethod
    def wait_this(time_seconds):
        time.sleep(time_seconds)

    @classmethod
    def get_valid_time_parameters(cls):
        """
        get the months or valid date parameters accordng to the request
        """
        try:
            months_wi = cls.work_items.payload['months']
            now = cls.run_time_stamp
            current_date_to_use = datetime(now.year, now.month, 1)

            months_to_add = 0 if months_wi <= 1 else (months_wi-1)
            accepted_new_dates = []+[current_date_to_use]

            for m in range(months_to_add):
                accepted_new_dates.append(
                    current_date_to_use + relativedelta(months=0-m-1))

            # final_date = current_date_to_use + \
            #     relativedelta(months=months_to_add)

            default_accepted = ['ago']

            for d in accepted_new_dates:
                default_accepted.append(d.strftime("%b"))

            logger.info(f"Valid time parameters to use: {default_accepted}")
            return default_accepted

        except Exception as e:
            source = inspect.currentframe().f_code.co_name
            cls.work_items.fail(exception_type="APPLICATION",
                                code="ERROR_GETTING_VALID_TIME_PARAMETERS", message=e)
            raise FailedCustomException(
                message=e, source=source, file_name=cls.file_name_base_class)
