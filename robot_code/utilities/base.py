# from robocorp import browser
# from robocorp import workitems
from datetime import datetime
from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
from RPA.Tables import Tables
from RPA.Archive import Archive
from RPA.Browser.Selenium import Selenium
from robot_code.utilities import constants as CONSTANTS
from RPA.FileSystem import FileSystem
import time
from dateutil.relativedelta import relativedelta
import inspect
import logging
import glob
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from robot_code.utilities.custom_exception import FailedCustomException


chrome_options = Options()
# Speed optimization options
# chrome_options.add_argument('--headless')
chrome_options.page_load_strategy = "eager"
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--blink-settings=imagesEnabled=false')
chrome_options.add_argument('--disable-extensions')
# chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-software-rasterizer')
chrome_options.add_argument('--start-maximized')
# chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--enable-fast-unload')


logger = logging.getLogger()


class Base:
    """
    To provide all the commoun utils for the robot
    """
    # page = browser.page()
    # work_items = workitems.inputs.current
    run_time_stamp = datetime.now()
    string_timestamp = run_time_stamp.strftime("%Y%m%d_%H%M%S")
    http_actions = HTTP()
    zip_archive_actions = Archive()
    my_constanst = CONSTANTS
    selenium = Selenium()
    file_system_actions = FileSystem()
    file_name_base_class = inspect.currentframe().f_code.co_filename
    tables_actions = Tables()
    excel_actions = Files()
    chrome_options = chrome_options
    Selenium_By = By
    Selenium_Keys = Keys
    Selenium_Ec = ec

    @classmethod
    def archive_to_zip(cls):
        """
        To archive all data and clean output folder
        """
        source = inspect.currentframe().f_code.co_name
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

            logger.info(
                cls.my_constanst.LOG_INFO_TEMPLATE.format(
                    message=f"FINAL ZIP FILE CREATED: {archive_name}",
                    function_name=source,
                    file_name=cls.get_file_name(cls.file_name_base_class)
                )
            )

        except Exception as e:
            fail_message = cls.my_constanst.LOG_FAILED_TEMPLATE.format(
                message=e,
                function_name=source,
                file_name=cls.get_file_name(cls.file_name_base_class)
            )
            raise FailedCustomException(message=fail_message)

    @classmethod
    def clean_output_folder(cls):
        """
        To clean the output folder
        """
        source = inspect.currentframe().f_code.co_name
        try:
            for folder in [
                    cls.my_constanst.PICTURES_PATH,
                    cls.my_constanst.LOGGING_PATH,
                    cls.my_constanst.FINAL_REPORT_PATH]:

                cls.file_system_actions.remove_directory(
                    path=folder,
                    recursive=True
                )

            logger.info(
                cls.my_constanst.LOG_INFO_TEMPLATE.format(
                    message="CLEANUP PROCESS EXECUTED",
                    function_name=source,
                    file_name=cls.get_file_name(cls.file_name_base_class)
                )
            )

        except Exception as e:
            fail_message = self.my_constanst.LOG_FAILED_TEMPLATE.format(
                message=e,
                function_name=source,
                file_name=cls.get_file_name(cls.file_name_base_class)
            )
            raise FailedCustomException(message=fail_message)

    def get_valid_time_parameters(self, item):
        """
        get the months or valid date parameters accordng to the request
        """
        source = inspect.currentframe().f_code.co_name
        try:
            months_wi = item.payload["months"]
            now = self.run_time_stamp
            current_date_to_use = datetime(now.year, now.month, 1)

            months_to_add = 0 if months_wi <= 1 else (months_wi-1)
            accepted_new_dates = []+[current_date_to_use]

            for m in range(months_to_add):
                accepted_new_dates.append(
                    current_date_to_use + relativedelta(months=0-m-1))

            default_accepted = ['ago']

            for d in accepted_new_dates:
                default_accepted.append(d.strftime("%b"))

            logger.info(
                self.my_constanst.LOG_INFO_TEMPLATE.format(
                    message=f"VALID TIME PARAMETERS TO USE: {default_accepted}",
                    function_name=source,
                    file_name=self.get_file_name(
                        self.file_name_base_class)
                )
            )
            return default_accepted

        except Exception as e:
            fail_message = self.my_constanst.LOG_FAILED_TEMPLATE.format(
                message=e,
                function_name=source,
                file_name=self.get_file_name(self.file_name_base_class)
            )
            raise FailedCustomException(message=fail_message)

    @staticmethod
    def wait_this(time_seconds):
        time.sleep(time_seconds)

    @staticmethod
    def get_file_name(text):
        return text.split("robot_code")[-1]
