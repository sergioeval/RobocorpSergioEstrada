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
    SELECTOR_SEARCH_RESULTS,
    SELECTOR_ROOT_RESULTS_SECTION,
    PICTURES_PATH
)
from Utilities import FailedCustomException, check_contains_money_amount
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pathlib import Path
import os
from RPA.Archive import Archive
import logging
import inspect
from bs4 import BeautifulSoup
from RPA.HTTP import HTTP
import re


logger = logging.getLogger()
browser.configure(slowmo=100)
http = HTTP()


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

        return self.final_search_results

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

            # need to sort by  date Selector fixed OK
            page.wait_for_selector(
                selector=SELECTOR_OPTIONS_SORT_BY,
                timeout=40000
            ).click()

            page.locator(selector=SELECTOR_OPTIONS_SORT_BY).locator(
                selector_or_locator=SELECTOR_OPTION_BY_DATE).click()

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
        page = browser.page()

        try:
            months = self.wi.payload['months']

            # Get the accepted params to validate dates in news
            accepted_parameters_for_dates = self._utility_get_months_parameters()
            # print(accepted_parameters_for_dates)

            # Check if page has pagination or not and return reult
            paginations = self._utility_get_maximun_paginations_in_page()

            # Get results from page
            self.final_search_results = []
            for p in paginations:
                results = self._utility_get_requested_search_results_data()
                results, need_cleanup = self._utility_eval_search_results(
                    results=results,
                    accepted_params=accepted_parameters_for_dates)
                # if need cleanup
                if need_cleanup == True:
                    results = [x for x in results if x['accepted'] == True]
                    self.final_search_results = self.final_search_results+results
                    break

                # no cleanup needed continue pagination
                self.final_search_results = self.final_search_results+results
                # go to next page
                page.locator(
                    selector=SELECTOR_PAGINATION_TEMPLATE.format(count=p)).click()

        except Exception as e:
            source = inspect.currentframe().f_code.co_name
            raise FailedCustomException(
                message=e, source=source, file_name=self.file_name)

    def _utility_eval_search_results(self, results, accepted_params):
        """
        To evaluate the search results from each page
        """
        need_cleanup = False

        for res in results:
            date = res["date"]
            for el in accepted_params:
                if el in date:
                    res["accepted"] = True
                    break
            if "accepted" not in res.keys():
                res["accepted"] = False
                need_cleanup = True
        return results, need_cleanup

    def _utility_get_requested_search_results_data(self):
        """To get the requested search results data from page/s"""
        page = browser.page()

        # get main element containing all results
        page.wait_for_selector(
            selector=SELECTOR_ROOT_RESULTS_SECTION, timeout=30000)
        search_results = page.locator(
            selector=SELECTOR_ROOT_RESULTS_SECTION).inner_html()

        soup = BeautifulSoup(search_results, "html.parser")
        only_news = soup.find_all(
            "div", attrs={"class": "gsc-webResult gsc-result"})
        news_data = []

        for result in only_news:
            title = result.find('a', attrs={'class': 'gs-title'}).text
            description = result.find(
                'div', attrs={"dir": "ltr", "class": "gs-bidi-start-align gs-snippet"}).text
            date = description.split("...")[0].strip()
            image_data = result.find("img")
            image_source = image_data.get("src")
            image_name = image_source.split('/')[-1].split(":")[-1]+".png"
            http.download(image_source, PICTURES_PATH +
                          image_name, overwrite=True)
            search_word_counts = len([x for x in description.split() if str(
                x.lower()) == self.wi.payload["search_phrase"].lower()])
            news_data.append({
                "title": title,
                "description": description,
                "date": date,
                "image_name": image_name,
                "search_word_counts": search_word_counts,
                "contains_money_amount": check_contains_money_amount(text=description)
            })
        return news_data

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

        default_accepted = ['ago']

        for d in accepted_new_dates:
            default_accepted.append(d.strftime("%b"))
        return default_accepted
