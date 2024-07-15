from selenium.webdriver.common.by import By
import re
from bs4 import BeautifulSoup
from robot_code.utilities.base import Base
from robot_code.utilities.custom_exception import FailedCustomException
import inspect
import logging
logger = logging.getLogger()


class Get_News_Data(Base):
    """
    To get the news data from the already sorted information
    """
    file_name = inspect.currentframe().f_code.co_filename

    def __init__(self, pagination, accepted_time_params):
        """
        """
        self.accepted_time_params = accepted_time_params
        self.pagination = pagination

    def get_all_data(self):
        """
        For each pagination , get data from page
        """
        source = inspect.currentframe().f_code.co_name
        try:
            final_search_results = []
            if len(self.pagination) == 0:
                results = self.get_and_evaluate()
                final_search_results = final_search_results+results
                logger.info(
                    self.my_constanst.LOG_INFO_TEMPLATE.format(
                        message="Search results validated",
                        function_name=source,
                        file_name=self.get_file_name(self.file_name)
                    )
                )
                return final_search_results

            for p in self.pagination:
                results = self.get_and_evaluate()
                final_search_results = final_search_results+results
                # go to next page
                self.selenium.click_element_when_clickable(
                    locator=self.my_constanst.SELECTOR_PAGINATION_TEMPLATE.format(
                        count=p),
                    timeout=30000)

            logger.info(
                self.my_constanst.LOG_INFO_TEMPLATE.format(
                    message="Search results validated",
                    function_name=source,
                    file_name=self.get_file_name(self.file_name)
                )
            )

            return final_search_results

        except Exception as e:
            self.work_items.fail(exception_type="APPLICATION",
                                 code="STEP_3_GET_ALL_DATA_FAILED", message=e)
            fail_message = self.my_constanst.LOG_FAILED_TEMPLATE.format(
                message=e,
                function_name=source,
                file_name=self.get_file_name(self.file_name)
            )
            raise FailedCustomException(message=fail_message)

    def get_and_evaluate(self):
        """
        To make the code easier to read 
        """
        source = inspect.currentframe().f_code.co_name
        try:
            results = self.get_data_from_page()
            results, need_cleanup = self.eval_search_results(
                results=results,
                accepted_params=self.accepted_time_params)

            if need_cleanup == False:
                return results

            results = [x for x in results if x['accepted'] == True]
            return results

        except Exception as e:
            self.work_items.fail(exception_type="APPLICATION",
                                 code="STEP_3_GET_AND_EVALUATE_FAILED", message=e)
            fail_message = self.my_constanst.LOG_FAILED_TEMPLATE.format(
                message=e,
                function_name=source,
                file_name=self.get_file_name(self.file_name)
            )
            raise FailedCustomException(message=fail_message)

    def eval_search_results(self, results, accepted_params):
        """
        To evaluate the search results from each page
        """
        source = inspect.currentframe().f_code.co_name
        try:
            need_cleanup = False

            for res in results:
                date = res["date"]
                for el in accepted_params:
                    if el in date:
                        res["accepted"] = True
                        # if accepted we can download the image
                        self.http_actions.download(
                            res["image_source"],
                            self.my_constanst.PICTURES_PATH +
                            res["image_name"],
                            overwrite=True)
                        break
                if "accepted" not in res.keys():
                    res["accepted"] = False
                    need_cleanup = True

            logger.info(
                self.my_constanst.LOG_INFO_TEMPLATE.format(
                    message="Search Results evaluation executed Correctly",
                    function_name=source,
                    file_name=self.get_file_name(self.file_name)
                )
            )
            return results, need_cleanup

        except Exception as e:
            self.work_items.fail(exception_type="APPLICATION",
                                 code="RESULTS_EVALUATION_PROCESS_FAILED", message=e)
            fail_message = self.my_constanst.LOG_FAILED_TEMPLATE.format(
                message=e,
                function_name=source,
                file_name=self.get_file_name(self.file_name)
            )
            raise FailedCustomException(message=fail_message)

    def get_data_from_page(self):
        """To get the requested search results data from page/s"""
        source = inspect.currentframe().f_code.co_name
        try:
            # page = browser.page()

            # get main element containing all results
            self.selenium.wait_until_element_is_visible(
                locator=self.my_constanst.SELECTOR_ROOT_RESULTS_SECTION,
                timeout=30000)

            search_results = self.selenium.get_webelement(
                locator="id:___gcse_0")
            news_elements = search_results.find_elements(
                by=self.Selenium_By.CLASS_NAME, value="gsc-webResult.gsc-result")

            news_data = []

            for result in news_elements:
                res_data = result.text.split("\n")
                title = res_data[0]
                description = res_data[2]
                date = description.split("...")[0].strip()
                image_data = result.find_element(
                    by=By.TAG_NAME, value='img')
                image_source = image_data.get_attribute("src")
                image_name = image_source.split('/')[-1].split(":")[-1]+".png"
                search_word_counts = len([x for x in description.split() if str(
                    x.lower()) == self.work_items.payload["search_phrase"].lower()])

                news_data.append({
                    "title": title,
                    "description": description,
                    "date": date,
                    "image_name": image_name,
                    "image_source": image_source,
                    "search_word_counts": search_word_counts,
                    "contains_money_amount": self.check_contains_money_amount(text=description)
                })

            logger.info(
                self.my_constanst.LOG_INFO_TEMPLATE.format(
                    message="Data from page extracted correctly.",
                    function_name=source,
                    file_name=self.get_file_name(self.file_name)
                )
            )

            return news_data

        except Exception as e:
            self.work_items.fail(exception_type="APPLICATION",
                                 code="STEP_3_GET_DATA_FROM_PAGE_FAILED", message=e)
            fail_message = self.my_constanst.LOG_FAILED_TEMPLATE.format(
                message=e,
                function_name=source,
                file_name=self.get_file_name(self.file_name)
            )
            raise FailedCustomException(message=fail_message)

    @staticmethod
    def check_contains_money_amount(text):
        pattern = r'\$\d{1,3}(,\d{3})*(\.\d{1,2})?|(\d+ (dollars|USD))'
        return bool(re.search(pattern, text))
