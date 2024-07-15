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
            self.page.goto(
                url=self.my_constanst.NEWS_URL
            )
            # wait for hamburguer menu
            self.page.wait_for_selector(
                selector=self.my_constanst.SELECTOR_HAMBURGER_MENU,
                timeout=40000)

            # self.page.mouse.wheel(delta_y=40, delta_x=0)
            # self.page.mouse.wheel(delta_y=-40, delta_x=0)
            self.wait_this(time_seconds=3)

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
            self.page.wait_for_selector(
                selector=self.my_constanst.SELECTOR_HAMBURGER_MENU,
                timeout=40000).click()

            # clicking in the search bar and enter searchphrase
            self.page.wait_for_selector(
                selector=self.my_constanst.SELECTOR_SEARCH_FIELD,
                timeout=40000
            ).fill(value=search_phrase)

            self.page.keyboard.press('Enter')
            self.wait_this(time_seconds=2)

            # self.page.mouse.wheel(delta_y=40, delta_x=0)
            # self.page.mouse.wheel(delta_y=-25, delta_x=0)

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
