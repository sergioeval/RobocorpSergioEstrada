
from robot_code.utilities.base import Base
from robot_code.utilities.custom_exception import FailedCustomException
import inspect
import logging
logger = logging.getLogger()


class Go_Search_Phrase(Base):
    """
    Go to url and search phrase from work item
    """
    file_name = inspect.currentframe().f_code.co_filename

    def run(self):
        """
        run the whole process
        """
        self.go_to_page()
        self.search_phrase()

    def go_to_page(self):
        source = inspect.currentframe().f_code.co_name
        try:

            self.selenium.open_available_browser(options=self.chrome_options)

            for _ in range(3):
                try:
                    self.selenium.go_to(url=self.my_constanst.NEWS_URL)
                except:
                    self.selenium.reload_page()

            logger.info(
                self.my_constanst.LOG_INFO_TEMPLATE.format(
                    message="Go to page executed ok",
                    function_name=source,
                    file_name=self.get_file_name(self.file_name)
                )
            )

        except Exception as e:
            # source = inspect.currentframe().f_code.co_name
            self.work_items.fail(exception_type="APPLICATION",
                                 code="GOTO_PAGE_FAILED", message=e)

            fail_message = self.my_constanst.LOG_FAILED_TEMPLATE.format(
                message=e,
                function_name=source,
                file_name=self.get_file_name(self.file_name)
            )
            raise FailedCustomException(message=fail_message)

    def search_phrase(self):
        """
        to search the phrase from the work item
        """
        source = inspect.currentframe().f_code.co_name
        try:
            search_phrase = self.work_items.payload['search_phrase']

            # Need to click on the hamburger menu
            self.selenium.click_element_when_clickable(
                locator=self.my_constanst.SELECTOR_HAMBURGER_MENU,
                timeout=40000)

            # wait for search field is visible
            self.selenium.wait_until_element_is_visible(
                locator=self.my_constanst.SELECTOR_SEARCH_FIELD,
                timeout=40000)

            # get the search field web element and insert text
            search_field = self.selenium.get_webelement(
                locator=self.my_constanst.SELECTOR_SEARCH_FIELD)

            search_field.send_keys(search_phrase+"\n")

            logger.info(
                self.my_constanst.LOG_INFO_TEMPLATE.format(
                    message="Search phrase process executed correctly.",
                    function_name=source,
                    file_name=self.get_file_name(self.file_name)
                )
            )
        except Exception as e:

            self.work_items.fail(exception_type="APPLICATION",
                                 code="SEARCH_PHRASE_FAILED", message=e)
            fail_message = self.my_constanst.LOG_FAILED_TEMPLATE.format(
                message=e,
                function_name=source,
                file_name=self.get_file_name(self.file_name)
            )
            raise FailedCustomException(message=fail_message)
