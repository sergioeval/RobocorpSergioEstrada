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
        try:
            final_search_results = []
            for p in self.pagination:
                results = self.get_data_from_page()
                results, need_cleanup = self.eval_search_results(
                    results=results,
                    accepted_params=self.accepted_time_params)
                # if need cleanup
                if need_cleanup == True:
                    results = [x for x in results if x['accepted'] == True]
                    final_search_results = final_search_results+results
                    break

                # no cleanup needed continue pagination
                final_search_results = final_search_results+results
                # go to next page
                self.page.locator(
                    selector=self.my_constanst.SELECTOR_PAGINATION_TEMPLATE.format(count=p)).click()

            logger.info("Search results validated")

            return final_search_results
        except Exception as e:
            source = inspect.currentframe().f_code.co_name
            self.work_items.fail(exception_type="APPLICATION",
                                 code="STEP_3_GET_ALL_DATA_FAILED", message=e)
            raise FailedCustomException(
                message=e, source=source, file_name=self.file_name)

    @staticmethod
    def eval_search_results(results, accepted_params):
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

    def get_data_from_page(self):
        """To get the requested search results data from page/s"""
        try:
            # page = browser.page()

            # get main element containing all results
            self.page.wait_for_selector(
                selector=self.my_constanst.SELECTOR_ROOT_RESULTS_SECTION,
                timeout=30000)

            search_results = self.page.locator(
                selector=self.my_constanst.SELECTOR_ROOT_RESULTS_SECTION).inner_html()

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
                self.http_actions.download(image_source, self.my_constanst.PICTURES_PATH +
                                           image_name, overwrite=True)
                search_word_counts = len([x for x in description.split() if str(
                    x.lower()) == self.work_items.payload["search_phrase"].lower()])

                news_data.append({
                    "title": title,
                    "description": description,
                    "date": date,
                    "image_name": image_name,
                    "search_word_counts": search_word_counts,
                    "contains_money_amount": self.check_contains_money_amount(text=description)
                })
            logger.info("Data from page extracted correctly.")

            return news_data
        except Exception as e:
            source = inspect.currentframe().f_code.co_name
            self.work_items.fail(exception_type="APPLICATION",
                                 code="STEP_3_GET_DATA_FROM_PAGE_FAILED", message=e)
            raise FailedCustomException(
                message=e, source=source, file_name=self.file_name)

    @staticmethod
    def check_contains_money_amount(text):
        pattern = r'\$\d{1,3}(,\d{3})*(\.\d{1,2})?|(\d+ (dollars|USD))'
        return bool(re.search(pattern, text))
