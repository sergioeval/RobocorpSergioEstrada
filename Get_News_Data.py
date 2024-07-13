from robocorp import browser
from RPA.Browser.Selenium import Selenium, expected_conditions
from constants import (
    NEWS_URL,
    SELECTOR_HAMBURGER_MENU,
    SELECTOR_SEARCH_FIELD,
    SELECTOR_SORT_BY_TEXT,
    SELECTOR_OPTIONS_SORT_BY,
    SELECTOR_OPTION_BY_DATE,
    SELECTOR_PAGINATION_SECTION,
    SELECTOR_PAGINATION_TEMPLATE,
    SELECTOR_SEARCH_RESULTS
)
from Utilities import FailedCustomException
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pathlib import Path
import os
from RPA.Archive import Archive
import logging
import inspect
from bs4 import BeautifulSoup

logger = logging.getLogger()


class Get_News_Data:
    """
    Object class to manipulate all interactions with the browser in my tasks
    and save my data in excel
    """

    def __init__(self, wi):
        self.wi = wi
        self.file_name = inspect.currentframe().f_code.co_filename
        self.current_date = datetime.now().strftime("%b %d, %Y")
        self.current_month = datetime.now().strftime("%b")
        self.current_year = datetime.now().strftime("%Y")

    def run_all(self):
        """
        To run all the necesary steps to get the news data
        """
        self.step_1_open_url()
        self.step_2_look_for_phrase_and_sort_by_date()
        self.step_3_get_news_data()

    def step_1_open_url(self):
        """
        To just open the news url
        """
        logger.info("Open url proces start")

        try:
            for _ in range(5):
                try:
                    browser.goto(url=NEWS_URL)
                    break
                except Exception as e:
                    logger.error(
                        f"Initial connection to websited failed with error: {e}")

        except Exception as e:
            source = inspect.currentframe().f_code.co_name
            raise FailedCustomException(
                message=e, source=source, file_name=self.file_name)

    def step_2_look_for_phrase_and_sort_by_date(self):
        """
        Search for the phrase and sort the data
        """
        logger.info(
            f'Searching phrase and sort data: {self.wi.payload["search_phrase"]}')

        try:
            page = browser.page()
            # search for the phrase

            search_phrase = self.wi.payload["search_phrase"]
            print(search_phrase)

            # Need to click on the hamburger menu
            page.wait_for_selector(
                selector=SELECTOR_HAMBURGER_MENU,
                timeout=40000).click()

            # clicking in the search bar and enter searchphrase
            page.wait_for_selector(
                selector=SELECTOR_SEARCH_FIELD,
                timeout=40000
            ).fill(value=search_phrase)

            page.keyboard.press('Enter')

            # need to sort by  date
            page.wait_for_selector(
                selector=SELECTOR_OPTIONS_SORT_BY,
                timeout=40000
            ).click()

            page.wait_for_selector(
                selector=SELECTOR_OPTION_BY_DATE,
                timeout=40000
            ).click()

        except Exception as e:
            source = inspect.currentframe().f_code.co_name
            raise FailedCustomException(
                message=e, source=source, file_name=self.file_name)
        time.sleep(3)

    def step_3_get_news_data(self):
        """
        To get the news data already sorted
        # number of months to get
        # 0 and 1 = current month
        # 2 = current and previous month
        # 3 = current and 2 previous months
        # etc
        """
        logger.info("Getting the news data already sorted")

        try:
            months = self.wi.payload['months']

            # Get the accepted params to validate dates in news
            accepted_parameters_for_dates = self._utility_get_months_parameters()
            print(accepted_parameters_for_dates)

            # Check if page has pagination or not and return reult
            paginations = self._utility_get_maximun_paginations_in_page()

            # Get results to create work items
            results = self._utility_get_requested_search_results_data()

        except Exception as e:
            source = inspect.currentframe().f_code.co_name
            raise FailedCustomException(
                message=e, source=source, file_name=self.file_name)

    def _utility_get_requested_search_results_data(self):
        """To get the requested search results data from page/s"""
        page = browser.page()
        search_results = page.query_selector_all(
            selector=SELECTOR_SEARCH_RESULTS)
        print(search_results)
        for sr in search_results:
            # print(sr.text_content())
            soup = BeautifulSoup(sr.inner_html(), "html.parser")
            title = soup.find('a', attrs={'class': 'gs-title'}).text
            description = soup.find(
                'div', attrs={"class": "gs-bidi-start-align gs-snippet"}).text

            print(description)
            print('')

            break

    def _utility_get_maximun_paginations_in_page(self):
        """
        To get the maximmun pagination in the search result page
        """
        # we are limited to 10 pages result in nbcnews get max paginations
        # But we have to make sure we get only the pagination pages
        page = browser.page()
        pages = []
        count = 2

        # Check if pagination is visible , some results will not have it
        page.wait_for_load_state()
        if not page.is_visible(selector=SELECTOR_PAGINATION_SECTION):
            logger.info("No pagination in search result")
            return []

        while page.is_visible(
                selector=SELECTOR_PAGINATION_TEMPLATE.format(count=count)):
            pages.append(count)
            count += 1
        return pages

    def _utility_get_months_parameters(self):
        """
        get the months or valid date parameters accordng to the request
        """
        months_wi = self.wi.payload['months']
        now = datetime.now()
        current_date_to_use = datetime(now.year, now.month, 1)

        months_to_add = 0 if months_wi <= 1 else (months_wi-1)
        accepted_new_dates = []+[current_date_to_use]
        for m in range(months_to_add):
            accepted_new_dates.append(
                current_date_to_use + relativedelta(months=m+1))

        final_date = current_date_to_use + relativedelta(months=months_to_add)

        default_accepted = set(
            ['days ago', 'hours ago', 'minutes ago', 'seconds ago'])

        for d in accepted_new_dates:
            default_accepted.add((
                d.strftime("%b"),
                d.strftime("%Y")
            ))
        return default_accepted
