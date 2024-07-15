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
        source = inspect.currentframe().f_code.co_name
        try:
            # need to sort by  date Selector fixed OK
            self.page.wait_for_selector(
                selector=self.my_constanst.SELECTOR_OPTIONS_SORT_BY,
                timeout=40000
            ).click()

            # click on Date to sort the data
            self.page.locator(selector=self.my_constanst.SELECTOR_OPTIONS_SORT_BY).locator(
                selector_or_locator=self.my_constanst.SELECTOR_OPTION_BY_DATE).click()

            self.wait_this(time_seconds=2)

            logger.info(
                self.my_constanst.LOG_INFO_TEMPLATE.format(
                    message="Search result is sorted by date now.",
                    function_name=source,
                    file_name=self.get_file_name(self.file_name)
                )
            )

        except Exception as e:
            self.work_items.fail(exception_type="APPLICATION",
                                 code="SORT_DATA_FAILED", message=e)
            fail_message = self.my_constanst.LOG_FAILED_TEMPLATE.format(
                message=e,
                function_name=source,
                file_name=self.get_file_name(self.file_name)
            )
            raise FailedCustomException(message=fail_message)

    def get_pagination(self):
        """
        Get the available pagination in current search
        """
        source = inspect.currentframe().f_code.co_name
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

            logger.info(
                self.my_constanst.LOG_INFO_TEMPLATE.format(
                    message=f"Pagination Limits created correctly: {pages}",
                    function_name=source,
                    file_name=self.get_file_name(self.file_name)
                )
            )
            return pages
        except Exception as e:
            self.work_items.fail(exception_type="APPLICATION",
                                 code="GET_PAGINATION_FAILED", message=e)
            fail_message = self.my_constanst.LOG_FAILED_TEMPLATE.format(
                message=e,
                function_name=source,
                file_name=self.get_file_name(self.file_name)
            )
            raise FailedCustomException(message=fail_message)
