from robocorp import browser
from RPA.Browser.Selenium import Selenium, expected_conditions
from constants import (
    NEWS_URL,
    FailedCustomException
)
import time
from datetime import datetime
from pathlib import Path
import os
from RPA.Archive import Archive
import logging
import inspect


logger = logging.getLogger()


class Get_News_Data:
    """
    Object class to manipulate all interactions with the browser in my tasks 
    and save my data in excel
    """

    def __init__(self, wi):
        self.wi = wi
        self.file_name = inspect.currentframe().f_code.co_filename
        self.driver = Selenium()

    def run_all(self):
        """
        To run all the necesary steps to get the news data 
        """
        self._open_url()
        self._process_work_item()

    def _open_url(self):
        """
        To just open the news url
        """
        logger.info("Open url proces start")

        self.driver.open_available_browser()
        # self.driver.open_chrome_browser('www.google.com')
        # buscar = self.driver.get_webelement(locator="id:APjFqb")
        # buscar.click()
        # buscar.send_keys('Hola')

        try:

            # original time out 300 seconds
            self.driver.set_selenium_page_load_timeout(value=10)
            print('Opening the browser')
            try:
                self.driver.go_to(url=NEWS_URL)
            except Exception as e:
                logger.warning(f"Time out initial loading: {e}")
                print("Page loading timeout")

            # Reseting timeout to original
            self.driver.set_selenium_page_load_timeout(value=300)
        except Exception as e:
            source = inspect.currentframe().f_code.co_name
            raise FailedCustomException(
                message=e, source=source, file_name=self.file_name)

    def _process_work_item(self):
        """
        To search data for one of the work items 
        """
        logger.info(f'Working on item: {self.wi}')

        try:
            # search for the phrase

            search_phrase = self.wi.payload["search_phrase"]
            print(search_phrase)

            # Need to click on the hamburger menu
            self.driver.click_element(
                locator="css:.hamburger.js-menu-toggle >> xpath://button")
            # hamburger = self.driver.get_webelements(
            #     locator="class:hamburger")
            print('hi')
            print('otro print')

            for el in hamburger:
                attribute = el.get_attribute(name="class")
                if "hamburger" in attribute:
                    print('found attribute class')
                    self.driver.click_element(el)
                    break

            #     condition=expected_conditions.visibility_of_element_located(locator="class:hamburger"))
            # print(hamburger)

            # driver.click_element(
            #     locator="//button[@class='SearchOverlay-search-button']")
            time.sleep(10)
        except Exception as e:
            source = inspect.currentframe().f_code.co_name
            raise FailedCustomException(
                message=e, source=source, file_name=self.file_name)
        time.sleep(3)

    @staticmethod
    def archive_all():
        arc = Archive()
        arc.archive_folder_with_zip(
            folder=LOGGING_PATH, archive_name=OUTPUT_BASE_PATH+"logs.zip")
