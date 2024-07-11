from robocorp import browser
from RPA.Browser.Selenium import Selenium
from constants import NEWS_URL, PICTURES_PATH, OUTPUT_BASE_PATH, LOGGING_PATH
import time
from playwright._impl._errors import TimeoutError
import logging
from datetime import datetime
from pathlib import Path
import os


# creating the necesary output paths if they don't exists
os.makedirs(LOGGING_PATH, exist_ok=True)
os.makedirs(PICTURES_PATH, exist_ok=True)

# Logging file configuration
now = datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")
log_file_name = f"{LOGGING_PATH}{timestamp}.log"
logging.basicConfig(filename=log_file_name, filemode='w',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - \
%(message)s')


class Browser_Get_News:
    """
    Object class to manipulate all interactions with the browser in my tasks 
    and save my data in excel
    """

    @staticmethod
    def _open_url():
        """
        To just open the news url
        """
        logging.info("Open url proces start")
        page = browser.page()
        page.set_default_timeout(timeout=30000)
        try:
            page.goto(url=NEWS_URL)
        except TimeoutError:
            logging.warning('Timeout error page reloaded')
            page.reload(timeout=60000)

    def _search_one_work_item(self):
        """
        To search data for one of the work items 
        """
