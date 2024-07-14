from robot_code.utilities.base import Base
from robot_code.utilities.custom_exception import FailedCustomException
import inspect
import logging
logger = logging.getLogger()


class Sort_Get_Pagination(Base):
    """
    To sort the data and get paginations
    """
    file_name = inspect.currentframe().f_code.co_filename

    def run(self):
        """Run all process"""
        self.sort_search_result()
        return self.get_pagination()

    def sort_search_result(self):
        """
        Sort the search results
        """
        try:
            # need to sort by  date Selector fixed OK
            self.page.wait_for_selector(
                selector=self.my_constanst.SELECTOR_OPTIONS_SORT_BY,
                timeout=40000
            ).click()

            # click on Date to sort the data
            self.page.locator(selector=self.my_constanst.SELECTOR_OPTIONS_SORT_BY).locator(
                selector_or_locator=self.my_constanst.SELECTOR_OPTION_BY_DATE).click()

            logger.info(f"Search result is sorted by date now")

            self.wait_this(time_seconds=2)
        except Exception as e:
            source = inspect.currentframe().f_code.co_name
            self.work_items.fail(exception_type="APPLICATION",
                                 code="SORT_DATA_FAILED", message=e)
            raise FailedCustomException(
                message=e, source=source, file_name=self.file_name)

    def get_pagination(self):
        """
        Get the available pagination in current search
        """
        try:
            # need to sort by  date Selector fixed OK
            # But we have to make sure we get only the pagination pages
            pages = []
            count = 2

            # Check if pagination is visible , some results will not have it
            self.page.wait_for_load_state()
            if not self.page.is_visible(selector=self.my_constanst.SELECTOR_PAGINATION_SECTION):
                logger.info("No pagination in search result")
                return []

            while self.page.is_visible(
                    selector=self.my_constanst.SELECTOR_PAGINATION_TEMPLATE.format(count=count)):
                pages.append(count)
                count += 1
            return pages

            self.wait_this(time_seconds=2)
        except Exception as e:
            source = inspect.currentframe().f_code.co_name
            self.work_items.fail(exception_type="APPLICATION",
                                 code="GET_PAGINATION_FAILED", message=e)
            raise FailedCustomException(
                message=e, source=source, file_name=self.file_name)
